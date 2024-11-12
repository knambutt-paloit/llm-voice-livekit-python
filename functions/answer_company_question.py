import asyncio
import json
import logging
import os
from datetime import datetime
from io import BytesIO
from typing import Annotated

import openai
import pdfplumber
import pytesseract
from httpx import Timeout
from livekit.agents import llm
from PIL import Image
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

logger = logging.getLogger("company-question-demo")
openai.api_key = os.getenv("OPENAI_API_KEY")

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Ensure cache directory exists

# Custom timeout settings
timeout = Timeout(timeout=20.0)  # Set to 20 seconds, adjust if needed

# Helper function to create a cache filename based on PDF name
def get_cache_path(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(CACHE_DIR, f"{pdf_name}_cache.json")

async def extract_images_from_pdf(pdf_path):
    cache_path = get_cache_path(pdf_path)
    
    # Check if cached data exists
    if os.path.exists(cache_path):
        logger.info(f"Loading cached content from {cache_path}")
        with open(cache_path, "r") as cache_file:
            return json.load(cache_file)
        
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
                    # Get image data
                    x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                    image_data = page.within_bbox((x0, top, x1, bottom)).to_image().original

                    # Append the coroutine to image_tasks
                    image_tasks.append(process_image(image_data, page_num))
                except Exception as e:
                    logger.error(f"Error extracting image on page {page_num}: {e}")

        # Run all image tasks concurrently
        image_descriptions = await asyncio.gather(*image_tasks)

    # Combine extracted text and images
    content = {"text": all_text, "images": image_descriptions}

    # Save extracted content to cache
    with open(cache_path, "w") as cache_file:
        json.dump(content, cache_file)
        logger.info(f"Cached content saved to {cache_path}")

    return content

class AnswerCompanyQuestion(llm.FunctionContext):

    @llm.ai_callable()
    async def get_public_holiday_of_palo_it_company(
        self,
        question: Annotated[
            str, llm.TypeInfo(description="The question or get information about public holiday of PALO IT company")
        ],
    ):
        """Answers questions based on the public holiday of PALO IT company."""
        logger.info(f"Answering question: {question}")

        pdf_path = "assets/pdf/company/Palo_IT_2024_Public Holiday.pdf"

        # Extract content from PDF or get from cache
        content = await extract_images_from_pdf(pdf_path)
        context = content["text"] + "\n\n" + "\n".join(content["images"])

        response = openai.chat.completions.create(
            model="gpt-4",  # or gpt-4-mini
            messages=[
                {"role": "system", "content": "You are an assistant that answers questions based on the provided context."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Question: {question}"}
            ],
            max_tokens=150,
            temperature=0
        )
        
        answer = response.choices[0].message.content.strip()
        logger.info(f"Answer found: {answer}")
        return answer
    
    @llm.ai_callable()
    async def get_hr_onboarding_for_new_joiners(
        self,
        question: Annotated[
            str, llm.TypeInfo(description="The question or get information about HR onboarding for new joiners")
        ],
    ):
        """Answers questions based on the HR onboarding for new joiners."""
        logger.info(f"Answering question: {question}")

        pdf_directory = "assets/pdf"
        pdf_file = os.path.join(pdf_directory, "HR_Onboarding_New_Joiners_Updated_2024.pdf")
        all_text = ""
        image_descriptions = []

        async def process_image(image_data, page_num):
            try:
                # Load image from bytes
                img = Image.open(BytesIO(image_data))

                # Use OpenAI's vision model (or fallback to pytesseract for OCR)
                img_bytes = BytesIO()
                img.save(img_bytes, format="PNG")
                img_bytes.seek(0)

                try:
                    response = openai.images.create(
                        file=img_bytes,
                        model="openai-vision",  # Replace with the specific OpenAI vision model if available
                        prompt="Describe this image content in the context of HR onboarding."
                    )
                    return f"Page {page_num} Image: {response['data'][0]['text']}"
                except Exception as e:
                    logger.warning(f"OpenAI Vision failed; using OCR for image on page {page_num}. Error: {e}")
                    return f"Page {page_num} Image (OCR): {pytesseract.image_to_string(img)}"
            except Exception as e:
                logger.error(f"Failed to process image on page {page_num}: {e}")
                return ""

        with pdfplumber.open(pdf_file) as pdf:
            image_tasks = []
            for page_num, page in enumerate(pdf.pages[:5], start=1):  # Limit to first 5 pages
                # Extract text
                page_text = page.extract_text() or ""
                all_text += page_text + "\n"

                # Extract images
                for img_obj in page.images:
                    try:
                        # Get image data
                        x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                        image_data = page.within_bbox((x0, top, x1, bottom)).to_image().original

                        # Schedule async image processing
                        image_tasks.append(process_image(image_data, page_num))
                    except Exception as e:
                        logger.error(f"Error extracting image on page {page_num}: {e}")

            # Process all images asynchronously
            image_descriptions = await asyncio.gather(*image_tasks)

        # Combine text and image descriptions for context
        context = all_text + "\n\n" + "\n".join(image_descriptions)

        # Use OpenAI GPT model to answer the question based on the combined context
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Use gpt-4 if available, or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are an assistant that answers questions based on the provided context."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Question: {question}"}
            ],
            max_tokens=150,
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        logger.info(f"Answer found: {answer}")
        return answer