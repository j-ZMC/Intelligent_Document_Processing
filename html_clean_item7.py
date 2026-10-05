# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria para extraer texto de HTML (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
from bs4 import BeautifulSoup
# Libreria standard para expresiones regulares (https://docs.python.org/es/3/library/re.html)
import re


# Carpeta donde se guardan los reportes 10-K descargados
BASE = Path(__file__).resolve().parent / "company_report"


# Extrae solo el texto del Item 7 de un HTML, regresa None si no lo encuentra
def extraer_item7_limpio(html_path):
    archivo = open(html_path, encoding="utf-8")
    soup = BeautifulSoup(archivo, "xml")
    archivo.close()
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    # Junta todos los espacios y saltos de linea en un solo espacio (https://docs.python.org/es/3/library/re.html#re.sub)
    texto = re.sub(r"\s+", " ", soup.get_text(" "))
    inicios = []
    for m in re.finditer(r"ITEM 7\.", texto, re.IGNORECASE):
        if "ITEM 7A" not in texto[m.start():m.start() + 8].upper():
            inicios.append(m.start())
    fines = []
    for m in re.finditer(r"ITEM 7A\.", texto, re.IGNORECASE):
        fines.append(m.start())
    if len(inicios) == 0 or len(fines) == 0:
        return None
    inicio = inicios[-1]
    fin = None
    for punto in fines:
        if punto > inicio:
            fin = punto
            break
    if fin is None:
        return None
    pedazo = texto[inicio:fin]
    return pedazo.strip()


# Busca el HTML descargado de un ticker y un año, marca error si no existe
def encontrar_html_descargado(ticket, ano):
    ticket = ticket.upper()
    carpeta = BASE / ticket
    archivos = sorted(carpeta.glob(ticket + "_" + str(ano) + ".htm*"))
    if len(archivos) == 0:
        raise FileNotFoundError("No se encontró " + ticket + "_" + str(ano) + ".htm/html")
    return archivos[0]

# Ejecuta la prueba
if __name__ == "__main__":
    html_file = encontrar_html_descargado("AAPL", "2018")
    item7 = extraer_item7_limpio(html_file)
    salida = html_file.parent / "item_7_clean.txt"
    salida.write_text(item7, encoding="utf-8")
    palabras = item7.split()
    print("Palabras aproximadas: " + str(len(palabras)))
