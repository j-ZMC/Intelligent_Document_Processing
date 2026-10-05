# Libreria para ejecutar tareas en segundo plano (https://docs.python.org/es/3/library/threading.html)
import threading
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria de interfaz grafica (https://customtkinter.tomschimansky.com/)
import customtkinter as ctk
# Libreria para mostrar imagenes PNG (https://pillow.readthedocs.io/)
from PIL import Image
# Libreria local para graficar el JSON (automatic_data.py)
from automatic_data import graficar_resultado
# Libreria local para extraer el Item 7 (html_clean_item7.py)
from html_clean_item7 import encontrar_html_descargado, extraer_item7_limpio
# Libreria local para consultar al LLM (llm_to_json.py)
from llm_to_json import procesar_archivo_item7
# Libreria local para el analisis estadistico (statistical_analysis.py)
from statistical_analysis import analizar_finanzas, cargar_resultado, texto_analisis


def pagina_resultados(root, current_frame, ticker, ano, volver):
    current_frame.destroy()
    new_frame = ctk.CTkFrame(root)
    new_frame.pack(pady=40, padx=40, fill="both", expand=True)

    ctk.CTkLabel(new_frame, text=f"Resultados {ticker} {ano}",
                 font=("Arial", 32, "bold")).pack(pady=(30, 10))

    estado = ctk.CTkLabel(new_frame, text="Documento procesando... (Puede Tardar Unos Minutos)",
                          font=("Arial", 20, "bold"))
    estado.pack(pady=(10, 20))

    contenedor = ctk.CTkScrollableFrame(new_frame)
    contenedor.pack(pady=10, padx=40, fill="both", expand=True)

    boton_volver = ctk.CTkButton(new_frame, text="Volver",
                                 command=lambda: volver(root, new_frame),
                                 fg_color="gray", hover_color="dimgray",
                                 width=200, height=45, font=("Arial", 18))
    boton_volver.pack(pady=(10, 30))
    boton_volver.configure(state="disabled")

    def avisar(texto):
        estado.configure(text=texto)
        boton_volver.configure(state="normal")

    def mostrar_graficas(carpeta):
        for ruta in sorted(Path(carpeta).glob("*.png")):
            ctk.CTkLabel(contenedor, text=ruta.stem.replace("_", " ").capitalize(),
                         font=("Arial", 18, "bold")).pack(pady=(15, 5))
            imagen = ctk.CTkImage(light_image=Image.open(ruta), size=(900, 600))
            visor = ctk.CTkLabel(contenedor, text="", image=imagen)
            visor.image = imagen
            visor.pack(pady=5)
        if not list(Path(carpeta).glob("*.png")):
            ctk.CTkLabel(contenedor, text="No se generaron gráficas.",
                         font=("Arial", 16)).pack(pady=20)

    def terminar_ok(carpeta, texto):
        ctk.CTkLabel(contenedor, text=texto,
                     font=("Arial", 14), justify="left").pack(pady=(0, 15))
        try:
            mostrar_graficas(carpeta)
            new_frame.after(0, lambda: avisar("Gráficas listas."))
        except Exception as error:
            new_frame.after(0, lambda: avisar(f"Error al mostrar gráficas: {error}"))

    def terminar_error(detalle):
        new_frame.after(0, lambda: avisar(f"Error al graficar: {detalle}"))

    def trabajo():
        try:
            html_file = encontrar_html_descargado(ticker, ano)
            item7 = extraer_item7_limpio(html_file)
            if not item7:
                raise ValueError("No se encontró el Item 7 en ese reporte.")
            (html_file.parent / "item_7_clean.txt").write_text(item7, encoding="utf-8")
            procesar_archivo_item7(html_file.parent / "item_7_clean.txt")
            texto = texto_analisis(analizar_finanzas(cargar_resultado()))
            carpeta = graficar_resultado()
        except Exception as error:
            terminar_error(str(error))
        else:
            new_frame.after(0, lambda: terminar_ok(carpeta, texto))

    threading.Thread(target=trabajo, daemon=True).start()
