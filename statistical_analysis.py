import json
from pathlib import Path
from math_operations import dividir, multiplicar, porcentaje, restar, sumar


ARCHIVO_RESULTADO = Path(__file__).parent / "resultado.json"


def cargar_resultado():
    with open(ARCHIVO_RESULTADO, encoding="utf-8") as archivo:
        return json.load(archivo)["respuesta"]


def valores_de(lista):
    return [
        float(item["value"])
        for item in lista
        if isinstance(item, dict) and item.get("value") is not None
    ]


def analizar_finanzas(datos):
    recursos = datos["liquidity_and_capital_resources"]

    deudas = recursos.get("debt_and_financing", [])
    efectivo = recursos.get("cash_and_equivalents", [])
    obligaciones = recursos.get("contractual_obligations", [])

    valores_deuda = valores_de(deudas)
    valores_efectivo = valores_de(efectivo)
    valores_obligaciones = valores_de(obligaciones)

    total_deuda = sumar(*valores_deuda)
    total_efectivo = sumar(*valores_efectivo)
    total_obligaciones = sumar(*valores_obligaciones)

    deuda_promedio = dividir(total_deuda, len(valores_deuda)) if valores_deuda else 0
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
    }


def main():
    datos = cargar_resultado()
    estadisticas = analizar_finanzas(datos)

    print("ANÁLISIS DE resultado.json")
    print(f"Deuda total: {estadisticas['total_deuda']:,.0f} millones de USD")
    print(f"Efectivo total: {estadisticas['total_efectivo']:,.0f} millones de USD")
    print(
        "Obligaciones contractuales: "
        f"{estadisticas['total_obligaciones']:,.0f} millones de USD"
    )
    print(
        "Saldo de efectivo menos deuda: "
        f"{estadisticas['saldo_efectivo_deuda']:,.0f} millones de USD"
    )
    print(f"Deuda promedio: {estadisticas['deuda_promedio']:,.0f} millones de USD")
    print(
        "Deuda con incremento del 10%: "
        f"{estadisticas['deuda_con_incremento']:,.0f} millones de USD"
    )
    print(
        "Deuda como porcentaje del efectivo: "
        f"{estadisticas['porcentaje_deuda_sobre_efectivo']:.2f}%"
    )


if __name__ == "__main__":
    main()
