[1mdiff --git a/statistical_analysis.py b/statistical_analysis.py[m
[1mindex 58ded31..ed53194 100644[m
[1m--- a/statistical_analysis.py[m
[1m+++ b/statistical_analysis.py[m
[36m@@ -31,23 +31,67 @@[m [mdef valores_de(lista):[m
         k += 1[m
     return numeros[m
 [m
[31m-# Funcion para obtener los datos y calcularlos para las graficas[m
[31m-def analizar_finanzas(datos):[m
[31m-    recursos = datos["liquidity_and_capital_resources"][m
[32m+[m[32mETIQUETAS_FILAS = ["deuda", "efectivo", "obligaciones"][m
 [m
[31m-    deudas = recursos.get("debt_and_financing", [])[m
[31m-    efectivo = recursos.get("cash_and_equivalents", [])[m
[31m-    obligaciones = recursos.get("contractual_obligations", [])[m
 [m
[31m-    valores_deuda = valores_de(deudas)[m
[31m-    valores_efectivo = valores_de(efectivo)[m
[31m-    valores_obligaciones = valores_de(obligaciones)[m
[32m+[m[32mdef construir_matriz_financiera(valores_deuda, valores_efectivo, valores_obligaciones):[m
[32m+[m[32m    n = len(valores_deuda)[m
[32m+[m[32m    if len(valores_efectivo) > n:[m
[32m+[m[32m        n = len(valores_efectivo)[m
[32m+[m[32m    if len(valores_obligaciones) > n:[m
[32m+[m[32m        n = len(valores_obligaciones)[m
[32m+[m[32m    fila_deuda = list(valores_deuda) + [0.0] * (n - len(valores_deuda))[m
[32m+[m[32m    fila_efectivo = list(valores_efectivo) + [0.0] * (n - len(valores_efectivo))[m
[32m+[m[32m    fila_obligaciones = list(valores_obligaciones) + [0.0] * (n - len(valores_obligaciones))[m
[32m+[m[32m    return [fila_deuda, fila_efectivo, fila_obligaciones][m
[32m+[m
[32m+[m
[32m+[m[32mdef totales_por_columna(matriz):[m
[32m+[m[32m    if not matriz or not matriz[0]:[m
[32m+[m[32m        return [][m
[32m+[m[32m    totales = [][m
[32m+[m[32m    j = 0[m
[32m+[m[32m    while j < len(matriz[0]):[m
[32m+[m[32m        totales.append(sumar(matriz[0][j], matriz[1][j], matriz[2][j]))[m
[32m+[m[32m        j += 1[m
[32m+[m[32m    return totales[m
 [m
[31m-    total_deuda = sumar(*valores_deuda)[m
[31m-    total_efectivo = sumar(*valores_efectivo)[m
[31m-    total_obligaciones = sumar(*valores_obligaciones)[m
 [m
[32m+[m[32mdef saldos_por_columna(matriz):[m
[32m+[m[32m    if not matriz or not matriz[0]:[m
[32m+[m[32m        return [][m
[32m+[m[32m    saldos = [][m
[32m+[m[32m    j = 0[m
[32m+[m[32m    while j < len(matriz[0]):[m
[32m+[m[32m        saldos.append(restar(matriz[1][j], matriz[0][j]))[m
[32m+[m[32m        j += 1[m
[32m+[m[32m    return saldos[m
[32m+[m
[32m+[m
[32m+[m[32mdef porcentajes_deuda_por_columna(matriz):[m
[32m+[m[32m    if not matriz or not matriz[0]:[m
[32m+[m[32m        return [][m
[32m+[m[32m    porcentajes = [][m
[32m+[m[32m    j = 0[m
[32m+[m[32m    while j < len(matriz[0]):[m
[32m+[m[32m        efectivo = matriz[1][j][m
[32m+[m[32m        deuda = matriz[0][j][m
[32m+[m[32m        if efectivo:[m
[32m+[m[32m            porcentajes.append(dividir(multiplicar(deuda, 100), efectivo))[m
[32m+[m[32m        else:[m
[32m+[m[32m            porcentajes.append(0)[m
[32m+[m[32m        j += 1[m
[32m+[m[32m    return porcentajes[m
[32m+[m
[32m+[m
[32m+[m[32mdef estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones):[m
[32m+[m[32m    matriz = construir_matriz_financiera(valores_deuda, valores_efectivo, valores_obligaciones)[m
[32m+[m[32m    total_deuda = sumar(*valores_deuda) if valores_deuda else 0[m
[32m+[m[32m    total_efectivo = sumar(*valores_efectivo) if valores_efectivo else 0[m
[32m+[m[32m    total_obligaciones = sumar(*valores_obligaciones) if valores_obligaciones else 0[m
     deuda_promedio = dividir(total_deuda, len(valores_deuda)) if valores_deuda else 0[m
[32m+[m[32m    efectivo_promedio = dividir(total_efectivo, len(valores_efectivo)) if valores_efectivo else 0[m
[32m+[m[32m    obligaciones_promedio = dividir(total_obligaciones, len(valores_obligaciones)) if valores_obligaciones else 0[m
     deuda_con_incremento = sumar(total_deuda, porcentaje(total_deuda, 10))[m
     saldo_efectivo_deuda = restar(total_efectivo, total_deuda)[m
     porcentaje_deuda_sobre_efectivo = ([m
[36m@@ -55,7 +99,6 @@[m [mdef analizar_finanzas(datos):[m
         if total_efectivo[m
         else 0[m
     )[m
[31m-[m
     return {[m
         "total_deuda": total_deuda,[m
         "total_efectivo": total_efectivo,[m
[36m@@ -64,8 +107,29 @@[m [mdef analizar_finanzas(datos):[m
         "deuda_con_incremento": deuda_con_incremento,[m
         "saldo_efectivo_deuda": saldo_efectivo_deuda,[m
         "porcentaje_deuda_sobre_efectivo": porcentaje_deuda_sobre_efectivo,[m
[32m+[m[32m        "matriz": matriz,[m
[32m+[m[32m        "etiquetas_filas": list(ETIQUETAS_FILAS),[m
[32m+[m[32m        "totales_por_fila": [total_deuda, total_efectivo, total_obligaciones],[m
[32m+[m[32m        "totales_por_columna": totales_por_columna(matriz),[m
[32m+[m[32m        "promedios_por_fila": [deuda_promedio, efectivo_promedio, obligaciones_promedio],[m
[32m+[m[32m        "saldos_por_columna": saldos_por_columna(matriz),[m
[32m+[m[32m        "porcentajes_deuda_por_columna": porcentajes_deuda_por_columna(matriz),[m
     }[m
 [m
[32m+[m[32m# Funcion para obtener los datos y calcularlos para las graficas[m
[32m+[m[32mdef analizar_finanzas(datos):[m
[32m+[m[32m    recursos = datos["liquidity_and_capital_resources"][m
[32m+[m
[32m+[m[32m    deudas = recursos.get("debt_and_financing", [])[m
[32m+[m[32m    efectivo = recursos.get("cash_and_equivalents", [])[m
[32m+[m[32m    obligaciones = recursos.get("contractual_obligations", [])[m
[32m+[m
[32m+[m[32m    valores_deuda = valores_de(deudas)[m
[32m+[m[32m    valores_efectivo = valores_de(efectivo)[m
[32m+[m[32m    valores_obligaciones = valores_de(obligaciones)[m
[32m+[m
[32m+[m[32m    return estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones)[m
[32m+[m
 # Crea texto para los datos calculados[m
 def texto_analisis(estadisticas):[m
     lineas = [[m
[36m@@ -109,26 +173,7 @@[m [mdef analizar_values(datos):[m
     valores_deuda = valores_de(deudas)[m
     valores_efectivo = valores_de(efectivo)[m
     valores_obligaciones = valores_de(obligaciones)[m
[31m-    total_deuda = sumar(*valores_deuda)[m
[31m-    total_efectivo = sumar(*valores_efectivo)[m
[31m-    total_obligaciones = sumar(*valores_obligaciones)[m
[31m-    deuda_promedio = dividir(total_deuda, len(valores_deuda)) if valores_deuda else 0[m
[31m-    deuda_con_incremento = sumar(total_deuda, porcentaje(total_deuda, 10))[m
[31m-    saldo_efectivo_deuda = restar(total_efectivo, total_deuda)[m
[31m-    porcentaje_deuda_sobre_efectivo = ([m
[31m-        dividir(multiplicar(total_deuda, 100), total_efectivo)[m
[31m-        if total_efectivo[m
[31m-        else 0[m
[31m-    )[m
[31m-    return {[m
[31m-        "total_deuda": total_deuda,[m
[31m-        "total_efectivo": total_efectivo,[m
[31m-        "total_obligaciones": total_obligaciones,[m
[31m-        "deuda_promedio": deuda_promedio,[m
[31m-        "deuda_con_incremento": deuda_con_incremento,[m
[31m-        "saldo_efectivo_deuda": saldo_efectivo_deuda,[m
[31m-        "porcentaje_deuda_sobre_efectivo": porcentaje_deuda_sobre_efectivo,[m
[31m-    }[m
[32m+[m[32m    return estadisticas_desde_vectores(valores_deuda, valores_efectivo, valores_obligaciones)[m
 [m
 [m
 # Es la funcion principal para ejecutar la prueba[m
