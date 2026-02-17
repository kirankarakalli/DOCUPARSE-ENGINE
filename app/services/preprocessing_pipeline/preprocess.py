import mimetypes
from fastapi import UploadFile
import cv2
import numpy as np
import os
def detect_file_type(file: UploadFile) -> str:
    """
    Detect the file type based on the file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected file type (e.g., 'text', 'image', 'pdf', etc.).
    """
    mime_type,_=mimetypes.guess_type(file.filename)

    if not mime_type:
        return "unknown"
    if mime_type.startswith("text"):
        return "text"
    elif mime_type.startswith("image"):
        return "image"
    elif mime_type in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        return "docx"
    elif mime_type=="application/pdf":
        return "pdf"
    else:
        return "other"
    

def convert_to_grayscale(image_path:str,output_dir:str)->str:
    os.makedirs(output_dir,exist_ok=True)
    img=cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")
    img_grayscale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    file_path=os.path.join(output_dir,"01_gray_scale.jpg")
    cv2.imwrite(file_path,img_grayscale)
    return file_path



def denoise_image(image_path:str,output_dir:str)->str:
    os.makedirs(output_dir,exist_ok=True)
    img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)

    if img is None:
       raise ValueError("Error: Image not found. Please check the file path.")
    else:
        denoised_image_median=cv2.medianBlur(img,3)
        file_path=os.path.join(output_dir,"02_denoise_img.jpg")
        cv2.imwrite(file_path,denoised_image_median)
        return file_path
        


def threshold_image(image_path:str,output_dir:str)->str:
    os.makedirs(output_dir,exist_ok=True)
    img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")

    adaptive_threshold=cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    file_path=os.path.join(output_dir,"03_Threshold_img.jpg")
    cv2.imwrite(file_path,adaptive_threshold)
    return file_path



def deskew_image(image_path:str,output_dir:str)->str:
    os.makedirs(output_dir,exist_ok=True)
    img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("could not read a image")
    img=cv2.bitwise_not(img)

    coords=np.column_stack(np.where(img>0))
    angle=cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle=90+angle
    (h,w)=img.shape
    center=(w//2,h//2)
    M=cv2.getRotationMatrix2D(center,angle,1.0)
    rotated = cv2.warpAffine(
        img,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    file_path=os.path.join(output_dir,"04_deskew_img.jpg")
    cv2.imwrite(file_path, rotated)
    return file_path
    

def preprocess_image(image_path:str,upload_id:str)->dict:
    base_output_dir=os.path.join('processed',upload_id)
    os.makedirs(base_output_dir,exist_ok=True)

    gray_path=convert_to_grayscale(image_path,base_output_dir)
    denoise_path=denoise_image(gray_path,base_output_dir)
    threshold_path=threshold_image(denoise_path,base_output_dir)
    deskew_path=deskew_image(threshold_path,base_output_dir)

    return{
        "grayscale": gray_path,
        "denoised": denoise_path,
        "threshold": threshold_path,
        "deskewed": deskew_path
    }








    
