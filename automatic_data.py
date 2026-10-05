# Libreria stanndard para trabajar con JSONS (https://docs.python.org/es/3/library/json.html)
import json
# Libreria standard para expresiones regulares (https://docs.python.org/es/3/library/re.html)
import re
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria para graficar (https://matplotlib.org/)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Carpeta base del proyecto
BASE = Path(__file__).parent
# Ruta del json generado por el LLM, se sobrescribe en cada analisis
JSON = BASE / "resultado.json"
# Carpeta donde se guardan las graficas PNG
GRAFICAS = BASE / "graficas"


# Saca el nombre del dato buscando en varios campos posibles
def etiqueta(item):
    if item.get("name"):
        return str(item.get("name"))
    if item.get("description"):
        return str(item.get("description"))
    if item.get("label"):
        return str(item.get("label"))
    return "Dato"


# Saca el numero del dato buscando en varios campos posibles, saltando los vacios
def valor(item):
    claves = ["value", "amount", "total", "net_sales", "operating_income"]
    for clave in claves:
        dato = item.get(clave)
        if dato is None:
            continue
        try:
            numero = float(dato)
        except (TypeError, ValueError):
            continue
        return numero
    return None


# Crea una grafica de barras y la guarda como PNG
def crear_grafica(nombre, datos):
    etiquetas = []
    valores = []
    for par in datos:
        etiquetas.append(par[0])
        valores.append(par[1])
    ancho = len(etiquetas) * 1.25
    if ancho < 9:
        ancho = 9
    plt.figure(figsize=(ancho, 6))
    barras = plt.bar(etiquetas, valores, color="#1685e0")
    titulo = nombre.replace("_", " ")
    titulo = titulo.capitalize()
    plt.title(titulo)
    plt.ylabel("Valor (millones de USD)")
    plt.xticks(rotation=35)
    plt.grid(axis="y", alpha=0.25)
    indice = 0
    for barra in barras:
        numero = valores[indice]
        x = barra.get_x() + barra.get_width() / 2
        texto = "{:,.0f}".format(numero)
        plt.text(x, numero, texto, ha="center", va="bottom")
        indice = indice + 1
    plt.tight_layout()
    # Cambia todo lo que no sea letra, numero o _ por un _ (https://docs.python.org/es/3/library/re.html#re.sub)
    nombre_archivo = re.sub(r"[^\w]+", "_", nombre)
    ruta = GRAFICAS / (nombre_archivo + ".png")
    plt.savefig(ruta, dpi=100)
    plt.close()


# Grafica las listas del json que tengan numeros y regresa la carpeta
def graficar_resultado():
    texto = JSON.read_text(encoding="utf-8")
    datos = json.loads(texto)["respuesta"]
    financieros = datos["financial_results"]
    recursos = datos["liquidity_and_capital_resources"]
    nombres = ["metrics", "segments", "cash_and_equivalents", "debt_and_financing", "contractual_obligations"]
    listas = []
    listas.append(financieros.get("metrics", []))
    listas.append(financieros.get("segments", []))
    listas.append(recursos.get("cash_and_equivalents", []))
    listas.append(recursos.get("debt_and_financing", []))
    listas.append(recursos.get("contractual_obligations", []))
    GRAFICAS.mkdir(exist_ok=True)
    i = 0
    for lista in listas:
        nombre = nombres[i]
        pares = []
        for item in lista:
            if not isinstance(item, dict):
                continue
            numero = valor(item)
            if numero is None:
                continue
            nombre_dato = etiqueta(item)
            pares.append((nombre_dato, numero))
        if len(pares) > 0:
            crear_grafica(nombre, pares)
        i = i + 1
    print("Graficas guardadas en: " + str(GRAFICAS))
    return GRAFICAS

# Ejecuta la prueba
if __name__ == "__main__":
    graficar_resultado()
