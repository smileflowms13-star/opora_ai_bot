import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "opora.db"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _get_table_columns(cursor: sqlite3.Cursor, table_name: str) -> set[str]:
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    return {row[1] for row in cursor.fetchall()}


def _add_column_if_missing(
    cursor: sqlite3.Cursor,
    table_name: str,
    column_name: str,
    column_definition: str,
) -> None:
    columns = _get_table_columns(cursor, table_name)

    if column_name not in columns:
        cursor.execute(
            f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_definition}'
        )


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            age_confirmed INTEGER DEFAULT 0,
            consent_accepted INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
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
        """
    )

    cursor.execute(
        """
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
        """
    )

    cursor.execute(
        """
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
        """
    )

    # РњСЏРіРєРёРµ РјРёРіСЂР°С†РёРё РґР»СЏ СЃС‚Р°СЂС‹С… РІРµСЂСЃРёР№ С‚Р°Р±Р»РёС†
    user_columns = _get_table_columns(cursor, "users")

    if "username" not in user_columns:
        _add_column_if_missing(cursor, "users", "username", "TEXT")

    if "first_name" not in user_columns:
        _add_column_if_missing(cursor, "users", "first_name", "TEXT")

    if "age_confirmed" not in user_columns:
        _add_column_if_missing(cursor, "users", "age_confirmed", "INTEGER DEFAULT 0")

    if "consent_accepted" not in user_columns:
        _add_column_if_missing(cursor, "users", "consent_accepted", "INTEGER DEFAULT 0")

    if "created_at" not in user_columns:
        _add_column_if_missing(cursor, "users", "created_at", "TEXT")

    if "updated_at" not in user_columns:
        _add_column_if_missing(cursor, "users", "updated_at", "TEXT")

    message_columns = _get_table_columns(cursor, "messages")
    if "user_id" not in message_columns:
        _add_column_if_missing(cursor, "messages", "user_id", "INTEGER")

    if "telegram_id" not in message_columns:
        _add_column_if_missing(cursor, "messages", "telegram_id", "INTEGER")

    if "role" not in message_columns:
        _add_column_if_missing(cursor, "messages", "role", "TEXT")

    if "content" not in message_columns:
        _add_column_if_missing(cursor, "messages", "content", "TEXT")

    if "text" not in message_columns:
        _add_column_if_missing(cursor, "messages", "text", "TEXT")

    if "is_high_risk" not in message_columns:
        _add_column_if_missing(cursor, "messages", "is_high_risk", "INTEGER DEFAULT 0")

    if "created_at" not in message_columns:
        _add_column_if_missing(cursor, "messages", "created_at", "TEXT")

    diary_columns = _get_table_columns(cursor, "diary_entries")
    if "user_id" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "user_id", "INTEGER")

    if "telegram_id" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "telegram_id", "INTEGER")

    if "mood" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "mood", "INTEGER")

    if "anxiety" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "anxiety", "INTEGER")

    if "energy" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "energy", "INTEGER")

    if "sleep" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "sleep", "INTEGER")

    if "sleep_quality" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "sleep_quality", "INTEGER")

    if "note" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "note", "TEXT")

    if "created_at" not in diary_columns:
        _add_column_if_missing(cursor, "diary_entries", "created_at", "TEXT")

    trigger_columns = _get_table_columns(cursor, "trigger_entries")
    if "user_id" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "user_id", "INTEGER")

    if "telegram_id" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "telegram_id", "INTEGER")

    if "situation" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "situation", "TEXT")

    if "thought" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "thought", "TEXT")

    if "emotion" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "emotion", "TEXT")

    if "body" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "body", "TEXT")

    if "impulse" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "impulse", "TEXT")

    if "need" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "need", "TEXT")

    if "created_at" not in trigger_columns:
        _add_column_if_missing(cursor, "trigger_entries", "created_at", "TEXT")

    try:
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_telegram_id
            ON users(telegram_id)
            """
        )
    except sqlite3.IntegrityError:
        # Р•СЃР»Рё РІ СЃС‚Р°СЂРѕР№ Р±Р°Р·Рµ РµСЃС‚СЊ РґСѓР±Р»Рё telegram_id, РёРЅРґРµРєСЃ РјРѕР¶РµС‚ РЅРµ СЃРѕР·РґР°С‚СЊСЃСЏ.
        # Р”Р»СЏ MVP СЌС‚Рѕ РЅРµ РєСЂРёС‚РёС‡РЅРѕ.
        pass

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_messages_user_id
        ON messages(user_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_diary_entries_user_id
        ON diary_entries(user_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_trigger_entries_user_id
        ON trigger_entries(user_id)
        """
    )

    conn.commit()
    conn.close()


def _get_internal_user_id(
    cursor: sqlite3.Cursor,
    telegram_id: int,
) -> Optional[int]:
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return int(row["id"])


def _get_user_identifiers(
    cursor: sqlite3.Cursor,
    telegram_id: int,
) -> list[int]:
    ids = [int(telegram_id)]

    internal_user_id = _get_internal_user_id(cursor, telegram_id)

    if internal_user_id is not None and internal_user_id not in ids:
        ids.append(internal_user_id)

    return ids


def ensure_user(
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    now = _now()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    if row is not None:
        user_id = int(row["id"])

        update_parts = ["updated_at = ?"]
        params: list[Any] = [now]

        if username is not None:
            update_parts.append("username = ?")
            params.append(username)

        if first_name is not None:
            update_parts.append("first_name = ?")
            params.append(first_name)

        params.append(telegram_id)

        cursor.execute(
            f"""
            UPDATE users
            SET {", ".join(update_parts)}
            WHERE telegram_id = ?
            """,
            params,
        )

        conn.commit()
        conn.close()

        return user_id

    cursor.execute(
        """
        INSERT INTO users (
            telegram_id,
            username,
            first_name,
            age_confirmed,
            consent_accepted,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, 0, 0, ?, ?)
        """,
        (
            telegram_id,
            username,
            first_name,
            now,
            now,
        ),
    )

    user_id = int(cursor.lastrowid)

    conn.commit()
    conn.close()

    return user_id


def get_or_create_user(
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> int:
    return ensure_user(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
    )


def user_has_consent(telegram_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT age_confirmed, consent_accepted
        FROM users
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return False

    age_confirmed = int(row["age_confirmed"] or 0)
    consent_accepted = int(row["consent_accepted"] or 0)

    return age_confirmed == 1 and consent_accepted == 1


def set_user_consent(
    telegram_id: int,
    accepted: bool = True,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> None:
    ensure_user(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
    )

    conn = get_connection()
    cursor = conn.cursor()

    value = 1 if accepted else 0

    cursor.execute(
        """
        UPDATE users
        SET age_confirmed = ?,
            consent_accepted = ?,
            updated_at = ?
        WHERE telegram_id = ?
        """,
        (
            value,
            value,
            _now(),
            telegram_id,
        ),
    )

    conn.commit()
    conn.close()


def reset_user_consent(telegram_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "users")

    set_parts = []
    params: list[Any] = []

    if "age_confirmed" in columns:
        set_parts.append("age_confirmed = ?")
        params.append(0)

    if "consent_accepted" in columns:
        set_parts.append("consent_accepted = ?")
        params.append(0)

    if "updated_at" in columns:
        set_parts.append("updated_at = ?")
        params.append(_now())

    if not set_parts:
        conn.close()
        return

    params.append(telegram_id)

    cursor.execute(
        f"""
        UPDATE users
        SET {", ".join(set_parts)}
        WHERE telegram_id = ?
        """,
        params,
    )

    conn.commit()
    conn.close()


def save_message(
    user_id: Optional[int] = None,
    role: str = "user",
    content: Optional[str] = None,
    text: Optional[str] = None,
    telegram_id: Optional[int] = None,
    is_high_risk: bool = False,
    **kwargs: Any,
) -> int:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        raise ValueError("save_message: user_id or telegram_id is required")

    if content is None:
        content = text

    if content is None:
        content = kwargs.get("message") or ""

    role = role or "user"

    if role == "bot":
        role = "assistant"

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "messages")

    fields = []
    values = []

    if "user_id" in columns:
        fields.append("user_id")
        values.append(user_id)

    if "telegram_id" in columns:
        fields.append("telegram_id")
        values.append(telegram_id or user_id)

    if "role" in columns:
        fields.append("role")
        values.append(role)

    if "content" in columns:
        fields.append("content")
        values.append(content)

    if "text" in columns:
        fields.append("text")
        values.append(content)

    if "message_text" in columns:
        fields.append("message_text")
        values.append(content)

    if "is_high_risk" in columns:
        fields.append("is_high_risk")
        values.append(1 if is_high_risk else 0)

    if "created_at" in columns:
        fields.append("created_at")
        values.append(_now())

    placeholders = ", ".join(["?"] * len(values))
    fields_sql = ", ".join(fields)

    cursor.execute(
        f"""
        INSERT INTO messages ({fields_sql})
        VALUES ({placeholders})
        """,
        values,
    )

    message_id = int(cursor.lastrowid)

    conn.commit()
    conn.close()

    return message_id


def add_message(
    user_id: int,
    role: str,
    content: str,
    is_high_risk: bool = False,
) -> int:
    return save_message(
        user_id=user_id,
        role=role,
        content=content,
        is_high_risk=is_high_risk,
    )


def save_user_message(user_id: int, content: str) -> int:
    return save_message(
        user_id=user_id,
        role="user",
        content=content,
    )


def save_assistant_message(user_id: int, content: str) -> int:
    return save_message(
        user_id=user_id,
        role="assistant",
        content=content,
    )


def _row_value(row: sqlite3.Row, key: str, default: Any = None) -> Any:
    try:
        return row[key]
    except Exception:
        return default


def get_recent_messages(
    user_id: Optional[int] = None,
    limit: int = 12,
    telegram_id: Optional[int] = None,
    exclude_high_risk: bool = True,
) -> list[dict[str, str]]:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "messages")
    user_ids = _get_user_identifiers(cursor, int(user_id))

    where_parts = []
    params: list[Any] = []

    if "user_id" in columns:
        placeholders = ", ".join(["?"] * len(user_ids))
        where_parts.append(f"user_id IN ({placeholders})")
        params.extend(user_ids)

    if "telegram_id" in columns:
        where_parts.append("telegram_id = ?")
        params.append(user_id)

    if not where_parts:
        conn.close()
        return []

    where_sql = " OR ".join(where_parts)

    if exclude_high_risk and "is_high_risk" in columns:
        where_sql = f"({where_sql}) AND COALESCE(is_high_risk, 0) = 0"

    order_sql = "ORDER BY id DESC"

    if "created_at" in columns:
        order_sql = "ORDER BY created_at DESC, id DESC"

    cursor.execute(
        f"""
        SELECT *
        FROM messages
        WHERE {where_sql}
        {order_sql}
        LIMIT ?
        """,
        [*params, limit],
    )

    rows = cursor.fetchall()
    conn.close()

    rows = list(reversed(rows))

    result: list[dict[str, str]] = []

    for row in rows:
        role = _row_value(row, "role", "user") or "user"

        if role == "bot":
            role = "assistant"

        content = (
            _row_value(row, "content")
            or _row_value(row, "text")
            or _row_value(row, "message_text")
            or ""
        )

        content = str(content).strip()

        if not content:
            continue

        result.append(
            {
                "role": str(role),
                "content": content,
            }
        )

    return result


def save_diary_entry(
    user_id: Optional[int] = None,
    mood: Optional[int] = None,
    anxiety: Optional[int] = None,
    energy: Optional[int] = None,
    sleep: Optional[int] = None,
    note: str = "",
    telegram_id: Optional[int] = None,
    sleep_quality: Optional[int] = None,
    **kwargs: Any,
) -> int:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        raise ValueError("save_diary_entry: user_id or telegram_id is required")

    if sleep_quality is None:
        sleep_quality = sleep

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "diary_entries")

    fields = []
    values = []

    if "user_id" in columns:
        fields.append("user_id")
        values.append(user_id)

    if "telegram_id" in columns:
        fields.append("telegram_id")
        values.append(telegram_id or user_id)

    if "mood" in columns:
        fields.append("mood")
        values.append(mood)

    if "anxiety" in columns:
        fields.append("anxiety")
        values.append(anxiety)

    if "energy" in columns:
        fields.append("energy")
        values.append(energy)

    if "sleep" in columns:
        fields.append("sleep")
        values.append(sleep)

    if "sleep_quality" in columns:
        fields.append("sleep_quality")
        values.append(sleep_quality)

    if "note" in columns:
        fields.append("note")
        values.append(note)

    if "created_at" in columns:
        fields.append("created_at")
        values.append(_now())

    placeholders = ", ".join(["?"] * len(values))
    fields_sql = ", ".join(fields)

    cursor.execute(
        f"""
        INSERT INTO diary_entries ({fields_sql})
        VALUES ({placeholders})
        """,
        values,
    )

    entry_id = int(cursor.lastrowid)

    conn.commit()
    conn.close()

    return entry_id


def add_diary_entry(
    user_id: int,
    mood: Optional[int],
    anxiety: Optional[int],
    energy: Optional[int],
    sleep: Optional[int],
    note: str,
) -> int:
    return save_diary_entry(
        user_id=user_id,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        sleep=sleep,
        note=note,
    )


def create_diary_entry(
    user_id: int,
    mood: Optional[int],
    anxiety: Optional[int],
    energy: Optional[int],
    sleep: Optional[int],
    note: str,
) -> int:
    return save_diary_entry(
        user_id=user_id,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        sleep=sleep,
        note=note,
    )


def get_diary_entries(
    user_id: Optional[int] = None,
    limit: Optional[int] = None,
    telegram_id: Optional[int] = None,
) -> list[sqlite3.Row]:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "diary_entries")
    user_ids = _get_user_identifiers(cursor, int(user_id))

    where_parts = []
    params: list[Any] = []

    if "user_id" in columns:
        placeholders = ", ".join(["?"] * len(user_ids))
        where_parts.append(f"user_id IN ({placeholders})")
        params.extend(user_ids)

    if "telegram_id" in columns:
        where_parts.append("telegram_id = ?")
        params.append(user_id)

    if not where_parts:
        conn.close()
        return []

    where_sql = " OR ".join(where_parts)

    order_sql = "ORDER BY id DESC"

    if "created_at" in columns:
        order_sql = "ORDER BY created_at DESC, id DESC"

    limit_sql = ""

    if limit is not None:
        limit_sql = "LIMIT ?"
        params.append(limit)

    cursor.execute(
        f"""
        SELECT *
        FROM diary_entries
        WHERE {where_sql}
        {order_sql}
        {limit_sql}
        """,
        params,
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_user_diary_entries(
    user_id: int,
    limit: Optional[int] = None,
) -> list[sqlite3.Row]:
    return get_diary_entries(user_id=user_id, limit=limit)


def get_diary_stats(user_id: int) -> dict[str, Any]:
    entries = get_diary_entries(user_id=user_id)

    if not entries:
        return {
            "count": 0,
            "avg_mood": None,
            "avg_anxiety": None,
            "avg_energy": None,
            "avg_sleep": None,
        }

    def avg(field: str) -> Optional[float]:
        values = []

        for row in entries:
            value = _row_value(row, field)

            if value is not None:
                try:
                    values.append(float(value))
                except Exception:
                    pass

        if not values:
            return None

        return round(sum(values) / len(values), 1)

    return {
        "count": len(entries),
        "avg_mood": avg("mood"),
        "avg_anxiety": avg("anxiety"),
        "avg_energy": avg("energy"),
        "avg_sleep": avg("sleep"),
    }


def save_trigger_entry(
    user_id: Optional[int] = None,
    situation: str = "",
    thought: str = "",
    emotion: str = "",
    body: str = "",
    impulse: str = "",
    need: str = "",
    telegram_id: Optional[int] = None,
    **kwargs: Any,
) -> int:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        raise ValueError("save_trigger_entry: user_id or telegram_id is required")

    if not body:
        body = kwargs.get("body_reaction") or kwargs.get("body_sensation") or ""

    if not need:
        need = kwargs.get("need_text") or kwargs.get("need_value") or ""

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "trigger_entries")

    fields = []
    values = []

    if "user_id" in columns:
        fields.append("user_id")
        values.append(user_id)

    if "telegram_id" in columns:
        fields.append("telegram_id")
        values.append(telegram_id or user_id)

    if "situation" in columns:
        fields.append("situation")
        values.append(situation)

    if "thought" in columns:
        fields.append("thought")
        values.append(thought)

    if "emotion" in columns:
        fields.append("emotion")
        values.append(emotion)

    if "body" in columns:
        fields.append("body")
        values.append(body)

    if "impulse" in columns:
        fields.append("impulse")
        values.append(impulse)

    if "need" in columns:
        fields.append("need")
        values.append(need)

    if "created_at" in columns:
        fields.append("created_at")
        values.append(_now())

    placeholders = ", ".join(["?"] * len(values))
    fields_sql = ", ".join(fields)

    cursor.execute(
        f"""
        INSERT INTO trigger_entries ({fields_sql})
        VALUES ({placeholders})
        """,
        values,
    )

    entry_id = int(cursor.lastrowid)

    conn.commit()
    conn.close()

    return entry_id


def add_trigger_entry(
    user_id: int,
    situation: str,
    thought: str,
    emotion: str,
    body: str,
    impulse: str,
    need: str,
) -> int:
    return save_trigger_entry(
        user_id=user_id,
        situation=situation,
        thought=thought,
        emotion=emotion,
        body=body,
        impulse=impulse,
        need=need,
    )


def create_trigger_entry(
    user_id: int,
    situation: str,
    thought: str,
    emotion: str,
    body: str,
    impulse: str,
    need: str,
) -> int:
    return save_trigger_entry(
        user_id=user_id,
        situation=situation,
        thought=thought,
        emotion=emotion,
        body=body,
        impulse=impulse,
        need=need,
    )


def get_trigger_entries(
    user_id: Optional[int] = None,
    limit: Optional[int] = None,
    telegram_id: Optional[int] = None,
) -> list[sqlite3.Row]:
    if user_id is None:
        user_id = telegram_id

    if user_id is None:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    columns = _get_table_columns(cursor, "trigger_entries")
    user_ids = _get_user_identifiers(cursor, int(user_id))

    where_parts = []
    params: list[Any] = []

    if "user_id" in columns:
        placeholders = ", ".join(["?"] * len(user_ids))
        where_parts.append(f"user_id IN ({placeholders})")
        params.extend(user_ids)

    if "telegram_id" in columns:
        where_parts.append("telegram_id = ?")
        params.append(user_id)

    if not where_parts:
        conn.close()
        return []

    where_sql = " OR ".join(where_parts)

    order_sql = "ORDER BY id DESC"

    if "created_at" in columns:
        order_sql = "ORDER BY created_at DESC, id DESC"

    limit_sql = ""

    if limit is not None:
        limit_sql = "LIMIT ?"
        params.append(limit)

    cursor.execute(
        f"""
        SELECT *
        FROM trigger_entries
        WHERE {where_sql}
        {order_sql}
        {limit_sql}
        """,
        params,
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_user_trigger_entries(
    user_id: int,
    limit: Optional[int] = None,
) -> list[sqlite3.Row]:
    return get_trigger_entries(user_id=user_id, limit=limit)


def get_trigger_stats(user_id: int) -> dict[str, Any]:
    entries = get_trigger_entries(user_id=user_id)

    return {
        "count": len(entries),
    }


def delete_user_data(telegram_id: int) -> int:
    """
    РЈРґР°Р»СЏРµС‚ РґР°РЅРЅС‹Рµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РёР· РѕСЃРЅРѕРІРЅС‹С… С‚Р°Р±Р»РёС† РїСЂРѕРµРєС‚Р°.
    Р’РѕР·РІСЂР°С‰Р°РµС‚ РїСЂРёРјРµСЂРЅРѕРµ РєРѕР»РёС‡РµСЃС‚РІРѕ СѓРґР°Р»С‘РЅРЅС‹С… СЃС‚СЂРѕРє.
    """

    conn = get_connection()
    cursor = conn.cursor()

    deleted_rows = 0

    internal_user_id = _get_internal_user_id(cursor, telegram_id)

    ids_for_delete = [int(telegram_id)]

    if internal_user_id is not None and internal_user_id not in ids_for_delete:
        ids_for_delete.append(internal_user_id)

    tables = [
        "messages",
        "diary_entries",
        "trigger_entries",
    ]

    for table_name in tables:
        try:
            columns = _get_table_columns(cursor, table_name)
        except Exception:
            continue

        if "user_id" in columns:
            placeholders = ", ".join(["?"] * len(ids_for_delete))

            cursor.execute(
                f"""
                DELETE FROM {table_name}
                WHERE user_id IN ({placeholders})
                """,
                ids_for_delete,
            )

            if cursor.rowcount and cursor.rowcount > 0:
                deleted_rows += cursor.rowcount

        if "telegram_id" in columns:
            cursor.execute(
                f"""
                DELETE FROM {table_name}
                WHERE telegram_id = ?
                """,
                (telegram_id,),
            )

            if cursor.rowcount and cursor.rowcount > 0:
                deleted_rows += cursor.rowcount

    cursor.execute(
        """
        DELETE FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    if cursor.rowcount and cursor.rowcount > 0:
        deleted_rows += cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_rows


# РРЅРёС†РёР°Р»РёР·РёСЂСѓРµРј Р±Р°Р·Сѓ РїСЂРё РёРјРїРѕСЂС‚Рµ РјРѕРґСѓР»СЏ.
init_db()
def get_trigger_count(telegram_id: int) -> int:
    """
    Р’РѕР·РІСЂР°С‰Р°РµС‚ РєРѕР»РёС‡РµСЃС‚РІРѕ Р·Р°РїРёСЃРµР№ СЂР°Р·Р±РѕСЂР° С‚СЂРёРіРіРµСЂРѕРІ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ.

    РЎРѕРІРјРµСЃС‚РёРјР°СЏ С„СѓРЅРєС†РёСЏ РґР»СЏ СЃС‚Р°СЂРѕРіРѕ handlers/trigger.py,
    РєРѕС‚РѕСЂС‹Р№ РёРјРїРѕСЂС‚РёСЂСѓРµС‚ get_trigger_count.
    Р Р°Р±РѕС‚Р°РµС‚ Рё СЃРѕ СЃС…РµРјРѕР№ С‡РµСЂРµР· telegram_id, Рё СЃРѕ СЃС…РµРјРѕР№ С‡РµСЂРµР· user_id.
    """
    import sqlite3

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        trigger_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(trigger_entries)").fetchall()
        }

        conditions = []
        params = []

        if "telegram_id" in trigger_columns:
            conditions.append("telegram_id = ?")
            params.append(telegram_id)

        if "user_id" in trigger_columns:
            # Р’ РЅРѕРІС‹С… РІРµСЂСЃРёСЏС… user_id РјРѕР¶РµС‚ Р±С‹С‚СЊ РІРЅСѓС‚СЂРµРЅРЅРёРј id РёР· С‚Р°Р±Р»РёС†С‹ users
            user_row = cursor.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()

            if user_row:
                internal_user_id = user_row[0]
                conditions.append("user_id = ?")
                params.append(internal_user_id)

            # РќР° СЃР»СѓС‡Р°Р№ СЃС‚Р°СЂС‹С…/СЃРјРµС€Р°РЅРЅС‹С… Р·Р°РїРёСЃРµР№, РіРґРµ РІ user_id РјРѕРі РїРѕРїР°СЃС‚СЊ telegram_id
            conditions.append("user_id = ?")
            params.append(telegram_id)

        if not conditions:
            return 0

        query = f"""
            SELECT COUNT(*)
            FROM trigger_entries
            WHERE {" OR ".join(conditions)}
        """

        result = cursor.execute(query, params).fetchone()
        return int(result[0]) if result else 0

    finally:
        conn.close()

def get_sleep_stats(telegram_id: int, limit: int = 30) -> dict:
    """
    Возвращает мягкую статистику сна по дневнику пользователя.

    Совместимая функция для map_builder.py.
    Работает со старыми/смешанными схемами:
    - если в diary_entries есть telegram_id;
    - если в diary_entries есть user_id;
    - если user_id связан с users.id.
    """
    import sqlite3

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        diary_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(diary_entries)").fetchall()
        }

        if "sleep" not in diary_columns:
            return {
                "count": 0,
                "average": None,
                "min": None,
                "max": None,
                "values": [],
            }

        conditions = []
        params = []

        if "telegram_id" in diary_columns:
            conditions.append("telegram_id = ?")
            params.append(telegram_id)

        if "user_id" in diary_columns:
            user_row = cursor.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()

            if user_row:
                internal_user_id = user_row[0]
                conditions.append("user_id = ?")
                params.append(internal_user_id)

            # На случай старой/смешанной схемы, где user_id мог быть равен telegram_id
            conditions.append("user_id = ?")
            params.append(telegram_id)

        if not conditions:
            return {
                "count": 0,
                "average": None,
                "min": None,
                "max": None,
                "values": [],
            }

        order_column = "created_at" if "created_at" in diary_columns else "id"

        query = f"""
            SELECT sleep
            FROM diary_entries
            WHERE ({' OR '.join(conditions)})
              AND sleep IS NOT NULL
              AND sleep != ''
            ORDER BY {order_column} DESC
            LIMIT ?
        """

        params.append(limit)

        rows = cursor.execute(query, params).fetchall()

        values = []

        for row in rows:
            raw_value = row[0]

            try:
                value = float(raw_value)
                values.append(value)
            except (TypeError, ValueError):
                continue

        if not values:
            return {
                "count": 0,
                "average": None,
                "min": None,
                "max": None,
                "values": [],
            }

        average = sum(values) / len(values)

        return {
            "count": len(values),
            "average": round(average, 2),
            "min": min(values),
            "max": max(values),
            "values": values,
        }

    finally:
        conn.close()

