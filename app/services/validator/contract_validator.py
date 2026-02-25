from datetime import datetime
import re
from app.services.validator.base_validator import BaseValidator


class ContractValidator(BaseValidator):

    def validate(self, data: dict):

        if data.get("document_type") != "contract":
            return False, "Invalid document_type for contract"

        contract_data = data.get("data", {})

        required_fields = [
            "contract_number",
            "effective_date",
            "party_one",
            "party_two"
        ]

        for field in required_fields:
            if not contract_data.get(field):
                return False, f"Missing field: {field}"

        contract_number = contract_data.get("contract_number")
        if contract_number:
            if not re.match(r'^[A-Z0-9\-\/]+$', contract_number):
                return False, "Invalid contract_number format"

        effective_date = contract_data.get("effective_date")
        try:
            datetime.strptime(effective_date, "%d %B %Y")
        except ValueError:
            return False, "Invalid effective_date format. Expected 'DD Month YYYY'"

        party_one = contract_data.get("party_one")
        party_two = contract_data.get("party_two")

        if party_one.strip().lower() == party_two.strip().lower():
            return False, "party_one and party_two cannot be the same"

        if len(party_one.strip()) < 2:
            return False, "party_one name too short"

        if len(party_two.strip()) < 2:
            return False, "party_two name too short"

        return True, None