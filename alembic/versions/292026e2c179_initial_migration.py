"""Initial migration

Revision ID: 292026e2c179
Revises: 
Create Date: 2024-11-12 16:14:42.821384

"""
import os
import sys

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '292026e2c179'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Add project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def upgrade() -> None:
    # Create the documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('upload_date', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index(op.f('ix_public_documents_file_path'), 'documents', ['file_path'], unique=True, schema='public')
    op.create_index(op.f('ix_public_documents_id'), 'documents', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_documents_title'), 'documents', ['title'], unique=False, schema='public')

    # Create the contents table with ON DELETE CASCADE and ON UPDATE SET DEFAULT for the foreign key
    op.create_table(
        'contents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('public.documents.id', onupdate="SET DEFAULT", ondelete="CASCADE"), nullable=True),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('image_content', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index(op.f('ix_public_contents_document_id'), 'contents', ['document_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_contents_id'), 'contents', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_contents_page_number'), 'contents', ['page_number'], unique=False, schema='public')


def downgrade() -> None:
    # Drop indexes and tables in reverse order
    op.drop_index(op.f('ix_public_contents_page_number'), table_name='contents', schema='public')
    op.drop_index(op.f('ix_public_contents_id'), table_name='contents', schema='public')
    op.drop_index(op.f('ix_public_contents_document_id'), table_name='contents', schema='public')
    op.drop_table('contents', schema='public')
    op.drop_index(op.f('ix_public_documents_title'), table_name='documents', schema='public')
    op.drop_index(op.f('ix_public_documents_id'), table_name='documents', schema='public')
    op.drop_index(op.f('ix_public_documents_file_path'), table_name='documents', schema='public')
    op.drop_table('documents', schema='public')