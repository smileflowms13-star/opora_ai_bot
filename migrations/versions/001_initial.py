"""initial

Revision ID: 001
Revises: 
Create Date: 2026-05-30
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            age_confirmed INTEGER DEFAULT 0,
            consent_accepted INTEGER DEFAULT 0,
            daily_reminder_enabled INTEGER DEFAULT 0,
            daily_reminder_time TEXT,
            crisis_plan TEXT,
            language TEXT DEFAULT 'ru',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            telegram_id INTEGER,
            role TEXT NOT NULL,
            content TEXT,
            text TEXT,
            is_high_risk INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            telegram_id INTEGER,
            mood INTEGER,
            anxiety INTEGER,
            energy INTEGER,
            sleep INTEGER,
            sleep_quality INTEGER,
            note TEXT,
            created_at TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS trigger_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            telegram_id INTEGER,
            situation TEXT,
            thought TEXT,
            emotion TEXT,
            body TEXT,
            impulse TEXT,
            need TEXT,
            created_at TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS onboarding (
            user_id INTEGER PRIMARY KEY,
            focus_area TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
            telegram_id INTEGER PRIMARY KEY,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_action_date TEXT,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    """)
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_diary_entries_user_id ON diary_entries(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_trigger_entries_user_id ON trigger_entries(user_id)")

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS streaks")
    op.execute("DROP TABLE IF EXISTS onboarding")
    op.execute("DROP TABLE IF EXISTS trigger_entries")
    op.execute("DROP TABLE IF EXISTS diary_entries")
    op.execute("DROP TABLE IF EXISTS messages")
    op.execute("DROP TABLE IF EXISTS users")