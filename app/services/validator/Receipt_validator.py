from app.services.validator.base_validator import BaseValidator

class ReceiptValidator(BaseValidator):
    REQUIRED_FIELDS = [
        "total_amount",
        "date"
    ]

    def validate(self, data: dict):
        receipt_data=data.get("data",{})
        for field in self.REQUIRED_FIELDS:
            if not receipt_data.get(field):
                return False, f"Missing field: {field}"
        return True, None