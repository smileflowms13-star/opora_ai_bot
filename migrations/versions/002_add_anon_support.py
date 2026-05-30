"""add anon_support table

Revision ID: 002
Revises: 001
Create Date: 2026-05-30
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS anon_support (
            anon_id TEXT PRIMARY KEY,
            telegram_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS anon_support")