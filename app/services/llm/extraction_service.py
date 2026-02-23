from app.services.llm.client import client
import json

from app.services.llm.client import client
import json

def extract_structured_data(text: str):

    prompt = f"""
You are a document analysis system.

Extract structured information from the following document text.

Return ONLY valid JSON in this format:

{{
  "document_type": "",
  "invoice_number": "",
  "date": "",
  "total_amount": "",
  "vendor": ""
}}

If any field is missing, return null.

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