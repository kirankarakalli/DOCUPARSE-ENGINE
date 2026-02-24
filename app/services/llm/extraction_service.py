from app.services.llm.client import client
import json

from app.services.llm.client import client
import json

def extract_structured_data(text: str):

    prompt = f"""
    You are a document extraction system.

    1. Identify the document_type (invoice, receipt, contract, report, other).
    2. Extract relevant structured data.
    3. Return ONLY valid JSON.
    4. If a field is missing, return null.

    JSON format:

    {{
    "document_type": "",
    "data": {{
        "document_number": null,
        "date": null,
        "total_amount": null,
        "vendor_or_party": null,
        "additional_fields": null
    }}
        }}

Document text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a document extraction engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.strip("```")
        content = content.replace("json", "").strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON returned from LLM", "raw_output": content}