from datetime import datetime
import re
from app.services.validator.base_validator import BaseValidator

class ReceiptValidator(BaseValidator):

    def validate(self, data: dict):

        if data.get("document_type") != "receipt":
            return False, "Invalid document_type for receipt"

        receipt_data = data.get("data", {})

        receipt_number = receipt_data.get("document_number")
        if receipt_number:
            if not re.match(r'^[A-Z0-9\-]+$', receipt_number):
                return False, "Invalid receipt_number format"

        date_value = receipt_data.get("date")
        if date_value:
            try:
                datetime.strptime(date_value, "%d %B %Y")
            except ValueError:
                return False, "Invalid date format. Expected 'DD Month YYYY'"
        else:
            return False, "Receipt date is required"

        total_amount = receipt_data.get("total_amount")
        if total_amount:
            numeric = re.sub(r"[^\d.]", "", str(total_amount))
            try:
                amount = float(numeric)
                if amount <= 0:
                    return False, "Total amount must be greater than 0"
            except ValueError:
                return False, "Invalid total_amount format"
        else:
            return False, "Total amount is required"

        merchant = receipt_data.get("vendor_or_party")
        if not merchant or len(str(merchant).strip()) < 2:
            return False, "Merchant name is required"

        return True, None