from ..db.db import get_conn
from datetime import datetime
import random

def get_training_words(limit=25, errors_only=False):
    conn = get_conn()
    cursor = conn.cursor()

    if errors_only:
        cursor.execute("""
            SELECT w.id, w.english, w.translation,
            COALESCE(p.correct_count,0), COALESCE(p.incorrect_count,0)
            FROM words w
            JOIN progress p ON w.id = p.word_id
            WHERE p.incorrect_count > 0
        """)
    else:
        cursor.execute("""
            SELECT w.id, w.english, w.translation,
            COALESCE(p.correct_count,0), COALESCE(p.incorrect_count,0)
            FROM words w
            LEFT JOIN progress p ON w.id = p.word_id
        """)

    words = cursor.fetchall()
    conn.close()

    def priority(x):
        correct, incorrect = x[3], x[4]
        total = correct + incorrect
        if total == 0:
            return 1.0
        return (incorrect + 1) / (total + 1) + 0.01

    weighted_words = [(w, priority(w)) for w in words]

    selected = []
    while len(selected) < min(limit, len(weighted_words)):
        w, _ = random.choices(weighted_words, weights=[pr for _, pr in weighted_words])[0]
        if w not in selected:
            selected.append(w)

    selected.sort(key=lambda x: priority(x), reverse=True)
    return selected

def update_progress(word_id, correct=True):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_count, incorrect_count FROM progress WHERE word_id=?", (word_id,))
    record = cursor.fetchone()
    now = datetime.now().isoformat()

    if record:
        correct_count = record[0] + (1 if correct else 0)
        incorrect_count = record[1] + (0 if correct else 1)
        cursor.execute("""
            UPDATE progress
            SET correct_count=?, incorrect_count=?, last_reviewed=?
            WHERE word_id=?
        """, (correct_count, incorrect_count, now, word_id))
    else:
        cursor.execute("""
            INSERT INTO progress (word_id, correct_count, incorrect_count, last_reviewed)
            VALUES (?, ?, ?, ?)
        """, (word_id, 1 if correct else 0, 0 if correct else 1, now))

    conn.commit()
    conn.close()

def check_answer(word_id, user_input, correct_translation):
    ok = user_input.strip().lower() == correct_translation.strip().lower()
    update_progress(word_id, ok)
    return ok