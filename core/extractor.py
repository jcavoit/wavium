import yt_dlp



def _segundos_a_tiempo(segundos: int) -> str:
    if not segundos:
        return "0:00"
    horas   = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs    = segundos % 60
    if horas > 0:
        return f"{horas}:{minutos:02d}:{segs:02d}"
    return f"{minutos}:{segs:02d}"


def _formatear_tamanio(bytes_: int | None) -> str:
    if not bytes_:
        return "Tamaño desconocido"
    for unidad in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unidad}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"



def _clasificar_stream(f: dict) -> str:
    tiene_video = f.get("vcodec", "none") != "none"
    tiene_audio = f.get("acodec", "none") != "none"
    if tiene_video and tiene_audio:
        return "combinado"
    if tiene_video:
        return "solo_video"
    if tiene_audio:
        return "solo_audio"
    return "desconocido"


def _es_formato_util(f: dict, tipo: str) -> bool:
    ext = f.get("ext", "")
    if tipo == "solo_audio":
        return ext in {"m4a", "webm"}
    if tipo in ("solo_video", "combinado"):
        altura = f.get("height")
        return bool(altura and altura >= 144 and ext in {"mp4", "webm"})
    return False


def _deduplicar_por_resolucion(formatos: list) -> list:
    vistos = {}
    for f in formatos:
        altura = f["height"]
        if altura not in vistos or (f["ext"] == "mp4" and vistos[altura]["ext"] != "mp4"):
            vistos[altura] = f
    return list(vistos.values())



def extraer_formatos(formatos_crudos: list) -> dict:
    videos = []
    audios = []

    for f in formatos_crudos:
        tipo = _clasificar_stream(f)
        if not _es_formato_util(f, tipo):
            continue

        tamanio = _formatear_tamanio(f.get("filesize") or f.get("filesize_approx"))

        if tipo == "solo_audio":
            audios.append({
                "format_id": f.get("format_id"),
                "ext":       f.get("ext"),
                "calidad":   f.get("abr", 0),
                "tamanio":   tamanio,
                "codec":     f.get("acodec", "?"),
            })
        elif tipo in ("solo_video", "combinado"):
            videos.append({
                "format_id":   f.get("format_id"),
                "resolucion":  f"{f.get('height')}p",
                "ext":         f.get("ext"),
                "fps":         f.get("fps", 30),
                "tiene_audio": tipo == "combinado",
                "tamanio":     tamanio,
                "codec":       f.get("vcodec", "?"),
                "height":      f.get("height"),
            })

    videos = _deduplicar_por_resolucion(videos)
    videos = sorted(videos, key=lambda x: x["height"], reverse=True)
    audios = sorted(audios, key=lambda x: x["calidad"], reverse=True)

    return {
        "video": videos,
        "audio": audios[:3],
    }



def ping_video(url: str) -> dict:
    opciones = {
        "quiet":        True,
        "no_warnings":  True,
        "extract_flat": "in_playlist",
        "noplaylist":   True,
    }
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        raise Exception(f"No se puede acceder al vídeo: {e}")

    return {
        "titulo":   info.get("title", "Sin título"),
        "duracion": _segundos_a_tiempo(info.get("duration", 0)),
    }



def obtener_info(url: str) -> tuple[dict, list]:
    opciones = {
        "quiet":             True,
        "no_warnings":       True,
        "noplaylist":        True,
        "writesubtitles":    False,
        "writeautomaticsub": False,
        "writethumbnail":    False,
    }
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"Vídeo no disponible: {e}")
    except yt_dlp.utils.ExtractorError as e:
        raise Exception(f"Error al extraer información: {e}")

    metadatos = {
        "titulo":    info.get("title",    "Sin título"),
        "duracion":  _segundos_a_tiempo(info.get("duration", 0)),
        "miniatura": info.get("thumbnail"),
        "canal":     info.get("uploader", "Desconocido"),
    }

    return metadatos, info.get("formats", [])