import pytest
from services.diary_service import save_and_process_diary_entry
from database import get_connection

@pytest.fixture(autouse=True)
def clean_db(test_db_path):
    conn = get_connection()
    conn.execute("DELETE FROM diary_entries")
    conn.execute("DELETE FROM streaks")
    conn.commit()
    conn.close()

def test_save_diary_entry_and_streak():
    telegram_id = 999
    streak_data, streak_msg = save_and_process_diary_entry(
        telegram_id=telegram_id,
        mood_score=7,
        anxiety_score=3,
        energy_score=8,
        sleep_quality="хорошо",
        note="Хороший день"
    )
    assert streak_msg is not None
    assert "1" in streak_msg  # первый день

    # Проверяем запись в БД
    conn = get_connection()
    row = conn.execute("SELECT * FROM diary_entries WHERE telegram_id=?", (telegram_id,)).fetchone()
    assert row is not None
    assert row["mood"] == 7
    assert row["note"] == "Хороший день"
    conn.close()