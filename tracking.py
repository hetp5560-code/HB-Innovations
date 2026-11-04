import json
from config import get_db_connection


def init_tracking_tables():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resume_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                template_name TEXT NOT NULL,
                action TEXT NOT NULL,
                snapshot_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activity_logs(user_id, created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resume_user_date ON resume_history(user_id, created_at)")
        conn.commit()
    finally:
        conn.close()


def log_activity(user_id, action, details=None):
    if not user_id:
        return
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, action, details)
        )
        conn.commit()
    except Exception as error:
        print("Activity log error:", repr(error))
    finally:
        conn.close()


def save_resume_history(user_id, template_name, action, data):
    snapshot = json.dumps(data, ensure_ascii=False, default=str)
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO resume_history (user_id, template_name, action, snapshot_json) VALUES (?, ?, ?, ?)",
            (user_id, str(template_name), action, snapshot)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as error:
        print("Resume history error:", repr(error))
        return None
    finally:
        conn.close()
