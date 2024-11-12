import asyncio
import datetime
import logging
import os
from io import BytesIO

import openai
import pdfplumber
import pytesseract
from PIL import Image, ImageFile
from sqlalchemy.orm import Session

from models.content import Content
from models.document import Document

ImageFile.LOAD_TRUNCATED_IMAGES = True  # Handle truncated images if they exist in the PDF

logger = logging.getLogger("pdf-extraction")
openai.api_key = os.getenv("OPENAI_API_KEY")

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Ensure cache directory exists

# Helper function to create a cache filename based on PDF name
def get_cache_path(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(CACHE_DIR, f"{pdf_name}_cache.json")

async def process_image(img, page_num):
    """Process an image using OCR."""
    try:
        # Convert image to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        # Use pytesseract for OCR
        ocr_text = pytesseract.image_to_string(img)
        return f"Page {page_num} Image (OCR): {ocr_text}"
    except Exception as e:
        logger.error(f"Failed to process image on page {page_num}: {e}")
        return ""

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

    # If cache does not exist, proceed to extract data
    all_text = ""
    image_descriptions = []

    with pdfplumber.open(pdf_path) as pdf:
        image_tasks = []
        for page_num, page in enumerate(pdf.pages[:5], start=1):  # Limit to first 5 pages
            page_text = page.extract_text() or ""
            all_text += page_text + "\n"
            
            # Extract images
            for img_obj in page.images:
                try:
                    # Get image data from bounding box
                    x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                    image_data = page.within_bbox((x0, top, x1, bottom)).to_image().original

                    # Append the coroutine to image_tasks
                    image_tasks.append(process_image(image_data, page_num))
                except Exception as e:
                    logger.error(f"Error extracting image on page {page_num}: {e}")

        # Run all image tasks concurrently
        image_descriptions = await asyncio.gather(*image_tasks)

        # Create a new Content entry for each page
        new_content = Content(
            document_id=new_document.id,
            page_number=1,
            text_content=all_text,
            image_content="\n".join(image_descriptions)
        )

        db.add(new_content)

    # Commit all changes at once
    db.commit()