#librerias
import os
import time

#-----------Funcion para generar archivo de configuracion-----------------
def generar_archivo_configuracion():
    # Nombre del archivo con extensión .cfg
    nombre_archivo = "data.cfg"
    
    # Verificar si el archivo ya existe
    if not os.path.exists(nombre_archivo):
        # Obtener el directorio del usuario actual
        directorio_usuario = os.path.expanduser("~")
        directorio_musica = os.path.join(directorio_usuario, "Music/yt_downloader")
        directorio_videos = os.path.join(directorio_usuario, "Videos/yt_downloader")
        
        # Crear las carpetas si no existen
        os.makedirs(directorio_musica, exist_ok=True)
        os.makedirs(directorio_videos, exist_ok=True)
        
        configuracion = {
            "calidad_video": "1080p",
            "calidad_audio": "320kbps",
            "directorio_musica": directorio_musica,
            "directorio_videos": directorio_videos
        }
        
        # Crear el archivo y escribir la configuración
        with open(nombre_archivo, 'w') as archivo:
            for clave, valor in configuracion.items():
                archivo.write(f"{clave}: {valor}\n")

#-----------Funcion para leer configuracion-----------------        
def leer_configuracion():
    configuracion = {}
    with open("data.cfg", 'r') as archivo:
        for linea in archivo:
            clave, valor = linea.strip().split(": ")
            configuracion[clave] = valor
    return configuracion

#-----------Funcion para escribir configuracion-----------------
def escribir_configuracion(configuracion):
    with open("data.cfg", 'w') as archivo:
        for clave, valor in configuracion.items():
            archivo.write(f"{clave}: {valor}\n")

#-----------Funcion para cambiar calidad del video-----------------
def cambiar_calidad_video(configuracion):
    calidades_validas = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    print("Calidades válidas: ", ', '.join(calidades_validas))
    while True:
        nueva_calidad = input("Ingrese la nueva calidad de video: ")
        if nueva_calidad in calidades_validas:
            configuracion["calidad_video"] = nueva_calidad
            escribir_configuracion(configuracion)
            os.system("cls")
            print("Calidad de video actualizada.")
            time.sleep(2)
            os.system("cls")
            return True
        else:
            print("Calidad de video no válida. Por favor, ingrese una de las siguientes opciones: ", ', '.join(calidades_validas))

#-----------Funcion para cambiar directorio de musica -----------------
def cambiar_directorio_musica(configuracion):
    while True:
        nuevo_directorio = input("Ingrese el nuevo directorio de descarga de música: ")
        if os.path.isdir(nuevo_directorio):
            configuracion["directorio_musica"] = nuevo_directorio
            escribir_configuracion(configuracion)
            print("Directorio de descarga de música actualizado.")
            time.sleep(2)
            os.system("cls")
            return True
        else:
            print("Directorio no válido. Por favor, ingrese un directorio válido.")

#-----------Funcion para cambiar directorio de videos-----------------
def cambiar_directorio_videos(configuracion):
    while True:
        nuevo_directorio = input("Ingrese el nuevo directorio de descarga de videos: ")
        if os.path.isdir(nuevo_directorio):
            configuracion["directorio_videos"] = nuevo_directorio
            escribir_configuracion(configuracion)
            print("Directorio de descarga de videos actualizado.")
            time.sleep(2)
            os.system("cls")
            return True
        else:
            print("Directorio no válido. Por favor, ingrese un directorio válido.")
