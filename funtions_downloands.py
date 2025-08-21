#librerias
import os
import re
import yt_dlp
from configurations import leer_configuracion

#variables
ffmpeg_path = 'ffmpeg/bin'  # Tener en cuenta la ruta de ffmpeg en tu sistema


def leer_enlaces(ruta_archivo):
    """Lee los enlaces desde un archivo de texto."""
    try:
        with open(ruta_archivo, 'r') as archivo:
            enlaces = [linea.strip() for linea in archivo.readlines()]
        return enlaces
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no existe.")
        return []

def descargar_audio_mp3(enlace, ruta_salida):
    try:
        if not os.path.exists(ffmpeg_path):
            print(f"La ruta de ffmpeg no existe: {ffmpeg_path}")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(ruta_salida, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([enlace])
        print(f"Descarga completada: {enlace}")
    except Exception as e:
        print(f"Error al descargar {enlace}: {e}")


def descargar_audio_mp3_url(enlace, ruta_salida):
    try:
        configuracion = leer_configuracion()
        calidad_audio = configuracion.get("calidad_audio", "192kbps")  # Leer la calidad de audio del archivo de configuración

        if not os.path.exists(ffmpeg_path):
            print(f"La ruta de ffmpeg no existe: {ffmpeg_path}")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': calidad_audio,
            }],
            'outtmpl': os.path.join(ruta_salida, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([enlace])
        print(f"Descarga completada: {enlace}")
    except Exception as e:
        print(f"Error al descargar {enlace}: {e}")

def descargar_videos_mp4(enlace, ruta_salida, resolucion, progreso_callback):
    try:
        resolution = re.sub(r'[p]','',resolucion)
        if not os.path.exists(ffmpeg_path):
            print(f"La ruta de ffmpeg no existe: {ffmpeg_path}")
            return

        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best/best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'outtmpl': os.path.join(ruta_salida, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,
        }
        if progreso_callback:
            ydl_opts['progress_hooks'] = [progreso_callback]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([enlace])
        print(f"Descarga completada: {enlace}")
    except Exception as e:
        print(f"Error al descargar {enlace}: {e}")
