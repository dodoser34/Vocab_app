from ..db.db import get_conn

def get_latest_words(limit=10):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, english, translation, created_at
        FROM words
        ORDER BY datetime(created_at) DESC
        LIMIT ?
    """, (limit,))
    words = cursor.fetchall()
    conn.close()
    return words
