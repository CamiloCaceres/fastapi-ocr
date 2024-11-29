from PIL import Image
import pytesseract
from tempfile import NamedTemporaryFile
import shutil
from pathlib import Path

async def extract_text(file_content, language='eng'):
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file_content, temp_file)
        temp_path = temp_file.name

    try:
        image = Image.open(temp_path)
        text = pytesseract.image_to_string(image, lang=language)
        
        # Return both raw text and structured data
        words = text.split()
        char_count = len(text)
        line_count = len(text.splitlines())
        
        return {
            "text": text.strip(),
            "metadata": {
                "word_count": len(words),
                "char_count": char_count,
                "line_count": line_count,
                "language": language
            }
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        Path(temp_path).unlink()

async def extract_structured_data(file_content, language='eng'):
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file_content, temp_file)
        temp_path = temp_file.name

    try:
        image = Image.open(temp_path)
        data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
        
        # Convert to more usable format
        structured_data = []
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                structured_data.append({
                    'text': data['text'][i],
                    'confidence': data['conf'][i],
                    'block_num': data['block_num'][i],
                    'position': {
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    }
                })
        
        return structured_data
    except Exception as e:
        return {"error": str(e)}
    finally:
        Path(temp_path).unlink()