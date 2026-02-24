from app.services.validator.base_validator import BaseValidator

class ContractValidator(BaseValidator):

    REQUIRED_FIELDS = [
        "contract_number",
        "effective_date",
        "party_one",
        "party_two"
    ]

    def validate(self, data: dict):
        contract_data = data.get("data", {})
        for field in self.REQUIRED_FIELDS:
            if not contract_data.get(field):
                return False, f"Missing field: {field}"

        if contract_data.get("party_one") == contract_data.get("party_two"):
            return False, "party_one and party_two cannot be same"

        return True, None