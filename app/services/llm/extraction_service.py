from app.services.llm.client import client
import json

from app.services.llm.client import client
import json

def extract_structured_data(text: str):

    prompt = f"""
You are a high-precision document extraction engine.

TASK:
Analyze the provided document text and extract structured information.

INSTRUCTIONS:
- Identify the document_type: one of
  ["invoice", "receipt", "contract", "report", "other"].
- Extract only factual information explicitly present in the text.
- Do NOT infer missing values.
- Do NOT hallucinate.
- If a field is not found, return null.
- Return ONLY valid JSON.
- Do NOT include explanations, comments, or markdown.
- Ensure output is strictly parseable JSON.

OUTPUT FORMAT:

{{
  "document_type": "<invoice|receipt|contract|report|other>",
  "confidence_score": <number between 0 and 1>,
  "data": {{
    "document_number": string | null,
    "date": string | null,
    "total_amount": string | null,
    "vendor_or_party": string | null,
    "currency": string | null,
    "additional_fields": object | null
  }}
}}

Rules:
- confidence_score must reflect extraction certainty.
- currency should be ISO code if identifiable (USD, EUR, etc).
- additional_fields should contain any important extracted fields not covered above.
- Keep field names exactly as specified.

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