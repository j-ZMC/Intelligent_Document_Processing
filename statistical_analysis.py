# Libreria stanndard para trabajar con JSONS, ya sea crearlos o modificarlos (https://docs.python.org/es/3/library/json.html)
import json
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria propia
from math_operations import dividir, multiplicar, porcentaje, restar, sumar

# Busca el ultimo json generado, ya que solo se crea uno al mismo tiempo
ARCHIVO_RESULTADO = Path(__file__).parent / "resultado.json"

# Cargar el ultimo json
def cargar_resultado():
    with open(ARCHIVO_RESULTADO, encoding="utf-8") as archivo:
        return json.load(archivo)["respuesta"]

# Saca los numeros del campo value de una lista, saltando los vacios
def valores_de(lista):
    numeros = []
    k = 0
    while k < len(lista):
        item = lista[k]
        try:
            dato = item.get("value")
        except AttributeError:
            k += 1
            continue
        if dato is None:
            k += 1
            continue
        numeros.append(float(dato))
        k += 1
    return numeros

ETIQUETAS_FILAS = ["deuda", "efectivo", "obligaciones"]


def construir_matriz_financiera(valores_deuda, valores_efectivo, valores_obligaciones):
    n = len(valores_deuda)
    if len(valores_efectivo) > n:
        n = len(valores_efectivo)
    if len(valores_obligaciones) > n:
        n = len(valores_obligaciones)
    fila_deuda = list(valores_deuda) + [0.0] * (n - len(valores_deuda))
    fila_efectivo = list(valores_efectivo) + [0.0] * (n - len(valores_efectivo))
    fila_obligaciones = list(valores_obligaciones) + [0.0] * (n - len(valores_obligaciones))
    return [fila_deuda, fila_efectivo, fila_obligaciones]


def totales_por_columna(matriz):
    if not matriz or not matriz[0]:
        return []
    totales = []
    j = 0
    while j < len(matriz[0]):
        totales.append(sumar(matriz[0][j], matriz[1][j], matriz[2][j]))
        j += 1
    return totales


def saldos_por_columna(matriz):
    if not matriz or not matriz[0]:
        return []
    saldos = []
    j = 0
    while j < len(matriz[0]):
        saldos.append(restar(matriz[1][j], matriz[0][j]))
        j += 1
    return saldos


def porcentajes_deuda_por_columna(matriz):
    if not matriz or not matriz[0]:
        return []
    porcentajes = []
    j = 0
    while j < len(matriz[0]):
        efectivo = matriz[1][j]
        deuda = matriz[0][j]
        if efectivo:
            porcentajes.append(dividir(multiplicar(deuda, 100), efectivo))
        else:
            porcentajes.append(0)
        j += 1
    return porcentajes


def estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones):
    matriz = construir_matriz_financiera(valores_deuda, valores_efectivo, valores_obligaciones)
    total_deuda = sumar(*valores_deuda) if valores_deuda else 0
    total_efectivo = sumar(*valores_efectivo) if valores_efectivo else 0
    total_obligaciones = sumar(*valores_obligaciones) if valores_obligaciones else 0
    deuda_promedio = dividir(total_deuda, len(valores_deuda)) if valores_deuda else 0
    efectivo_promedio = dividir(total_efectivo, len(valores_efectivo)) if valores_efectivo else 0
    obligaciones_promedio = dividir(total_obligaciones, len(valores_obligaciones)) if valores_obligaciones else 0
    deuda_con_incremento = sumar(total_deuda, porcentaje(total_deuda, 10))
    saldo_efectivo_deuda = restar(total_efectivo, total_deuda)
    porcentaje_deuda_sobre_efectivo = (
        dividir(multiplicar(total_deuda, 100), total_efectivo)
        if total_efectivo
        else 0
    )
    return {
        "total_deuda": total_deuda,
        "total_efectivo": total_efectivo,
        "total_obligaciones": total_obligaciones,
        "deuda_promedio": deuda_promedio,
        "deuda_con_incremento": deuda_con_incremento,
        "saldo_efectivo_deuda": saldo_efectivo_deuda,
        "porcentaje_deuda_sobre_efectivo": porcentaje_deuda_sobre_efectivo,
        "matriz": matriz,
        "etiquetas_filas": list(ETIQUETAS_FILAS),
        "totales_por_fila": [total_deuda, total_efectivo, total_obligaciones],
        "totales_por_columna": totales_por_columna(matriz),
        "promedios_por_fila": [deuda_promedio, efectivo_promedio, obligaciones_promedio],
        "saldos_por_columna": saldos_por_columna(matriz),
        "porcentajes_deuda_por_columna": porcentajes_deuda_por_columna(matriz),
    }

# Funcion para obtener los datos y calcularlos para las graficas
def analizar_finanzas(datos):
    recursos = datos["liquidity_and_capital_resources"]

    deudas = recursos.get("debt_and_financing", [])
    efectivo = recursos.get("cash_and_equivalents", [])
    obligaciones = recursos.get("contractual_obligations", [])

    valores_deuda = valores_de(deudas)
    valores_efectivo = valores_de(efectivo)
    valores_obligaciones = valores_de(obligaciones)

    return estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones)

# Crea texto para los datos calculados
def texto_analisis(estadisticas):
    lineas = [
        "ANÁLISIS DE resultado.json",
        f"Deuda total: {estadisticas['total_deuda']:,.0f} millones de USD",
        f"Efectivo total: {estadisticas['total_efectivo']:,.0f} millones de USD",
        "Obligaciones contractuales: "
        f"{estadisticas['total_obligaciones']:,.0f} millones de USD",
        "Saldo de efectivo menos deuda: "
        f"{estadisticas['saldo_efectivo_deuda']:,.0f} millones de USD",
        f"Deuda promedio: {estadisticas['deuda_promedio']:,.0f} millones de USD",
        "Deuda con incremento del 10%: "
        f"{estadisticas['deuda_con_incremento']:,.0f} millones de USD",
        "Deuda como porcentaje del efectivo: "
        f"{estadisticas['porcentaje_deuda_sobre_efectivo']:.2f}%",
    ]
    return "\n".join(lineas)

# Lo mismo que analizar_finanzas pero con whiles.
def analizar_values(datos):
    LIST_VALUES = list(datos.keys())
    i = 0
    recursos = {}
    while i < len(LIST_VALUES):
        if LIST_VALUES[i] == "liquidity_and_capital_resources":
            recursos = datos[LIST_VALUES[i]]
        i += 1
    VALUES = list(recursos.keys())
    j = 0
    deudas = []
    efectivo = []
    obligaciones = []
    while j < len(VALUES):
        if VALUES[j] == "debt_and_financing":
            deudas = recursos[VALUES[j]]
        elif VALUES[j] == "cash_and_equivalents":
            efectivo = recursos[VALUES[j]]
        elif VALUES[j] == "contractual_obligations":
            obligaciones = recursos[VALUES[j]]
        j += 1
    valores_deuda = valores_de(deudas)
    valores_efectivo = valores_de(efectivo)
    valores_obligaciones = valores_de(obligaciones)
    return estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones)


# Es la funcion principal para ejecutar la prueba
def main():
    datos = cargar_resultado()
    estadisticas = analizar_finanzas(datos)
    print(texto_analisis(estadisticas))

# Ejecuta la prueba
if __name__ == "__main__":
    #datos = cargar_resultado()
    #analizar_values(datos)
    main()
