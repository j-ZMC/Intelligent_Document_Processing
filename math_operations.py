def sumar(*valores):
    return sum(valores)


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b


def porcentaje(valor, porcentaje_a_calcular):
    return valor * porcentaje_a_calcular / 100


def calcular_beneficio(ingresos, gastos):
    return restar(ingresos, gastos)


if __name__ == "__main__":
    resultado = calcular_beneficio(1500, 900)
    print(resultado)
