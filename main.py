import sys
import os
import shutil
import subprocess
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui     import QIcon
from gui.main_window   import MainWindow


def ruta_recurso(relativa: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relativa)


def preparar_ytdlp() -> str:
    destino = Path(os.getenv("APPDATA")) / "Wavium" / "yt-dlp.exe"
    destino.parent.mkdir(parents=True, exist_ok=True)

    if not destino.exists():
        origen = ruta_recurso("assets/yt-dlp.exe")
        shutil.copy(origen, destino)

    try:
        subprocess.run([str(destino), "-U"], capture_output=True, timeout=15)
    except Exception:
        pass

    return str(destino)


if __name__ == "__main__":
    ytdlp_path = preparar_ytdlp()

    app = QApplication(sys.argv)
    app.setApplicationName("Wavium")
    app.setApplicationVersion("1.0.0")
    app.setWindowIcon(QIcon(ruta_recurso("assets/logo.png")))

    window = MainWindow(ytdlp_path=ytdlp_path)
    window.showMaximized()

    sys.exit(app.exec())
