import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

SCHEMA={
    "type": "object",
    "properties": {
        "document_type": {"type": "string"},
        "invoice_number": {"type": ["string", "null"]},
        "receipt_number": {"type": ["string", "null"]},
        "date": {"type": ["string", "null"]},
        "total_amount": {"type": ["string", "null"]},
        "vendor": {"type": ["string", "null"]}
    },

    "required":["document_type"]
}

def validate_against_schema(data:dict,schema:dict):
    try:
        validate(instance=data,schema=schema)
        return True,None
    except ValidationError as e:
        return False,None

