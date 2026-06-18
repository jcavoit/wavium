import re

def validar_url(url: str) -> bool:
    patron = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
    return bool(re.match(patron, url.strip())) 