import sqlite3
from pathlib import Path
from src.config import Config


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite telemetry table if it doesn't already exist."""
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS request_telemetry (
                request_id TEXT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                query TEXT NOT NULL,
                category TEXT NOT NULL,
                complexity TEXT NOT NULL,
                route TEXT NOT NULL,
                model TEXT NOT NULL,
                confidence REAL NOT NULL,
                fallback_triggered INTEGER NOT NULL,
                fallback_reason TEXT,
                routing_latency_ms REAL NOT NULL,
                generation_latency_ms REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                estimated_cost_usd REAL
            );
        """)
    conn.close()
