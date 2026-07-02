import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("database") / "predictions.db"


def create_database():
    """
    Creates the SQLite database and predictions table
    if it does not already exist.
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            priority TEXT,

            category TEXT,

            sub_category TEXT,

            department TEXT,

            group_name TEXT,

            site TEXT,

            request_type TEXT,

            created_day TEXT,

            created_month TEXT,

            created_hour INTEGER,

            prediction INTEGER,

            probability REAL,

            risk_level TEXT

        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    priority,
    category,
    sub_category,
    department,
    group,
    site,
    request_type,
    created_day,
    created_month,
    created_hour,
    prediction,
    probability,
    risk_level
):
    """
    Saves one prediction into the SQLite database.
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (

            timestamp,
            priority,
            category,
            sub_category,
            department,
            group_name,
            site,
            request_type,
            created_day,
            created_month,
            created_hour,
            prediction,
            probability,
            risk_level

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            priority,
            category,
            sub_category,
            department,
            group,
            site,
            request_type,
            created_day,
            created_month,
            created_hour,
            int(prediction),
            float(probability),
            risk_level
        )
    )

    conn.commit()
    conn.close()

def get_all_predictions():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
