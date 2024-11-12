# functions/extract_and_store.py
import datetime
import json
import os

import pdfplumber
import pytesseract
from PIL import Image
from sqlalchemy.orm import Session

from models.content import Content
from models.document import Document

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Ensure cache directory exists

# Helper function to create a cache filename based on PDF name
def get_cache_path(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(CACHE_DIR, f"{pdf_name}_cache.json")

async def extract_and_store_pdf_content(pdf_path: str, title: str, db: Session):
    # Add a new entry in the Document table
    new_document = Document(
        title=title,
        file_path=pdf_path,
        upload_date=datetime.datetime.now()
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)  # Get the ID of the newly inserted document

    # Extract content from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text_content = page.extract_text() or ""
            
            # Extract images and apply OCR
            images = []
            for img_obj in page.images:
                img = page.within_bbox((img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"])).to_image()
                ocr_text = pytesseract.image_to_string(img)
                images.append(ocr_text)
            
            # Create a new Content entry for each page
            new_content = Content(
                document_id=new_document.id,
                page_number=page_number,
                text_content=text_content,
                image_content="\n".join(images)
            )

            db.add(new_content)

    # Commit all changes at once
    db.commit()