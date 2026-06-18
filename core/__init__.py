

from core.validator import validar_url
from core.extractor import ping_video, obtener_info, extraer_formatos
from core.downloader import descargar, descargar_async, ErrorDescarga

from pathlib import Path

def carpeta_por_defecto() -> str:
    """Devuelve la carpeta Downloads del usuario actual en cualquier sistema."""
    return str(Path.home() / "Downloads")

__all__ = [
    "validar_url",
    "ping_video",
    "obtener_info",
    "extraer_formatos",
    "descargar",
    "descargar_async",
    "ErrorDescarga",
    "carpeta_por_defecto",
]