def get_user_message_count(telegram_id: int) -> int:
    """
    Возвращает количество сообщений пользователя в таблице messages.

    Совместимая функция для handlers/info.py.
    Работает со схемами:
    - messages.telegram_id;
    - messages.user_id, где user_id = users.id;
    - messages.user_id, где user_id мог быть равен telegram_id.
    """
    import sqlite3

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        message_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(messages)").fetchall()
        }

        conditions = []
        params = []

        if "telegram_id" in message_columns:
            conditions.append("telegram_id = ?")
            params.append(telegram_id)

        if "user_id" in message_columns:
            user_row = cursor.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()

            if user_row:
                internal_user_id = user_row[0]
                conditions.append("user_id = ?")
                params.append(internal_user_id)

            # На случай старой/смешанной схемы, где user_id мог быть равен telegram_id
            conditions.append("user_id = ?")
            params.append(telegram_id)

        if not conditions:
            return 0

        query = f"""
            SELECT COUNT(*)
            FROM messages
            WHERE {' OR '.join(conditions)}
        """

        result = cursor.execute(query, params).fetchone()

        return int(result[0]) if result else 0

    finally:
        conn.close()

def add_user(telegram_id: int, username=None, first_name=None) -> int:
    """
    Создаёт пользователя, если его нет, или обновляет username/first_name.
    Возвращает внутренний id из таблицы users.

    Совместимая функция для старых обработчиков, включая fallback.py.
    """
    import sqlite3
    from datetime import datetime

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    now = datetime.now().isoformat(timespec="seconds")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        user_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(users)").fetchall()
        }

        row = cursor.execute(
            "SELECT id FROM users WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()

        if row:
            internal_user_id = int(row[0])

            update_parts = []
            params = []

            if "username" in user_columns:
                update_parts.append("username = ?")
                params.append(username)

            if "first_name" in user_columns:
                update_parts.append("first_name = ?")
                params.append(first_name)

            if "updated_at" in user_columns:
                update_parts.append("updated_at = ?")
                params.append(now)

            if update_parts:
                params.append(telegram_id)
                cursor.execute(
                    f"UPDATE users SET {', '.join(update_parts)} WHERE telegram_id = ?",
                    params,
                )
                conn.commit()

            return internal_user_id

        insert_columns = []
        values = []

        if "telegram_id" in user_columns:
            insert_columns.append("telegram_id")
            values.append(telegram_id)

        if "username" in user_columns:
            insert_columns.append("username")
            values.append(username)

        if "first_name" in user_columns:
            insert_columns.append("first_name")
            values.append(first_name)

        if "age_confirmed" in user_columns:
            insert_columns.append("age_confirmed")
            values.append(0)

        if "consent_accepted" in user_columns:
            insert_columns.append("consent_accepted")
            values.append(0)

        if "created_at" in user_columns:
            insert_columns.append("created_at")
            values.append(now)

        if "updated_at" in user_columns:
            insert_columns.append("updated_at")
            values.append(now)

        placeholders = ", ".join(["?"] * len(insert_columns))

        cursor.execute(
            f"""
            INSERT INTO users ({', '.join(insert_columns)})
            VALUES ({placeholders})
            """,
            values,
        )

        conn.commit()

        return int(cursor.lastrowid)

    finally:
        conn.close()


def save_message(telegram_id: int, role: str, content: str) -> None:
    """
    Сохраняет сообщение в таблицу messages.

    Совместимая функция для fallback.py.
    Работает с разными схемами:
    - messages.telegram_id;
    - messages.user_id;
    - messages.content / text / message.
    """
    import sqlite3
    from datetime import datetime

    if content is None:
        return

    content = str(content).strip()

    if not content:
        return

    # Дополнительная защита: high-risk пользовательские сообщения не сохраняем в AI-историю.
    try:
        from safety import is_high_risk

        if role == "user" and is_high_risk(content):
            return
    except Exception:
        pass

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    now = datetime.now().isoformat(timespec="seconds")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        internal_user_id = add_user(telegram_id)

        message_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(messages)").fetchall()
        }

        insert_columns = []
        values = []

        if "telegram_id" in message_columns:
            insert_columns.append("telegram_id")
            values.append(telegram_id)

        if "user_id" in message_columns:
            insert_columns.append("user_id")
            values.append(internal_user_id)

        if "role" in message_columns:
            insert_columns.append("role")
            values.append(role)

        if "content" in message_columns:
            insert_columns.append("content")
            values.append(content)
        elif "text" in message_columns:
            insert_columns.append("text")
            values.append(content)
        elif "message" in message_columns:
            insert_columns.append("message")
            values.append(content)
        else:
            return

        if "created_at" in message_columns:
            insert_columns.append("created_at")
            values.append(now)

        placeholders = ", ".join(["?"] * len(insert_columns))

        cursor.execute(
            f"""
            INSERT INTO messages ({', '.join(insert_columns)})
            VALUES ({placeholders})
            """,
            values,
        )

        conn.commit()

    finally:
        conn.close()


