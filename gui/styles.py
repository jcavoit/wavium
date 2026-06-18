

ESTILO = """

/* ── Base ─────────────────────────────────────────────────────────────────── */

QWidget {
    background-color: #f7f7fa;
    color: #1a1f2e;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
    border: none;
}

QMainWindow {
    background-color: #f7f7fa;
}

/* ── Inputs ────────────────────────────────────────────────────────────────── */

QLineEdit {
    background-color: #ffffff;
    border: 1.5px solid #e2e2ea;
    border-radius: 12px;
    padding: 11px 16px;
    font-size: 14px;
    color: #1a1f2e;
    selection-background-color: #6c5ce7;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 1.5px solid #6c5ce7;
    background-color: #ffffff;
}

QLineEdit:disabled {
    background-color: #f0f0f5;
    color: #9999aa;
    border: 1.5px solid #e2e2ea;
}

/* ── Botones ───────────────────────────────────────────────────────────────── */

QPushButton {
    background-color: #6c5ce7;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 11px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #5a4dd4;
}

QPushButton:pressed {
    background-color: #4a3ec0;
}

QPushButton:disabled {
    background-color: #e2e2ea;
    color: #9999aa;
}

QPushButton#btn_secundario {
    background-color: #ebebf0;
    color: #1a1f2e;
    font-weight: 500;
}

QPushButton#btn_secundario:hover {
    background-color: #dddde8;
}

QPushButton#btn_carpeta {
    background-color: #ebebf0;
    color: #1a1f2e;
    border-radius: 12px;
    padding: 11px 16px;
    font-size: 13px;
    font-weight: 500;
    min-width: 44px;
}

QPushButton#btn_carpeta:hover {
    background-color: #dddde8;
}

/* ── ComboBox ──────────────────────────────────────────────────────────────── */

QComboBox {
    background-color: #ffffff;
    border: 1.5px solid #e2e2ea;
    border-radius: 12px;
    padding: 11px 16px;
    font-size: 14px;
    color: #1a1f2e;
    min-width: 140px;
}

QComboBox:focus {
    border: 1.5px solid #6c5ce7;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1.5px solid #e2e2ea;
    border-radius: 8px;
    selection-background-color: #6c5ce7;
    selection-color: #ffffff;
    padding: 4px;
}

/* ── ProgressBar ───────────────────────────────────────────────────────────── */

QProgressBar {
    background-color: #e8e8f0;
    border: none;
    border-radius: 4px;
    height: 6px;
    font-size: 0px;
}

QProgressBar::chunk {
    background-color: #6c5ce7;
    border-radius: 4px;
}

/* ── RadioButtons ──────────────────────────────────────────────────────────── */

QRadioButton {
    font-size: 14px;
    color: #1a1f2e;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #d0d0dc;
    background-color: #ffffff;
}

QRadioButton::indicator:checked {
    border: 2px solid #6c5ce7;
    background-color: #6c5ce7;
}

QRadioButton::indicator:hover {
    border: 2px solid #6c5ce7;
}

/* ── Cards ─────────────────────────────────────────────────────────────────── */

QFrame#card_preview {
    background-color: #ffffff;
    border-radius: 16px;
    border: 1.5px solid #e8e8f0;
}

QFrame#card_opciones {
    background-color: #ffffff;
    border-radius: 16px;
    border: 1.5px solid #e8e8f0;
}

/* ── Labels ────────────────────────────────────────────────────────────────── */

QLabel#label_app_nombre {
    font-size: 26px;
    font-weight: 700;
    color: #1a1f2e;
    letter-spacing: -0.5px;
}

QLabel#label_tagline_1 {
    font-size: 12px;
    color: #6e6e8a;
}

QLabel#label_tagline_2 {
    font-size: 12px;
    font-weight: 500;
    color: #6c5ce7;
}

QLabel#label_video_titulo {
    font-size: 15px;
    font-weight: 600;
    color: #1a1f2e;
}

QLabel#label_video_meta {
    font-size: 13px;
    color: #6e6e8a;
}

QLabel#label_estado {
    font-size: 12px;
    color: #6e6e8a;
}

QLabel#label_estado_error {
    font-size: 12px;
    color: #e74c3c;
}

QLabel#label_estado_ok {
    font-size: 12px;
    color: #27ae60;
}

QLabel#label_seccion {
    font-size: 11px;
    font-weight: 600;
    color: #9999aa;
    letter-spacing: 0.8px;
}

/* ── ScrollBar ─────────────────────────────────────────────────────────────── */

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #d0d0dc;
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

"""