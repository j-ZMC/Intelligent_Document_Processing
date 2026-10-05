# Libreria Standard para uso de moldelos de LLM  (https://developers.openai.com/api/reference/python)
from openai import OpenAI
# Libreria standard Python para organizar archivos (https://docs.python.org/es/3/library/pathlib.html)
from pathlib import Path
# Libreria stanndard para trabajar con JSONS, ya sea crearlos o modificarlos (https://docs.python.org/es/3/library/json.html)
import json
# Libreria standard para para acceder al sistema operativo: https://docs.python.org/3/library/os.html
import os

from dotenv import load_dotenv

load_dotenv()

# Direccion del 10-k usado para la prueba
BASE_DIR = Path(__file__).parent
file_path = (
    BASE_DIR
    / "company_report"
    / "AAPL"
    / "2025"
    / "sec-edgar-filings"
    / "AAPL"
    / "10-K"
    / "0000320193-25-000079"
    / "item_7_clean.txt"
)

# Instrucciones para el modelo LLM y que lo guarde en JSON
instructions = """
Analiza exclusivamente el contenido del Item 7 de un informe anual 10-K:
Management's Discussion and Analysis of Financial Condition and Results of Operations.

Devuelve exclusivamente un objeto JSON valido, sin markdown ni texto fuera del JSON,
con esta estructura exacta:
{
    "document": {
        "company_name": null,
        "ticker": null,
        "form": "10-K",
        "fiscal_year": null,
        "item": "Item 7",
        "title": "Management's Discussion and Analysis of Financial Condition and Results of Operations"
    },
    "executive_summary": null,
    "financial_results": {
        "periods": [],
        "metrics": [
            {
                "name": null,
                "value": null,
                "unit": null,
                "currency": null,
                "period": null,
                "change_vs_prior": null,
                "source_excerpt": null
            }
        ],
        "segments": []
    },
    "liquidity_and_capital_resources": {
        "cash_and_equivalents": [],
        "debt_and_financing": [],
        "capital_expenditures": [],
        "contractual_obligations": [],
        "sources_of_liquidity": [],
        "uses_of_liquidity": []
    },
    "cash_flows": {
        "operating": [],
        "investing": [],
        "financing": []
    },
    "trends_and_uncertainties": [],
    "critical_accounting_estimates": [],
    "source_sections": []
}

Reglas:
- Extrae solo informacion que aparezca explicitamente en el Item 7.
- Conserva los valores numericos como numeros, no como texto.
- Incluye unidad, moneda y periodo cuando existan.
- Usa null cuando un dato no este disponible y [] cuando no existan elementos.
- No inventes datos ni completes informacion desde otras secciones del 10-K.
- En source_excerpt incluye una cita breve del texto que respalde cada dato importante.
- El json se va a usar para hacer graficas automaticas con la libreria matplotlib, por lo que debe ser valido y consistente.
"""

# Carga el modelo de IA y genera una respuesta json para ser usada despues
def extraer_json_item7(texto_contexto, api_key=None, model="muse-spark-1.3-contributor"):
    client = OpenAI(
        api_key=api_key or os.environ.get("MODEL_API_KEY"), # Checa la key del .env
        base_url="https://api.meta.ai/v1" # Url de Meta
    )
    response = client.chat.completions.create(
        model=model,  # Cambie el modelo a Muse Spark 1.3 Contributor Tier
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"{instructions}\n\n{texto_contexto}"
            },
            {
                "role": "user",
                "content": "Extrae y estructura el Item 7 siguiendo exactamente el esquema JSON indicado."
            }
        ]
    )
    return json.loads(response.choices[0].message.content) # Regresa el mensaje generado por IA

# Lee el Item 7, lo envia al LLM y guarda la respuesta en resultado.json
def procesar_archivo_item7(ruta_txt, api_key=None, model="muse-spark-1.3-contributor"):
    ruta_txt = Path(ruta_txt)
    with open(ruta_txt, "r", encoding="utf-8") as file:
        texto_contexto = file.read()
    resultado = extraer_json_item7(texto_contexto, api_key=api_key, model=model)
    salida = BASE_DIR / "resultado.json"
    with open(salida, "w", encoding="utf-8") as archivo_json:
        json.dump({"respuesta": resultado}, archivo_json, ensure_ascii=False, indent=4)
    return resultado, salida


# Ejecuta la prueba
if __name__ == "__main__":
    resultado, salida = procesar_archivo_item7(file_path)
    print(f"Respuesta guardada en: {salida}")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
