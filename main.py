import os
import tkinter as tk
from PIL import Image, ImageTk

def mostrar_loadscreen(duracion=3):
    load = tk.Tk()
    load.overrideredirect(True)  # Quita la barra de título

    # Cargar imagen JPG usando PIL
    imagen_pil = Image.open("src/YTDownloader.jpg")
    ancho, alto = imagen_pil.size
    imagen = ImageTk.PhotoImage(imagen_pil)

    # Obtener tamaño de la pantalla
    screen_width = load.winfo_screenwidth()
    screen_height = load.winfo_screenheight()

    # Calcular posición para centrar
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    # Ajustar tamaño y posición de la ventana
    load.geometry(f"{ancho}x{alto}+{x}+{y}")

    label_img = tk.Label(load, image=imagen)
    label_img.image = imagen
    label_img.pack()

    load.after(duracion * 1000, load.destroy)
    load.mainloop()

def mostrar_terminos_si_primera_vez():
    marcador = ".primary"
    if not os.path.exists(marcador):
        from visual.terminos import mostrar_terminos
        mostrar_terminos()
        with open(marcador, "w") as f:
            f.write("ok")

if __name__ == "__main__":
    mostrar_terminos_si_primera_vez()
    mostrar_loadscreen()
 # Importa y muestra el home usando Toplevel
     # Crear la ventana principal y ocultarla
    root = tk.Tk()
    root.withdraw()
    
    from visual.home import mostrar_home
    mostrar_home(root)
    
    root.mainloop()