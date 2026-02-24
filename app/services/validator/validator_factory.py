from app.services.validator.invoice_validator import InvoiceValidator
from app.services.validator.Receipt_validator import ReceiptValidator
from app.services.validator.contract_validator import ContractValidator

def get_validator(document_type: str):
    if document_type == "invoice":
        return InvoiceValidator()
    elif document_type == "receipt":
        return ReceiptValidator()
    elif document_type =='contract':
        return ContractValidator()
    else:
        return None