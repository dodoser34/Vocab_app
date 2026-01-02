import sqlite3
from ..db.db import get_conn

def add_word(
    english,
    translation,
    type_=None,
    past_simple=None,
    past_participle=None,
    example=None,
    tags=None
):
    english = english.strip().lower()
    translation = translation.strip()
    if not english or not translation:
        return False, "Empty fields"

    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO words (
                english, translation, type,
                past_simple, past_participle,
                example, tags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            english, translation, type_,
            past_simple, past_participle,
            example, tags
        ))
        conn.commit()
        return True, "Word added"
    except sqlite3.IntegrityError:
        return False, "Word already exists"
    finally:
        conn.close()
