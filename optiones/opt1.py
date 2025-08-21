import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageOps
import requests
import io
import threading
import os
import re
import yt_dlp
import queue
import math
from funtions_downloands import descargar_videos_mp4

ffmpeg_path = 'ffmpeg/bin'  # Ajusta la ruta según tu sistema

class CustomProgressbar(ttk.Progressbar):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        style = ttk.Style(master)
        style.theme_use('default')
        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor='#e0e0e0',
            bordercolor='#e0e0e0',
            background='#4CAF50',
            lightcolor='#4CAF50',
            darkcolor='#388E3C',
            thickness=20
        )
        self.config(style="green.Horizontal.TProgressbar")

def mostrar_ventana_descarga(link):
    directorio_video = "C:/Users/luisc/Videos"
    resolucion = "720p"

    # Ventana de carga centrada
    carga_win = tk.Toplevel()
    carga_win.title("Cargando información")
    ancho, alto = 400, 140
    x = (carga_win.winfo_screenwidth() // 2) - (ancho // 2)
    y = (carga_win.winfo_screenheight() // 2) - (alto // 2)
    carga_win.geometry(f"{ancho}x{alto}+{x}+{y}")
    carga_win.resizable(False, False)
    carga_win.configure(bg="#f5f6fa")

    tk.Label(carga_win, text="Obteniendo información...", font=("Segoe UI", 13, "bold"), bg="#f5f6fa", fg="#222").pack(pady=(25, 10))

    # Canvas para el círculo de carga
    canvas = tk.Canvas(carga_win, width=60, height=30, bg="#f5f6fa", highlightthickness=0)
    canvas.pack()

    puntos = []
    radio = 6
    cx, cy = 30, 15
    for i in range(6):
        ang = i * (360 / 6)
        x = cx + 18 * math.cos(math.radians(ang))
        y = cy + 8 * math.sin(math.radians(ang))
        punto = canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="#b2dfdb", outline="")
        puntos.append(punto)

    def animar(ind=0):
        for i, punto in enumerate(puntos):
            color = "#26a69a" if i == ind else "#b2dfdb"
            canvas.itemconfig(punto, fill=color)
        carga_win.after(120, lambda: animar((ind+1)%6))
    animar()

    carga_win.grab_set()
    carga_win.update()

    info_queue = queue.Queue()

    def obtener_info():
        try:
            ydl_info_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                info = ydl.extract_info(link, download=False)
            info_queue.put(('ok', info))
        except Exception as e:
            info_queue.put(('error', e))

    threading.Thread(target=obtener_info, daemon=True).start()

    def revisar_info():
        try:
            estado, resultado = info_queue.get_nowait()
            carga_win.destroy()
            if estado == 'ok':
                procesar_info(resultado)
            else:
                messagebox.showerror("Error", f"No se pudo obtener la información del video.\n{resultado}")
        except queue.Empty:
            carga_win.after(100, revisar_info)

    carga_win.after(100, revisar_info)

    def procesar_info(info):
        # Si es una playlist
        if 'entries' in info and isinstance(info['entries'], list) and len(info['entries']) > 1:
            indices = seleccionar_video_playlist(info)
            if not indices:
                return  # Usuario canceló o no seleccionó nada
            for idx in indices:
                video_info = info['entries'][idx]

                try:
                    mostrar_ventana_descarga_video(video_info)
                except Exception as e:
                    print(f"Error al descargar video: {video_info.get('title', 'Desconocido')}\n{e}")
                    # Opcional: mostrar un mensaje en la interfaz
                    # messagebox.showwarning("Video omitido", f"No se pudo descargar: {video_info.get('title', 'Desconocido')}\n{e}")
        else:
            # Es un solo video
            video_info = info
            try:
                mostrar_ventana_descarga_video(video_info)
            except Exception as e:
                print(f"Error al descargar video: {video_info.get('title', 'Desconocido')}\n{e}")

    # Debes tener definida la función mostrar_ventana_descarga_video(video_info)
    # Puedes adaptarla según tu flujo, por ejemplo:
    def mostrar_ventana_descarga_video(video_info):
        enlace = video_info.get('webpage_url')
        if not enlace:
            print("No se encontró el enlace del video.")
            return
        ruta_salida = "C:/Users/luisc/Videos"
        resolucion = "720p"

        # Ventana de progreso
        progreso_win = tk.Toplevel()
        progreso_win.title("Descargando...")
        progreso_win.geometry("450x120")
        tk.Label(progreso_win, text=video_info.get('title', 'Descargando...'), font=("Segoe UI", 12)).pack(pady=10)
        barra = ttk.Progressbar(progreso_win, orient="horizontal", length=400, mode="determinate")
        barra.pack(pady=10)
        progreso_win.update_idletasks()

        # Variable para saber si la ventana sigue viva
        progreso_win.viva = True
        def on_close():
            progreso_win.viva = False
            progreso_win.destroy()
        progreso_win.protocol("WM_DELETE_WINDOW", on_close)

        def progreso_hook(d):
            if not getattr(progreso_win, "viva", False):
                return
            if d.get('status') == 'downloading':
                porcentaje = d.get('_percent_str', '0.0%').replace('%', '')
                try:
                    porcentaje = float(porcentaje)
                except Exception:
                    porcentaje = 0
                barra['value'] = porcentaje
                progreso_win.update_idletasks()
            elif d.get('status') == 'finished':
                barra['value'] = 100
                progreso_win.update_idletasks()

        def descargar():
            try:
                descargar_videos_mp4(enlace, ruta_salida, resolucion, progreso_hook)
                if getattr(progreso_win, "viva", False):
                    progreso_win.viva = False
                    progreso_win.destroy()
                    messagebox.showinfo("Descarga completada", f"Descarga completada: {video_info.get('title', '')}")
            except Exception as e:
                if getattr(progreso_win, "viva", False):
                    progreso_win.viva = False
                    progreso_win.destroy()
                messagebox.showerror("Error", f"Error al descargar {enlace}:\n{e}")

        threading.Thread(target=descargar, daemon=True).start()

def seleccionar_video_playlist(info_playlist):
    # Ventana de carga centrada con animación de círculo
    root = tk._default_root
    ancho_carga, alto_carga = 380, 160
    x_carga = (root.winfo_screenwidth() // 2) - (ancho_carga // 2)
    y_carga = (root.winfo_screenheight() // 2) - (alto_carga // 2)
    carga_win = tk.Toplevel()
    carga_win.title("Cargando información")
    carga_win.geometry(f"{ancho_carga}x{alto_carga}+{x_carga}+{y_carga}")
    carga_win.resizable(False, False)
    carga_win.configure(bg="#f5f6fa")
    tk.Label(
        carga_win,
        text="Obteniendo miniaturas...",
        font=("Segoe UI", 13, "bold"),
        bg="#f5f6fa",
        fg="#222"
    ).pack(pady=(25, 10))

    # Canvas y puntos para animación reutilizable
    canvas = tk.Canvas(carga_win, width=80, height=40, bg="#f5f6fa", highlightthickness=0)
    canvas.pack()
    puntos = []
    radio = 7
    cx, cy = 40, 20
    for i in range(8):
        ang = i * (360 / 8)
        x = cx + 22 * math.cos(math.radians(ang))
        y = cy + 10 * math.sin(math.radians(ang))
        punto = canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="#b2dfdb", outline="")
        puntos.append(punto)

    # Aquí reutilizas tu animación:
    animar_circulo(canvas, puntos)

    carga_win.grab_set()
    carga_win.update()

    thumbs_imgs = [None] * len(info_playlist['entries'])

    def cargar_todas():
        for idx, v in enumerate(info_playlist['entries']):
            url = v.get('thumbnail', '')
            img = None
            if url:
                try:
                    resp = requests.get(url, timeout=3)
                    img = Image.open(io.BytesIO(resp.content)).resize((60, 60))
                    img = ImageTk.PhotoImage(img)
                except Exception:
                    img = None
            thumbs_imgs[idx] = img

    hilo = threading.Thread(target=cargar_todas)
    hilo.start()
    while hilo.is_alive():
        carga_win.update()
    carga_win.destroy()

    # Crear ventana centrada de selección
    ancho, alto = 755, 600
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    sel_win = tk.Toplevel()
    sel_win.title("Selecciona videos de la playlist")
    sel_win.geometry(f"{ancho}x{alto}+{x}+{y}")
    sel_win.configure(bg="#f5f6fa")
    sel_win.resizable(False, False)
    sel_win.grab_set()

    cancelado = {"valor": False}
    def on_close():
        cancelado["valor"] = True
        sel_win.destroy()
    sel_win.protocol("WM_DELETE_WINDOW", on_close)

    # Rectángulo superior con texto
    header = tk.Frame(sel_win, bg="#26a69a", height=60)
    header.pack(fill="x", side="top")
    tk.Label(
        header,
        text="Elija el video para descargar",
        bg="#26a69a",
        fg="white",
        font=("Segoe UI", 16, "bold"),
        pady=15
    ).pack()

    # Scrollable frame para la lista
    lista_frame = tk.Frame(sel_win, bg="#f5f6fa")
    lista_frame.pack(fill="both", expand=True, padx=10, pady=(10,0))

    canvas = tk.Canvas(lista_frame, bg="#f5f6fa", highlightthickness=0, width=520, height=430)
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg="#f5f6fa")

    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    checks = []

    style = ttk.Style()
    style.configure("Custom.TCheckbutton", background="#f5f6fa", foreground="#26a69a", font=("Segoe UI", 13))

    for i, v in enumerate(info_playlist['entries']):
        fila = tk.Frame(frame, bg="#f5f6fa", pady=8)
        fila.pack(fill="x", padx=5)

        # Miniatura
        thumb_label = tk.Label(fila, bg="#e0e0e0", width=60, height=60)
        thumb_label.pack(side="left", padx=(0, 8))
        if thumbs_imgs[i]:
            thumb_label.configure(image=thumbs_imgs[i])
            thumb_label.image = thumbs_imgs[i]

        # Título y duración
        nombre = v.get('title', 'Sin título')
        duracion = v.get('duration', 0)
        minutos = duracion // 60
        segundos = duracion % 60
        duracion_str = f"{minutos}:{segundos:02d}"
        info_label = tk.Label(
            fila,
            text=f"{nombre}\nduración: {duracion_str}",
            anchor="w",
            justify="left",
            bg="#f5f6fa",
            fg="#333",
            font=("Segoe UI", 11)
        )
        info_label.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Checkbox bonito y alineado, más cerca del texto
        var = tk.BooleanVar()
        check = ttk.Checkbutton(
            fila,
            variable=var,
            style="Custom.TCheckbutton"
        )
        check.pack(side="right", padx=(0, 8))
        checks.append(var)

        # Línea divisoria
        if i < len(info_playlist['entries']) - 1:
            sep = tk.Frame(frame, bg="#bdbdbd", height=2)
            sep.pack(fill="x", padx=5, pady=(0, 0))

    seleccionados = []

    def aceptar():
        seleccionados.clear()
        for i, var in enumerate(checks):
            if var.get():
                seleccionados.append(i)
        sel_win.destroy()

    # Botón llamativo abajo de la ventana
    btn = tk.Button(
        sel_win,
        text="Descargar seleccionados",
        command=aceptar,
        bg="#26a69a",
        fg="white",
        font=("Segoe UI", 14, "bold"),
        activebackground="#00796b",
        activeforeground="white",
        relief="flat",
        height=2
    )
    btn.pack(side="bottom", fill="x", padx=30, pady=20)

    sel_win.wait_window()
    if cancelado["valor"] or not seleccionados:
        return None
    return seleccionados

def animar_circulo(canvas, puntos, delay=120):
    def animar(ind=0):
        for i, punto in enumerate(puntos):
            color = "#26a69a" if i == ind else "#b2dfdb"
            canvas.itemconfig(punto, fill=color)
        canvas.after(delay, lambda: animar((ind+1)%len(puntos)))
    animar()

# Ejemplo de barra de progreso para usar en tu ventana de descarga:
def mostrar_progreso_descarga(ventana, porcentaje):
    # ventana: la ventana donde mostrar el progreso
    # porcentaje: valor entre 0 y 100
    if not hasattr(ventana, 'barra_progreso'):
        ventana.barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate")
        ventana.barra_progreso.pack(pady=10)
    ventana.barra_progreso['value'] = porcentaje
    ventana.update_idletasks()


