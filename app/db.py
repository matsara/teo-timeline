import sqlite3
from contextlib import contextmanager
from pathlib import Path


DB_PATH = Path("teo.db")


@contextmanager
def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alertas (
                id TEXT PRIMARY KEY,
                ticket TEXT NOT NULL,
                evento TEXT NOT NULL,
                status TEXT NOT NULL,
                descricao_timeline TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS acionamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alerta_id TEXT NOT NULL,
                nome TEXT NOT NULL,
                time TEXT NOT NULL,
                horario TEXT,
                atendeu TEXT,
                status_acionamento TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (alerta_id) REFERENCES alertas(id) ON DELETE CASCADE
            )
            """
        )

        # Backward-compatible migrations for existing local DB files.
        alerta_cols = {
            row["name"] for row in conn.execute("PRAGMA table_info(alertas)").fetchall()
        }
        if "descricao_timeline" not in alerta_cols:
            conn.execute("ALTER TABLE alertas ADD COLUMN descricao_timeline TEXT DEFAULT ''")

        acion_cols = {
            row["name"] for row in conn.execute("PRAGMA table_info(acionamentos)").fetchall()
        }
        if "status_acionamento" not in acion_cols:
            conn.execute("ALTER TABLE acionamentos ADD COLUMN status_acionamento TEXT DEFAULT ''")
