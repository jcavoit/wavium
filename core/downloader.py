import sys
import os
import threading
import yt_dlp

from core.validator import validar_url


def ruta_recurso(relativa: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', relativa)


FFMPEG_PATH = ruta_recurso("assets/ffmpeg.exe")


class ErrorDescarga(Exception):
    pass


def crear_hook(callback_progreso, callback_estado):
    def hook(d: dict):
        if d["status"] == "downloading":
            total      = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            descargado = d.get("downloaded_bytes", 0)
            velocidad  = d.get("speed") or 0
            eta        = d.get("eta") or 0

            if total > 0:
                callback_progreso(int(descargado / total * 100))

            vel_str = f"{velocidad / 1_048_576:.1f} MB/s" if velocidad else "..."
            callback_estado(f"Descargando... {vel_str}  |  ETA: {eta}s")

        elif d["status"] == "finished":
            callback_progreso(100)
            callback_estado("Procesando con FFmpeg...")

        elif d["status"] == "error":
            callback_estado("❌ Error durante la descarga")

    return hook


def construir_opciones(carpeta, resolucion, solo_audio,
                        hook_progreso, formato_audio="wav",
                        ytdlp_path=None) -> dict:
    base = {
        "outtmpl":         f"{carpeta}/%(title)s.%(ext)s",
        "noplaylist":      True,
        "quiet":           True,
        "progress_hooks":  [hook_progreso],
        "ffmpeg_location": FFMPEG_PATH,
    }

    if ytdlp_path:
        base["yt_dlp_filename"] = ytdlp_path

    if solo_audio:
        base["format"] = "bestaudio/best"
        base["postprocessors"] = [{
            "key":              "FFmpegExtractAudio",
            "preferredcodec":   formato_audio,
            "preferredquality": "0",
        }]
    else:
        altura = resolucion.replace("p", "")
        base["format"] = (
            f"bestvideo[height<={altura}][ext=mp4]+bestaudio[ext=m4a]"
            f"/bestvideo[height<={altura}]+bestaudio"
            f"/best[height<={altura}]"
        )
        base["merge_output_format"] = "mp4"

    return base


def descargar(url, carpeta, resolucion="720p", solo_audio=False,
              callback_progreso=None, callback_estado=None,
              formato_audio="wav", ytdlp_path=None):
    if not validar_url(url):
        raise ErrorDescarga("URL no válida. Introduce una URL de YouTube correcta.")

    hook = crear_hook(
        callback_progreso or (lambda p: None),
        callback_estado   or (lambda s: None),
    )
    opciones = construir_opciones(
        carpeta, resolucion, solo_audio, hook, formato_audio, ytdlp_path
    )

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        raise ErrorDescarga(f"No se pudo descargar el vídeo: {e}")
    except Exception as e:
        raise ErrorDescarga(f"Error inesperado: {e}")


def descargar_async(url, carpeta, resolucion="720p", solo_audio=False,
                    callback_progreso=None, callback_estado=None,
                    callback_fin=None, formato_audio="wav",
                    ytdlp_path=None) -> threading.Thread:
    def _tarea():
        try:
            descargar(url, carpeta, resolucion, solo_audio,
                      callback_progreso, callback_estado,
                      formato_audio, ytdlp_path)
            if callback_fin:
                callback_fin(exito=True, mensaje="✅ Descarga completada.")
        except ErrorDescarga as e:
            if callback_fin:
                callback_fin(exito=False, mensaje=str(e))

    hilo = threading.Thread(target=_tarea, daemon=True)
    hilo.start()
    return hilo
