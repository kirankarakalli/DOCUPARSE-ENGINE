from app.services.validator.base_validator import BaseValidator


class InvoiceValidator(BaseValidator):
    Required_fields = [
        "document_number",
        "total_amount",
        "vendor_or_party"   
    ]

    def validate(self, data: dict):
        invoice_data = data.get("data", {})
        
        for field in self.Required_fields:
            if not invoice_data.get(field):
                return False, f"Missing field: {field}"
        return True, None