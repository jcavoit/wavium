import time
from core import obtener_info, extraer_formatos, descargar_async

URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

meta, crudos = obtener_info(URL)
print(meta)

formatos = extraer_formatos(crudos)
print([v["resolucion"] for v in formatos["video"]])

terminado = {"valor": False}

def al_terminar(exito, mensaje):
    print(mensaje)
    terminado["valor"] = True

descargar_async(
    url=URL,
    carpeta=r"C:\Users\caavo\Desktop\yt-wav\descargas",
    solo_audio=True,
    callback_progreso=lambda p: print(f"{p}%"),
    callback_estado=lambda s: print(s),
    callback_fin=al_terminar,
)

# Esperar hasta que callback_fin confirme que terminó de verdad
while not terminado["valor"]:
    time.sleep(0.5)

print("Archivo guardado en descargas/")