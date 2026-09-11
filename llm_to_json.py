from openai import OpenAI
from pathlib import Path
import json
from pathlib import Path

file_path = (
    Path(__file__).parent
    / "company_report"
    / "AAPL"
    / "2025"
    / "sec-edgar-filings"
    / "AAPL"
    / "10-K"
    / "0000320193-25-000079"
    / "item_7_clean.txt"
)

with open(file_path, "r", encoding="utf-8") as file:
    texto_contexto = file.read()

client = OpenAI(
    api_key="API_KEY"
    # API OLLAMA_LOCALURL="http://localhost:11434" 
)


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

response = client.chat.completions.create(
    model="gpt-4o",  # gpt-4o, Ollama, gpt-5.6-Luna, gpt-5.6-turbo, gpt-5.6-turbo-16k, gpt-5.6-turbo-32k
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

resultado = json.loads(response.choices[0].message.content)
salida = Path(__file__).parent / "resultado.json"

with open(salida, "w", encoding="utf-8") as archivo_json:
    json.dump(
        {"respuesta": resultado},
        archivo_json,
        ensure_ascii=False,
        indent=4
    )

print(f"Respuesta guardada en: {salida}")
print(json.dumps(resultado, ensure_ascii=False, indent=2))
