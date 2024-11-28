from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import shutil
import PyPDF2
import re
from pathlib import Path

async def process_pdf(file_content):
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file_content, temp_file)
        temp_path = temp_file.name

    try:
        with open(temp_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = reader.pages[0].extract_text()
            
            provider = re.search(r"Provider:\s*(.*?)\s*\[", text).group(1).strip()
            course = re.search(r"Course:\s*(.*?)\s*\[", text).group(1).strip()
            start_date = re.search(r"Course Start Date:\s*(\d{2}/\d{2}/\d{4})", text).group(1)
            end_date = re.search(r"Course End Date:\s*(\d{2}/\d{2}/\d{4})", text).group(1)
            
            return {
                "provider": provider,
                "course": course,
                "start_date": start_date,
                "end_date": end_date
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        Path(temp_path).unlink()