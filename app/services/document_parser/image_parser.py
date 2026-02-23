from app.services.preprocessing_pipeline.preprocess import preprocess_image
from app.services.preprocessing_pipeline.ocr import extract_text_from_image

def parse_image(file_path:str,document_id:str)->str:
    """
    Process image file:
    1. Preprocess
    2. OCR
    3. Return extracted text
    """

    preprocess_result=preprocess_image(file_path,document_id)
    deskewed_path=preprocess_result.get('deskewed')
    if not deskewed_path:
        raise ValueError("Deskewed path missing after preprocessing")
    
    extracted_text = extract_text_from_image(deskewed_path)

    return extracted_text


