from pdf2image import convert_from_path
import tempfile
import os
from app.services.preprocessing_pipeline.ocr import extract_text_from_image

def parse_pdf(file_path:str)->str:
    """
    Convert PDF pages to images and run OCR on each page.
    Returns combined extracted text.
    """

    extracted_text=""
    pages=convert_from_path(file_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        for i,page in enumerate(pages):
            image_path = os.path.join(temp_dir, f"page_{i}.png")
            page.save(image_path, "PNG")

            text=extract_text_from_image(image_path)
            extracted_text+=text+"\n"

    return extracted_text



