import os
import tempfile
import pytest
from pathlib import Path
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="session")
def test_db_path():
    """Создаёт временную БД и применяет миграции Alembic."""
    # Создаём временный файл
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["OPORA_DB_PATH"] = path

    # Применяем миграции
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"
    cfg = Config(str(alembic_ini))
    # Устанавливаем путь к БД в конфигурации alembic
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{path}")
    command.upgrade(cfg, "head")

    yield path

    # Удаляем временную БД
    if os.path.exists(path):
        os.unlink(path)
    os.environ.pop("OPORA_DB_PATH", None)