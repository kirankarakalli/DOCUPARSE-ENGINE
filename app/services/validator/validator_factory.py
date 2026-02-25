from app.services.validator.invoice_validator import InvoiceValidator
from app.services.validator.Receipt_validator import ReceiptValidator
from app.services.validator.contract_validator import ContractValidator


VALIDATOR_REGISTRY = {
    "invoice": InvoiceValidator,
    "receipt": ReceiptValidator,
    "contract": ContractValidator,
}


def get_validator(document_type: str):
    if not document_type:
        return None

    document_type = document_type.strip().lower()

    validator_class = VALIDATOR_REGISTRY.get(document_type)
    if not validator_class:
        return None

    return validator_class()