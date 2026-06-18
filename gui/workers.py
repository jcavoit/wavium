from pathlib import Path

from PySide6.QtCore import QThread, Signal

from core.downloader import descargar, ErrorDescarga


class WorkerInfo(QThread):
    completado = Signal(dict, list)
    error      = Signal(str)

    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            from core.extractor import obtener_info
            metadatos, formatos_crudos = obtener_info(self.url)
            self.completado.emit(metadatos, formatos_crudos)
        except Exception as e:
            self.error.emit(str(e))


class WorkerDescarga(QThread):
    progreso  = Signal(int)
    estado    = Signal(str)
    terminado = Signal(bool, str)

    def __init__(self, url, carpeta, resolucion="720p",
                 solo_audio=False, formato_audio="wav",
                 ytdlp_path=None, parent=None):
        super().__init__(parent)
        self.url           = url
        self.carpeta       = carpeta
        self.resolucion    = resolucion
        self.solo_audio    = solo_audio
        self.formato_audio = formato_audio
        self.ytdlp_path    = ytdlp_path   # ← nuevo

    def run(self):
        Path(self.carpeta).mkdir(parents=True, exist_ok=True)
        try:
            descargar(
                url               = self.url,
                carpeta           = self.carpeta,
                resolucion        = self.resolucion,
                solo_audio        = self.solo_audio,
                callback_progreso = self.progreso.emit,
                callback_estado   = self.estado.emit,
                formato_audio     = self.formato_audio,
                ytdlp_path        = self.ytdlp_path,   # ← nuevo
            )
            self.terminado.emit(True, "✅ Descarga completada")
        except ErrorDescarga as e:
            self.terminado.emit(False, str(e))
        except Exception as e:
            self.terminado.emit(False, f"Error inesperado: {e}")
