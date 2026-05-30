"""add topic_id to anon_support

Revision ID: 003
Revises: 002
Create Date: 2026-05-30
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("ALTER TABLE anon_support ADD COLUMN topic_id INTEGER")

def downgrade() -> None:
    op.execute("ALTER TABLE anon_support DROP COLUMN topic_id")