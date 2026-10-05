# Libreria para ejecutar tareas en segundo plano (https://docs.python.org/es/3/library/threading.html)
import threading
# Libreria de interfaz grafica (https://customtkinter.tomschimansky.com/)
import customtkinter as ctk
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria local para la ventana de resultados (graphical_interface/results.py)
from graphical_interface.results import pagina_resultados
# Libreria standard para importar el descargador 10-K (empieza con numero y no admite import directo)
import importlib


modulo_descarga = importlib.import_module("10k_download")
BASE = Path(__file__).resolve().parent.parent / "company_report"


def en_fondo(tarea):
    threading.Thread(target=tarea, daemon=True).start()


def obtener_tickers():
    tickers = sorted(p.name.upper() for p in BASE.iterdir() if p.is_dir()) if BASE.is_dir() else []
    return tickers or ["Sin descargas"]


def obtener_anos(ticker):
    anos = sorted(a.stem.rsplit("_", 1)[-1] for a in (BASE / ticker).glob(f"{ticker}_*.md") if a.stem.rsplit("_", 1)[-1].isdigit())
    return anos or ["Sin años"]


def descargar(ticket, anos, mensaje, boton):
    ticket = ticket.strip().upper()
    if ticket == "":
        mensaje.configure(text="Escribe un ticker, por ejemplo AAPL.")
        return
    if not anos.isdigit() or int(anos) <= 0:
        mensaje.configure(text="La cantidad de años debe ser mayor a 0.")
        return
    boton.configure(state="disabled")
    mensaje.configure(text=f"Descargando {ticket} con {anos} año(s)...")

    def trabajo():
        try:
            modulo_descarga.ticket_year(ticket, int(anos))
            mensaje.after(0, lambda: mensaje.configure(text=f"Descarga terminada: {ticket} con {anos} año(s)."))
        except Exception as error:
            detalle = str(error)
            mensaje.after(0, lambda detalle=detalle: mensaje.configure(text=f"Error al descargar: {detalle}"))
        mensaje.after(0, lambda: boton.configure(state="normal"))

    en_fondo(trabajo)


def graficar(root, current_frame, menu_ticker, menu_ano, mensaje):
    ticker = menu_ticker.get()
    ano = menu_ano.get()
    if ticker == "Sin descargas" or ano == "Sin años":
        mensaje.configure(text="Primero descarga reportes o actualiza la lista.")
        return
    pagina_resultados(root, current_frame, ticker, ano, pagina_principal)


def cambiar_anos(opcion, menu_ano):
    menu_ano.configure(values=obtener_anos(opcion))
    menu_ano.set(obtener_anos(opcion)[0])


def actualizar_lista(menu_ticker, menu_ano, mensaje):
    menu_ticker.configure(values=obtener_tickers())
    menu_ticker.set(obtener_tickers()[0])
    cambiar_anos(menu_ticker.get(), menu_ano)
    mensaje.configure(text="Lista actualizada.")


def pagina_principal(root, current_frame):
    current_frame.destroy()
    new_frame = ctk.CTkFrame(master=root)
    new_frame.pack(pady=40, padx=40, fill="both", expand=True)

    new_frame.grid_columnconfigure(0, weight=1)
    new_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(master=new_frame,
                 text="Intelligent Document Processing",
                 font=("Arial", 36, "bold")).grid(row=0, column=0, columnspan=2, pady=(40, 20))

    ctk.CTkLabel(master=new_frame,
                 text="Descargar 10-K",
                 font=("Arial", 24, "bold")).grid(row=1, column=0, columnspan=2, pady=(20, 10))

    ctk.CTkLabel(master=new_frame, text="Ticker:", font=("Arial", 20, "bold")).grid(row=2, column=0, pady=10, padx=10, sticky="e")
    entry_ticket = ctk.CTkEntry(master=new_frame, placeholder_text="Ej. AAPL")
    entry_ticket.grid(row=2, column=1, pady=10, padx=10, sticky="w")

    ctk.CTkLabel(master=new_frame, text="Cantidad de años:", font=("Arial", 20, "bold")).grid(row=3, column=0, pady=10, padx=10, sticky="e")
    entry_anos = ctk.CTkEntry(master=new_frame, placeholder_text="Ej. 8")
    entry_anos.grid(row=3, column=1, pady=10, padx=10, sticky="w")

    boton_descargar = ctk.CTkButton(new_frame, text="Descargar",
                                    command=lambda: descargar(entry_ticket.get(), entry_anos.get(), label_mensaje, boton_descargar),
                                    fg_color="blue", hover_color="darkblue", width=200, height=50, font=("Arial", 20))
    boton_descargar.grid(row=4, column=0, columnspan=2, pady=20)

    ctk.CTkLabel(master=new_frame,
                 text="Graficar 10-K descargado",
                 font=("Arial", 24, "bold")).grid(row=5, column=0, columnspan=2, pady=(20, 10))

    ctk.CTkLabel(master=new_frame, text="Ticker:", font=("Arial", 20, "bold")).grid(row=6, column=0, pady=10, padx=10, sticky="e")
    menu_ticker = ctk.CTkOptionMenu(master=new_frame, values=obtener_tickers(),
                                    command=lambda x: cambiar_anos(x, menu_ano))
    menu_ticker.grid(row=6, column=1, pady=10, padx=10, sticky="w")

    ctk.CTkLabel(master=new_frame, text="Año:", font=("Arial", 20, "bold")).grid(row=7, column=0, pady=10, padx=10, sticky="e")
    menu_ano = ctk.CTkOptionMenu(master=new_frame, values=obtener_anos(menu_ticker.get()))
    menu_ano.grid(row=7, column=1, pady=10, padx=10, sticky="w")

    ctk.CTkButton(new_frame, text="Actualizar lista",
                  command=lambda: actualizar_lista(menu_ticker, menu_ano, label_mensaje),
                  fg_color="green", hover_color="darkgreen", width=200, height=50, font=("Arial", 20)).grid(row=8, column=0, pady=20, padx=10)

    ctk.CTkButton(new_frame, text="Graficar y analizar",
                  command=lambda: graficar(root, new_frame, menu_ticker, menu_ano, label_mensaje),
                  fg_color="green", hover_color="darkgreen", width=200, height=50, font=("Arial", 20)).grid(row=8, column=1, pady=20, padx=10)

    label_mensaje = ctk.CTkLabel(master=new_frame, text="Listo.", font=("Arial", 16, "bold"), text_color="white")
    label_mensaje.grid(row=9, column=0, columnspan=2, pady=(10, 40))
