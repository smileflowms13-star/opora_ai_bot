import pytest
from datetime import date, timedelta
from services.streak_service import process_streak
from database import get_connection

@pytest.fixture(autouse=True)
def clean_db(test_db_path):
    conn = get_connection()
    conn.execute("DELETE FROM streaks")
    conn.commit()
    conn.close()

def test_process_streak_first_time():
    msg = process_streak(123)
    assert msg is not None
    assert "1" in msg
    conn = get_connection()
    row = conn.execute("SELECT * FROM streaks WHERE telegram_id=123").fetchone()
    assert row is not None
    assert row["current_streak"] == 1
    conn.close()

def test_process_streak_consecutive():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO streaks (telegram_id, current_streak, longest_streak, last_action_date) VALUES (?, 3, 3, ?)",
        (456, yesterday)
    )
    conn.commit()
    conn.close()

    msg = process_streak(456)
    assert "4" in msg  # стало 4
    conn = get_connection()
    row = conn.execute("SELECT * FROM streaks WHERE telegram_id=456").fetchone()
    assert row["current_streak"] == 4
    conn.close()

def test_process_streak_same_day_no_change():
    today = date.today().isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO streaks (telegram_id, current_streak, longest_streak, last_action_date) VALUES (?, 5, 5, ?)",
        (789, today)
    )
    conn.commit()
    conn.close()

    msg = process_streak(789)
    # Теперь process_streak всегда возвращает сообщение (день 5)
    assert "День 5" in msg or "5" in msg
    # Проверяем, что стрик не изменился
    conn = get_connection()
    row = conn.execute("SELECT * FROM streaks WHERE telegram_id=789").fetchone()
    assert row["current_streak"] == 5
    conn.close()

def test_process_streak_level_up():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO streaks (telegram_id, current_streak, longest_streak, last_action_date) VALUES (?, 6, 6, ?)",
        (111, yesterday)
    )
    conn.commit()
    conn.close()

    msg = process_streak(111)
    assert "🌼" in msg  # повышение до цветка