
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

import os
import shutil
import uuid

from ocr_engine import extract_text

app = FastAPI(
    title="DocTR OCR API",
    description="OCR application using DocTR and FastAPI",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/extract-text")
def extract_document(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png", ".docx"]

    extension = os.path.splitext(file.filename or "")[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text(file_path)

        return {
            "filename": file.filename,
            "status": "success",
            "extracted_text": extracted_text
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    finally:
        file.file.close()

        if os.path.exists(file_path):
            os.remove(file_path)
