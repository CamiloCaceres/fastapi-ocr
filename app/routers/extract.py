from fastapi import APIRouter, UploadFile, File

from ..services import extract_info

router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("/coe")
async def parse_coe(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "File must be a PDF"}
    
    return await extract_info.parse_coe(file.file)

@router.post("/visa")
async def parse_visa(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "File must be a PDF"}
    
    return await extract_info.parse_visa(file.file)
