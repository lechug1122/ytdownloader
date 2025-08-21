import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
from optiones.opt1 import mostrar_ventana_descarga
def mostrar_home(root):
    home = tk.Toplevel(root)
    home.title("YTDownloader - Home")
    home.resizable(False, False)
    home.configure(bg="#e6f0fa")

    icono = ImageTk.PhotoImage(Image.open("src/incono.ico"))
    home.iconphoto(True, icono)

    ancho, alto = 700, 650
    home.update_idletasks()
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)
    home.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Encabezado
    canvas_header = tk.Canvas(home, width=ancho, height=60, highlightthickness=0, bg="#e6f0fa")
    canvas_header.pack()
    canvas_header.create_rectangle(0, 0, ancho, 60, fill="#1976d2", outline="")

    logo_img = Image.open("src/incono.png")
    logo_img = logo_img.resize((40, 40), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    canvas_header.logo = logo

    texto = "YTDownloader"
    fuente = ("Arial", 20, "bold")
    temp = tk.Label(canvas_header, text=texto, font=fuente)
    temp.update_idletasks()
    text_width = temp.winfo_reqwidth()
    temp.destroy()
    logo_width = 40
    espacio = 10
    total_width = logo_width + espacio + text_width
    inicio_x = (ancho - total_width) // 2
    canvas_header.create_image(inicio_x + logo_width // 2, 30, image=logo)
    canvas_header.create_text(inicio_x + logo_width + espacio + text_width // 2, 30, text=texto, fill="white", font=fuente)

    # Estilo para el Notebook
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background='#e6f0fa', borderwidth=0)
    style.configure('TNotebook.Tab', background='#e6f0fa', font=('Arial', 11))
    style.map('TNotebook.Tab', background=[('selected', '#1976d2')], foreground=[('selected', 'white'), ('!selected', 'black')])

    # Frame para las pestañas
    frame_tabs = tk.Frame(home, bg="#e6f0fa")
    frame_tabs.pack(expand=True, fill="both", padx=10, pady=10)

    notebook = ttk.Notebook(frame_tabs, style='TNotebook')
    notebook.pack(expand=True, fill="both")

    # Pestaña 1: Descargar video
    tab1 = tk.Frame(notebook, bg="#e6f0fa")
    notebook.add(tab1, text="Descargar Video")

    canvas1 = tk.Canvas(tab1, width=ancho, height=50, bg="#e6f0fa", highlightthickness=0)
    canvas1.pack(pady=(30, 10), fill="x")
    canvas1.create_rectangle(0, 0, ancho, 50, fill="#1976d2", outline="#1976d2", width=2)
    canvas1.create_text(ancho // 2, 25, text="Descargar videos por enlace", fill="white", font=("Arial", 14, "bold"))

    opt1 = tk.StringVar()

    # Frame para el campo de texto y botón en una sola fila
    fila = tk.Frame(tab1, bg="#e6f0fa")
    fila.pack(fill="x", padx=30, pady=(10, 30))

    entry_link = tk.Entry(
        fila,
        textvariable=opt1,
        width=40,
        font=("Arial", 12),
        relief="solid",
        borderwidth=2,
        highlightthickness=1,
        highlightbackground="#1976d2",
        fg="#888"
    )
    entry_link.insert(0, "Ingresar el video de youtube")
    entry_link.pack(side="left", fill="x", expand=True, ipady=6)

    # Progressbar (inicialmente oculta)
    progress = ttk.Progressbar(tab1, mode="indeterminate")
    progress.pack(fill="x", padx=30, pady=(0, 10))
    progress.pack_forget()

    def on_entry_click(event):
        if entry_link.get() == "Ingresar el video de youtube":
            entry_link.delete(0, "end")
            entry_link.config(fg="black")
    def on_focusout(event):
        if entry_link.get() == "":
            entry_link.insert(0, "Ingresar el video de youtube")
            entry_link.config(fg="#888")
    entry_link.bind('<FocusIn>', on_entry_click)
    entry_link.bind('<FocusOut>', on_focusout)



    def descargar_video():
        link = opt1.get()
        print(f"Enlace ingresado: {link}")
        mostrar_ventana_descarga(link)
    btn_descargar = tk.Button(
        fila,
        text="Descargar",
        font=("Arial", 12, "bold"),
        bg="#1976d2",
        fg="white",
        activebackground="#1565c0",
        activeforeground="white",
        relief="flat",
        width=14,
        height=1,
        command=descargar_video
    )
    btn_descargar.pack(side="left", padx=(10, 0), ipady=2)

    # Espacio para información de descargas
    info_frame = tk.Frame(tab1, bg="#e6f0fa")
    info_frame.pack(fill="both", expand=True, padx=30, pady=(10, 0))

    info_label = tk.Label(
        info_frame,
        text="Aquí aparecerá la información de la descarga...",
        bg="#e6f0fa",
        fg="#1976d2",
        font=("Arial", 11, "italic"),
        anchor="nw",
        justify="left"
    )
    info_label.pack(fill="both", expand=True, anchor="nw")

    # Pestaña 2: Descargar audio
    tab2 = tk.Frame(notebook, bg="#e6f0fa")
    notebook.add(tab2, text="Descargar Audio")

    canvas2 = tk.Canvas(tab2, width=ancho, height=50, bg="#e6f0fa", highlightthickness=0)
    canvas2.pack(pady=(30, 10), fill="x")
    canvas2.create_rectangle(0, 0, ancho, 50, fill="#1976d2", outline="#1976d2", width=2)
    canvas2.create_text(ancho // 2, 25, text="Descargar audio por enlace", fill="white", font=("Arial", 14, "bold"))

    # Pestaña 3: Descargar videos de lista
    tab3 = tk.Frame(notebook, bg="#e6f0fa")
    notebook.add(tab3, text="Descargar Videos de Lista")

    canvas3 = tk.Canvas(tab3, width=ancho, height=50, bg="#e6f0fa", highlightthickness=0)
    canvas3.pack(pady=(30, 10), fill="x")
    canvas3.create_rectangle(0, 0, ancho, 50, fill="#1976d2", outline="#1976d2", width=2)
    canvas3.create_text(ancho // 2, 25, text="Descargar videos de una lista", fill="white", font=("Arial", 14, "bold"))

    # Pestaña 4: Descargar música de lista
    tab4 = tk.Frame(notebook, bg="#e6f0fa")
    notebook.add(tab4, text="Descargar Música de Lista")

    canvas4 = tk.Canvas(tab4, width=ancho, height=50, bg="#e6f0fa", highlightthickness=0)
    canvas4.pack(pady=(30, 10), fill="x")
    canvas4.create_rectangle(0, 0, ancho, 50, fill="#1976d2", outline="#1976d2", width=2)
    canvas4.create_text(ancho // 2, 25, text="Descargar música de una lista", fill="white", font=("Arial", 14, "bold"))

    home.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    mostrar_home(root)
    root.mainloop()
