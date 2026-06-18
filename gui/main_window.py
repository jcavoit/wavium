import sys
import os
from pathlib import Path

from PySide6.QtCore    import Qt, QUrl
from PySide6.QtGui     import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QRadioButton, QProgressBar, QFileDialog,
    QFrame, QSizePolicy, QSpacerItem, QScrollArea,
    QApplication,
)

from core           import extraer_formatos, carpeta_por_defecto
from core.validator import validar_url
from gui.workers    import WorkerInfo, WorkerDescarga
from gui.styles     import ESTILO


def ruta_recurso(relativa: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relativa)


APP_NOMBRE = "wavium"
TAGLINE_1  = "El mejor audio converter jamás creado."
TAGLINE_2  = "Para artistas, por artistas."
LOGO_PATH  = ruta_recurso("assets/logo.png")


class MainWindow(QMainWindow):

    def __init__(self, ytdlp_path: str = None):   # ← recibe ytdlp_path
        super().__init__()
        self.ytdlp_path = ytdlp_path              # ← lo guarda

        self.setWindowTitle("Wavium")
        self.setMinimumWidth(620)

        pantalla = QApplication.primaryScreen().size()
        self.resize(pantalla.width(), pantalla.height())

        self.setStyleSheet(ESTILO)

        self._formatos_crudos = []
        self._metadatos       = {}
        self._worker_info     = None
        self._worker_descarga = None

        self._network = QNetworkAccessManager()
        self._network.finished.connect(self._on_miniatura_descargada)

        self._construir_ui()

    def _construir_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        interior = QWidget()
        scroll.setWidget(interior)

        fila = QHBoxLayout(interior)
        fila.setContentsMargins(0, 0, 0, 0)
        fila.setSpacing(0)

        columna = QWidget()
        columna.setFixedWidth(580)

        root = QVBoxLayout(columna)
        root.setContentsMargins(28, 32, 28, 32)
        root.setSpacing(20)

        root.addLayout(self._seccion_header())
        root.addLayout(self._seccion_url())
        root.addWidget(self._card_preview())
        root.addWidget(self._card_opciones())
        root.addWidget(self._card_descarga())
        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        fila.addStretch()
        fila.addWidget(columna)
        fila.addStretch()

    def _seccion_header(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(16)

        lbl_logo = QLabel()
        if os.path.exists(LOGO_PATH):
            pix = QPixmap(LOGO_PATH).scaled(
                64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            lbl_logo.setPixmap(pix)
        else:
            lbl_logo.setText("W")
            lbl_logo.setStyleSheet("""
                background-color: #1a1f2e;
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                border-radius: 14px;
                padding: 8px 14px;
            """)
        lbl_logo.setFixedSize(64, 64)
        layout.addWidget(lbl_logo, alignment=Qt.AlignVCenter)

        textos = QVBoxLayout()
        textos.setSpacing(2)

        lbl_nombre = QLabel(APP_NOMBRE)
        lbl_nombre.setObjectName("label_app_nombre")

        lbl_t1 = QLabel(TAGLINE_1)
        lbl_t1.setObjectName("label_tagline_1")

        lbl_t2 = QLabel(TAGLINE_2)
        lbl_t2.setObjectName("label_tagline_2")

        textos.addWidget(lbl_nombre)
        textos.addWidget(lbl_t1)
        textos.addWidget(lbl_t2)

        layout.addLayout(textos)
        layout.addStretch()

        return layout

    def _seccion_url(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("Pega la URL de YouTube aquí...")
        self.input_url.returnPressed.connect(self._obtener_info)

        self.btn_info = QPushButton("Obtener información")
        self.btn_info.setFixedHeight(44)
        self.btn_info.clicked.connect(self._obtener_info)

        layout.addWidget(self.input_url)
        layout.addWidget(self.btn_info)
        return layout

    def _card_preview(self) -> QFrame:
        self.card_preview = QFrame()
        self.card_preview.setObjectName("card_preview")
        self.card_preview.setVisible(False)

        layout = QHBoxLayout(self.card_preview)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        self.lbl_miniatura = QLabel()
        self.lbl_miniatura.setFixedSize(100, 56)
        self.lbl_miniatura.setStyleSheet(
            "border-radius: 8px; background-color: #e8e8f0;"
        )
        self.lbl_miniatura.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_miniatura, alignment=Qt.AlignTop)

        info = QVBoxLayout()
        info.setSpacing(4)

        self.lbl_video_titulo = QLabel()
        self.lbl_video_titulo.setObjectName("label_video_titulo")
        self.lbl_video_titulo.setWordWrap(True)

        self.lbl_video_meta = QLabel()
        self.lbl_video_meta.setObjectName("label_video_meta")

        info.addWidget(self.lbl_video_titulo)
        info.addWidget(self.lbl_video_meta)
        info.addStretch()
        layout.addLayout(info)

        return self.card_preview

    def _card_opciones(self) -> QFrame:
        self.card_opciones = QFrame()
        self.card_opciones.setObjectName("card_opciones")
        self.card_opciones.setVisible(False)

        layout = QVBoxLayout(self.card_opciones)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        lbl_modo = QLabel("MODO")
        lbl_modo.setObjectName("label_seccion")
        layout.addWidget(lbl_modo)

        modo_row = QHBoxLayout()
        self.radio_video = QRadioButton("Vídeo")
        self.radio_audio = QRadioButton("Solo audio (WAV)")
        self.radio_audio.setChecked(True)
        self.radio_video.toggled.connect(self._on_modo_cambiado)
        modo_row.addWidget(self.radio_video)
        modo_row.addWidget(self.radio_audio)
        modo_row.addStretch()
        layout.addLayout(modo_row)

        self.lbl_resolucion = QLabel("RESOLUCIÓN")
        self.lbl_resolucion.setObjectName("label_seccion")
        self.combo_resolucion = QComboBox()
        self.combo_resolucion.setFixedWidth(160)
        self.lbl_resolucion.setVisible(False)
        self.combo_resolucion.setVisible(False)
        layout.addWidget(self.lbl_resolucion)
        layout.addWidget(self.combo_resolucion, alignment=Qt.AlignLeft)

        lbl_carpeta = QLabel("CARPETA DE DESTINO")
        lbl_carpeta.setObjectName("label_seccion")
        layout.addWidget(lbl_carpeta)

        carpeta_row = QHBoxLayout()
        carpeta_row.setSpacing(8)

        self.input_carpeta = QLineEdit()
        self.input_carpeta.setText(carpeta_por_defecto())
        self.input_carpeta.setReadOnly(True)

        self.btn_carpeta = QPushButton("···")
        self.btn_carpeta.setObjectName("btn_carpeta")
        self.btn_carpeta.setFixedWidth(52)
        self.btn_carpeta.setFixedHeight(44)
        self.btn_carpeta.clicked.connect(self._elegir_carpeta)

        carpeta_row.addWidget(self.input_carpeta)
        carpeta_row.addWidget(self.btn_carpeta)
        layout.addLayout(carpeta_row)

        return self.card_opciones

    def _card_descarga(self) -> QFrame:
        self.card_descarga = QFrame()
        self.card_descarga.setObjectName("card_opciones")
        self.card_descarga.setVisible(False)

        layout = QVBoxLayout(self.card_descarga)
        layout.setContentsMargins(20, 22, 20, 22)
        layout.setSpacing(14)

        self.btn_descargar = QPushButton("Descargar")
        self.btn_descargar.setFixedHeight(48)
        self.btn_descargar.clicked.connect(self._iniciar_descarga)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(8)
        self.progress.setVisible(False)

        self.lbl_estado = QLabel("")
        self.lbl_estado.setObjectName("label_estado")
        self.lbl_estado.setAlignment(Qt.AlignCenter)
        self.lbl_estado.setMinimumHeight(28)

        layout.addWidget(self.btn_descargar)
        layout.addWidget(self.progress)
        layout.addWidget(self.lbl_estado)

        return self.card_descarga

    def _obtener_info(self):
        url = self.input_url.text().strip()
        if not validar_url(url):
            self._set_estado("❌ URL no válida.", error=True)
            return

        self.btn_info.setEnabled(False)
        self.btn_info.setText("Obteniendo información...")
        self.card_preview.setVisible(False)
        self.card_opciones.setVisible(False)
        self.card_descarga.setVisible(False)
        self._set_estado("")

        self._worker_info = WorkerInfo(self.input_url.text().strip())
        self._worker_info.completado.connect(self._on_info_recibida)
        self._worker_info.error.connect(self._on_info_error)
        self._worker_info.start()

    def _on_info_recibida(self, metadatos: dict, formatos_crudos: list):
        self._metadatos       = metadatos
        self._formatos_crudos = formatos_crudos

        self.lbl_video_titulo.setText(metadatos.get("titulo", ""))
        self.lbl_video_meta.setText(
            f"{metadatos.get('canal', '')}  ·  {metadatos.get('duracion', '')}"
        )

        miniatura = metadatos.get("miniatura")
        if miniatura:
            self._network.get(QNetworkRequest(QUrl(miniatura)))

        formatos = extraer_formatos(formatos_crudos)
        self.combo_resolucion.clear()
        for v in formatos["video"]:
            self.combo_resolucion.addItem(v["resolucion"], v)

        self.card_preview.setVisible(True)
        self.card_opciones.setVisible(True)
        self.card_descarga.setVisible(True)

        self.btn_info.setEnabled(True)
        self.btn_info.setText("Obtener información")

    def _on_info_error(self, mensaje: str):
        self._set_estado(f"❌ {mensaje}", error=True)
        self.btn_info.setEnabled(True)
        self.btn_info.setText("Obtener información")

    def _on_miniatura_descargada(self, reply):
        data = reply.readAll()
        pix  = QPixmap()
        pix.loadFromData(data)
        if not pix.isNull():
            pix = pix.scaled(100, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_miniatura.setPixmap(pix)

    def _on_modo_cambiado(self, video_activo: bool):
        self.lbl_resolucion.setVisible(video_activo)
        self.combo_resolucion.setVisible(video_activo)

    def _elegir_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta de destino", self.input_carpeta.text()
        )
        if carpeta:
            self.input_carpeta.setText(carpeta)

    def _iniciar_descarga(self):
        url     = self.input_url.text().strip()
        carpeta = self.input_carpeta.text().strip()

        if not url or not carpeta:
            return

        solo_audio = self.radio_audio.isChecked()
        resolucion = "720p"
        if not solo_audio and self.combo_resolucion.count() > 0:
            resolucion = self.combo_resolucion.currentText()

        self.btn_descargar.setEnabled(False)
        self.btn_descargar.setText("Descargando...")
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.lbl_estado.setVisible(True)
        self._set_estado("Iniciando descarga...")

        self._worker_descarga = WorkerDescarga(
            url           = url,
            carpeta       = carpeta,
            resolucion    = resolucion,
            solo_audio    = solo_audio,
            formato_audio = "wav",
            ytdlp_path    = self.ytdlp_path,   # ← pasa el path
        )
        self._worker_descarga.progreso.connect(self.progress.setValue)
        self._worker_descarga.estado.connect(self._set_estado)
        self._worker_descarga.terminado.connect(self._on_descarga_terminada)
        self._worker_descarga.start()

    def _on_descarga_terminada(self, exito: bool, mensaje: str):
        self.btn_descargar.setEnabled(True)
        self.btn_descargar.setText("Descargar")
        self._set_estado(mensaje, error=not exito, ok=exito)
        if exito:
            self.progress.setValue(100)

    def _set_estado(self, texto: str, error: bool = False, ok: bool = False):
        self.lbl_estado.setText(texto)
        if error:
            self.lbl_estado.setObjectName("label_estado_error")
        elif ok:
            self.lbl_estado.setObjectName("label_estado_ok")
        else:
            self.lbl_estado.setObjectName("label_estado")
        self.lbl_estado.setStyle(self.lbl_estado.style())
