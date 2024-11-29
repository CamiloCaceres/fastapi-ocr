from fastapi import APIRouter, UploadFile, File
from typing import Optional
from ..services import ocr

router = APIRouter(prefix="/ocr", tags=["ocr"])

@router.post("/text")
async def extract_text(
    file: UploadFile = File(...),
    language: Optional[str] = "eng"
):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        return {"error": "File must be an image (PNG, JPG, TIFF, BMP)"}
    
    return await ocr.extract_text(file.file, language)

@router.post("/structured")
async def extract_structured(
    file: UploadFile = File(...),
    language: Optional[str] = "eng"
):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        return {"error": "File must be an image (PNG, JPG, TIFF, BMP)"}
    
    return await ocr.extract_structured_data(file.file, language)