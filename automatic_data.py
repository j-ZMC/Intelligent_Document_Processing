# Libreria stanndard para trabajar con JSONS (https://docs.python.org/es/3/library/json.html)
import json
# Libreria standard para expresiones regulares (https://docs.python.org/es/3/library/re.html)
import re
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria para graficar (https://plotly.com/python/)
import plotly.express as px


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


# Agrega el periodo a la etiqueta para no juntar distintos valores en la misma barra
def etiqueta_con_periodo(item, base):
    periodo = item.get("period")
    if periodo is None:
        return base
    return f"{base} ({periodo})"


# Saca uno o varios pares (etiqueta, numero) de cada item
def extraer_pares(lista):
    pares = []
    for item in lista:
        if not isinstance(item, dict):
            continue
        base = etiqueta(item)
        numero = valor(item)
        if numero is not None:
            pares.append((etiqueta_con_periodo(item, base), numero))
            continue
        for clave, dato in item.items():
            if clave in ("name", "description", "label", "unit", "currency", "period", "source_excerpt"):
                continue
            try:
                numero = float(dato)
            except (TypeError, ValueError):
                continue
            pares.append((etiqueta_con_periodo(item, f"{base} {clave}"), numero))
    return pares


# Crea una grafica de barras y la guarda como PNG
def crear_grafica(nombre, datos):
    etiquetas = []
    valores = []
    for par in datos:
        etiquetas.append(par[0])
        valores.append(par[1])
    ancho = len(etiquetas) * 200
    if ancho < 900:
        ancho = 900
    if ancho > 2400:
        ancho = 2400
    textos = ["{:,.0f}".format(numero) for numero in valores]
    titulo = nombre.replace("_", " ")
    titulo = titulo.capitalize()
    maximo = max(valores)
    minimo = min(valores)
    if minimo < 0:
        limite_superior = maximo * 1.2 if maximo > 0 else maximo * 0.8
        limite_inferior = minimo * 1.2
    else:
        limite_superior = maximo * 1.2
        limite_inferior = 0
    figura = px.bar(
        x=etiquetas,
        y=valores,
        text=textos,
        color_discrete_sequence=["#1685e0"],
    )
    figura.update_traces(textposition="outside", cliponaxis=False)
    figura.update_layout(
        title=titulo,
        yaxis_title="Valor (millones de USD)",
        width=ancho,
        height=700,
        bargap=0.35,
        xaxis_tickangle=-25,
        xaxis_tickfont=dict(size=11),
        xaxis_automargin=True,
        yaxis_range=[limite_inferior, limite_superior],
        yaxis_griddash="dot",
        yaxis_gridcolor="rgba(0, 0, 0, 0.25)",
        margin=dict(l=60, r=30, t=100, b=220),
    )
    # Cambia todo lo que no sea letra, numero o _ por un _ (https://docs.python.org/es/3/library/re.html#re.sub)
    nombre_archivo = re.sub(r"[^\w]+", "_", nombre)
    ruta = GRAFICAS / (nombre_archivo + ".png")
    figura.write_image(str(ruta))


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
        pares = extraer_pares(lista)
        if len(pares) > 0:
            crear_grafica(nombre, pares)
        i = i + 1
    print("Graficas guardadas en: " + str(GRAFICAS))
    return GRAFICAS

# Ejecuta la prueba
if __name__ == "__main__":
    graficar_resultado()