def get_recent_messages(telegram_id: int, limit: int = 12) -> list:
    """
    Возвращает последние сообщения пользователя для AI-контекста.

    Формат:
    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]

    Совместимая функция для fallback.py.
    """
    import sqlite3

    db_path = (
        globals().get("DB_PATH")
        or globals().get("DATABASE_PATH")
        or globals().get("DATABASE")
        or "data/opora.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        message_columns = {
            row[1]
            for row in cursor.execute("PRAGMA table_info(messages)").fetchall()
        }

        if "role" not in message_columns:
            return []

        if "content" in message_columns:
            content_column = "content"
        elif "text" in message_columns:
            content_column = "text"
        elif "message" in message_columns:
            content_column = "message"
        else:
            return []

        conditions = []
        params = []

        if "telegram_id" in message_columns:
            conditions.append("telegram_id = ?")
            params.append(telegram_id)

        if "user_id" in message_columns:
            user_row = cursor.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()

            if user_row:
                internal_user_id = int(user_row[0])
                conditions.append("user_id = ?")
                params.append(internal_user_id)

            # На случай старой/смешанной схемы, где user_id мог быть равен telegram_id
            conditions.append("user_id = ?")
            params.append(telegram_id)

        if not conditions:
            return []

        order_column = "created_at" if "created_at" in message_columns else "id"

        query = f"""
            SELECT role, {content_column}
            FROM messages
            WHERE ({' OR '.join(conditions)})
            ORDER BY {order_column} DESC
            LIMIT ?
        """

        params.append(limit)

        rows = cursor.execute(query, params).fetchall()

        messages = []

        for role, content in reversed(rows):
            if role not in ("user", "assistant", "system"):
                continue

            if content is None:
                continue

            content = str(content).strip()

            if not content:
                continue

            messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        return messages

    finally:
        conn.close()
