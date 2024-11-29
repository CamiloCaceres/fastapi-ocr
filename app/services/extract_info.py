from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import shutil
import PyPDF2
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VisaInfo:
    type: str
    expiry_date: str
    sector: str = ""
    status: str = "Active"

async def parse_coe(file_content):
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

async def parse_visa(file_content):
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file_content, temp_file)
        temp_path = temp_file.name

    try:
        with open(temp_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Extract visa type
        type = ""
        if "Student (subclass 500)" in text:
            type = "Student (500)"
        elif "Temporary Graduate (subclass 485)" in text:
            type = "Temporary Graduate (485)"
        elif "Bridging A visa" in text:
            type = "Bridging A"
        
        # Extract expiry date
        date_patterns = [
            r"Must not arrive after\s*([\d]{1,2}\s+[A-Za-z]+\s+[\d]{4})",
            r"Stay until\s*([\d]{1,2}\s+[A-Za-z]+\s+[\d]{4})",
            r"Length of stay\s*([\d]{1,2}\s+[A-Za-z]+\s+[\d]{4})"
        ]
        
        expiry_date = None
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    expiry_date = datetime.strptime(match.group(1), "%d %B %Y")
                    break
                except ValueError:
                    continue
        
        # Extract sector
        sector = ""
        sector_match = re.search(r"Sector:\s*([^\n]*)", text)
        if sector_match:
            sector = sector_match.group(1).strip()
        
        # Check status
        status = "Active"
        if "Status: Not Active" in text:
            status = "Not Active"
        
        if not type or not expiry_date:
            raise ValueError("Could not extract required visa information")
        
        return VisaInfo(
            type=type,
            expiry_date=expiry_date.strftime("%Y-%m-%d"),
            sector=sector,
            status=status
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        Path(temp_path).unlink()

        