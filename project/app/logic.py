from datetime import datetime
from .db import get_conn

# ------------------ Add Word ------------------
def add_word(english, translation, type_=None, past_simple=None, past_participle=None, example=None, tags=None):
    """
    Adds a word to the database.
    """
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

# ------------------ Update Progress ------------------
def update_progress(word_id, correct=True):
    """Updates progress and last reviewed date for a word."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_count, incorrect_count FROM progress WHERE word_id=?", (word_id,))
    record = cursor.fetchone()
    now = datetime.now().isoformat()  # store as ISO string for SQLite

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

# ------------------ Get Words for Training ------------------
def get_words(limit=100, errors_only=False):
    """
    Returns words for training.
    Sorted: new words + frequently wrong words.
    """
    conn = get_conn()
    cursor = conn.cursor()
    
    if errors_only:
        cursor.execute("""
            SELECT w.id, w.english, w.translation, COALESCE(p.correct_count,0), COALESCE(p.incorrect_count,0)
            FROM words w
            JOIN progress p ON w.id = p.word_id
            WHERE p.incorrect_count > 0
            ORDER BY p.incorrect_count DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT w.id, w.english, w.translation, COALESCE(p.correct_count,0), COALESCE(p.incorrect_count,0)
            FROM words w
            LEFT JOIN progress p ON w.id = p.word_id
            ORDER BY w.id DESC
            LIMIT ?
        """, (limit,))

    words = cursor.fetchall()
    conn.close()

    # Prioritize words: new + frequently wrong
    def priority(x):
        correct, incorrect = x[3], x[4]
        total = correct + incorrect
        if total == 0:
            return 1.0  # new word
        return incorrect / total + 0.01

    words.sort(key=priority, reverse=True)
    return words

# ------------------ Last Added Words ------------------
def get_last_words(limit=10):
    """Returns only the last added words (newest first), ignoring training progress."""
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

# ------------------ Full Dictionary ------------------
def get_full_dictionary(order_by_time=False):
    """
    Returns only added words with translations.
    By default, sorted alphabetically.
    If order_by_time=True, sorted by creation time (newest first).
    Training progress is ignored.
    """
    conn = get_conn()
    cursor = conn.cursor()
    if order_by_time:
        cursor.execute("""
            SELECT id, english, translation, created_at
            FROM words
            ORDER BY datetime(created_at) DESC
        """)
    else:
        cursor.execute("""
            SELECT id, english, translation
            FROM words
            ORDER BY english ASC
        """)
    words = cursor.fetchall()
    conn.close()
    return words


# ------------------ Get Statistics ------------------
def get_statistics(min_attempts=0):
    """
    Returns overall and daily statistics.
    """
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(correct_count), SUM(incorrect_count) FROM progress")
    progress = cursor.fetchone()
    total_correct = progress[0] or 0
    total_incorrect = progress[1] or 0

    cursor.execute("""
        SELECT DATE(last_reviewed), SUM(correct_count), SUM(incorrect_count)
        FROM progress
        WHERE last_reviewed IS NOT NULL
        GROUP BY DATE(last_reviewed)
        ORDER BY DATE(last_reviewed)
    """)
    daily = cursor.fetchall()
    conn.close()

    accuracy = round(total_correct / (total_correct + total_incorrect) * 100, 2) if (total_correct + total_incorrect) > 0 else 0

    return {
        "total_words": total_words,
        "total_correct": total_correct,
        "total_incorrect": total_incorrect,
        "accuracy": accuracy,
        "daily": daily
    }