"""Add seed data

Revision ID: 8523b998efe3
Revises: 292026e2c179
Create Date: 2024-11-12 22:20:23.367127

"""
import os
import sys

from typing import Sequence, Union

import asyncio
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8523b998efe3'
down_revision: Union[str, None] = '292026e2c179'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Add project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.document import Document
from db.session import SessionLocal
from utils.pdf import extract_and_store_pdf_content

# Directory containing PDF files to process
PDF_DIRECTORY = "assets/pdf/company"

# Start a new session
bind = op.get_bind()
session = SessionLocal(bind=bind)

async def process_pdf_files():
    """Process all unprocessed PDF files in the PDF_DIRECTORY."""
    print("Processing PDF files on startup...")

    for filename in os.listdir(PDF_DIRECTORY):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIRECTORY, filename)

            # Check if this PDF has already been processed
            document = session.query(Document).filter_by(file_path=pdf_path).first()
            if document:
                print(f"PDF '{filename}' already processed, skipping.")
                continue

            # Process and store the PDF content
            try:
                print(f"Processing PDF '{filename}'...")
                await extract_and_store_pdf_content(pdf_path, title=filename, db=session)
                print(f"Successfully processed and stored '{filename}'.")
            except Exception as e:
                print(f"Failed to process '{filename}': {e}")

def upgrade() -> None:
    asyncio.run(process_pdf_files())


def downgrade() -> None:
    """Reverse the PDF processing by deleting inserted data."""
    print("Removing all processed PDF entries...")

    for filename in os.listdir(PDF_DIRECTORY):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIRECTORY, filename)
            print('pdf_path:', pdf_path)

            # Delete any records in the documents table with this file path
            session.execute(
                sa.delete(Document).where(Document.file_path == pdf_path)
            )
    
    # Commit the changes to remove the data
    session.commit()
    print("All processed PDF entries have been removed.")
