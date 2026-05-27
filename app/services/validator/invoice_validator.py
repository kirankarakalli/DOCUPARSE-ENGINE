from app.services.validator.base_validator import BaseValidator
import re
from datetime import datetime

from app.services.validator.base_validator import BaseValidator
import re
from datetime import datetime

class InvoiceValidator(BaseValidator):

    def validate(self, data: dict):

        if data.get("document_type") != "invoice":
            return False, "Invalid document_type for invoice"

        data_field = data.get("data", {})
        
        invoice_number = data_field.get("document_number")
        if invoice_number:
            if not re.match(r'^[A-Z0-9\-]+$', invoice_number):
                return False, "Invalid invoice_number format"

        date_value = data_field.get("date")
        if date_value:
            try:
                try:
                    datetime.strptime(date_value, "%d %B %Y")
                except:
                    datetime.strptime(date_value, "%B %d, %Y")

            except ValueError:
                return False, "Invalid date format"

        total_amount = data_field.get("total_amount")
        if total_amount:
            numeric = re.sub(r"[^\d.]", "", str(total_amount))
            try:
                amount = float(numeric)
                if amount <= 0:
                    return False, "Total amount must be greater than 0"
            except ValueError:
                return False, "Invalid total_amount format"

        vendor = data_field.get("vendor_or_party")
        if not vendor or not isinstance(vendor, str) or len(vendor.strip()) < 2:
            return False, "Vendor is required"

        return True, None