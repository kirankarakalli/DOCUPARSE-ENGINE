import cv2
import pytesseract


def extract_text_from_image(image_path:str)->str:
    img=cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")
    
    text=pytesseract.image_to_string(img)
    return text


