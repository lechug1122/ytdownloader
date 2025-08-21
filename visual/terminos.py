import tkinter as tk
import sys
from PIL import Image, ImageTk

def mostrar_terminos():
    terminos = tk.Tk()
    terminos.title("Términos y Condiciones")
    terminos.resizable(False, False)

    # Ícono de la ventana (ajusta la ruta si es necesario)
    icono = ImageTk.PhotoImage(Image.open("src/incono.ico"))
    terminos.iconphoto(True, icono)

    ancho, alto = 500, 450
    screen_width = terminos.winfo_screenwidth()
    screen_height = terminos.winfo_screenheight()
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)
    terminos.geometry(f"{ancho}x{alto}+{x}+{y}")

    texto_terminos = """Términos y Condiciones de Uso – YTDownloader
Última actualización: [12 de junio de 2025]

Bienvenido a YTDownloader. Al utilizar este software, usted acepta los siguientes términos y condiciones. Si no está de acuerdo con estos términos, no debe utilizar el programa.

1. Descripción del software
YTDownloader es una herramienta destinada a facilitar la descarga de contenido multimedia disponible públicamente desde plataformas en línea. Su propósito es exclusivamente educativo, personal y legal.

2. Uso legal
El usuario se compromete a utilizar YTDownloader únicamente para fines legales y de acuerdo con todas las leyes, normativas y regulaciones locales, nacionales e internacionales aplicables.

3. Propiedad intelectual y derechos de autor
YTDownloader no promueve ni aprueba la descarga de contenido protegido por derechos de autor sin la debida autorización de los titulares correspondientes. El software está diseñado para permitir la descarga de contenido libre o con permisos expresos del propietario.

El usuario es el único responsable del uso que haga del programa y de asegurarse de no infringir derechos de autor u otras leyes relacionadas con propiedad intelectual.

4. Exclusión de responsabilidad
YTDownloader y sus desarrolladores no se hacen responsables de:

El uso indebido del software por parte de los usuarios.
La descarga, distribución o modificación de contenido protegido por derechos de autor.
Cualquier daño o consecuencia legal derivada del uso del programa.

El uso del software es bajo su propio riesgo.

5. Licencia de uso
YTDownloader se proporciona "tal cual", sin garantías de ningún tipo, ya sean expresas o implícitas. El usuario no adquiere ningún derecho sobre el contenido descargado mediante el uso del programa.

6. Modificaciones y actualizaciones
Nos reservamos el derecho de modificar estos Términos y Condiciones en cualquier momento. Las actualizaciones serán notificadas a través del sitio web oficial o el canal de distribución del software. El uso continuado del programa después de dichas actualizaciones constituye la aceptación de los nuevos términos.

7. Ley aplicable
Estos Términos se regirán e interpretarán de acuerdo con las leyes del país en el que se distribuye legalmente el software. Cualquier disputa derivada de estos términos será resuelta por los tribunales competentes.
"""

    frame_texto = tk.Frame(terminos)
    frame_texto.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame_texto)
    scrollbar.pack(side="right", fill="y")

    texto = tk.Text(frame_texto, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10))
    texto.insert("1.0", texto_terminos)
    texto.config(state="disabled")
    texto.pack(expand=True, fill="both")
    scrollbar.config(command=texto.yview)

    frame_botones = tk.Frame(terminos)
    frame_botones.pack(pady=10)

    def aceptar():
        terminos.destroy()

    def no_aceptar():
        terminos.destroy()
        sys.exit(0)

    btn_aceptar = tk.Button(frame_botones, text="Aceptar", width=12, command=aceptar)
    btn_aceptar.pack(side="left", padx=10)

    btn_no = tk.Button(frame_botones, text="No aceptar", width=12, command=no_aceptar)
    btn_no.pack(side="right", padx=10)

    terminos.protocol("WM_DELETE_WINDOW", no_aceptar)
    terminos.mainloop()