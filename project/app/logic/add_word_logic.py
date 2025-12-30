from ..db.db import get_conn

def add_word(english, translation, type_=None, past_simple=None, past_participle=None, example=None, tags=None):
    english = english.strip()
    translation = translation.strip()
    if not english or not translation:
        return

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words (english, translation, type, past_simple, past_participle, example, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (english, translation, type_, past_simple, past_participle, example, tags))
    conn.commit()
    conn.close()

