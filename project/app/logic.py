from datetime import datetime, timedelta
from app.db import get_conn

def add_word(english, translation, type_=None, past_simple=None, past_participle=None, example=None, tags=None):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words (english, translation, type, past_simple, past_participle, example, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (english, translation, type_, past_simple, past_participle, example, tags))
    conn.commit()
    conn.close()

def update_progress(word_id, correct=True):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress WHERE word_id=?", (word_id,))
    record = cursor.fetchone()
    if record:
        correct_count = record[2] + (1 if correct else 0)
        incorrect_count = record[3] + (0 if correct else 1)
        cursor.execute("""
            UPDATE progress
            SET correct_count=?, incorrect_count=?, last_reviewed=?
            WHERE word_id=?
        """, (correct_count, incorrect_count, datetime.now(), word_id))
    else:
        cursor.execute("""
            INSERT INTO progress (word_id, correct_count, incorrect_count, last_reviewed)
            VALUES (?, ?, ?, ?)
        """, (word_id, 1 if correct else 0, 0 if correct else 1, datetime.now()))
    conn.commit()
    conn.close()

def get_words(limit=10, tags=None, types=None, errors_only=False):
    conn = get_conn()
    cursor = conn.cursor()
    if errors_only:
        cursor.execute("""
            SELECT w.id, w.english, w.translation, p.correct_count, p.incorrect_count
            FROM words w
            JOIN progress p ON w.id = p.word_id
            WHERE p.incorrect_count > 0
            ORDER BY p.incorrect_count DESC
        """)
    else:
        query = "SELECT w.id, w.english, w.translation, COALESCE(p.correct_count,0), COALESCE(p.incorrect_count,0) FROM words w LEFT JOIN progress p ON w.id = p.word_id"
        conditions = []
        params = []
        if tags:
            conditions.append("w.tags LIKE ?")
            params.append(f"%{tags}%")
        if types:
            conditions.append("w.type LIKE ?")
            params.append(f"%{types}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cursor.execute(query, params)
    words = cursor.fetchall()
    conn.close()
    words.sort(key=lambda x: (x[4]/(x[3]+x[4]+1) if x[4] else 0), reverse=True)
    return words[:limit]

def get_statistics():
    conn = get_conn()
    cursor = conn.cursor()
    # Общее
    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(correct_count), SUM(incorrect_count) FROM progress")
    progress = cursor.fetchone()
    total_correct = progress[0] if progress[0] else 0
    total_incorrect = progress[1] if progress[1] else 0

    # Статистика по дням
    cursor.execute("""
        SELECT DATE(last_reviewed), SUM(correct_count), SUM(incorrect_count)
        FROM progress
        WHERE last_reviewed IS NOT NULL
        GROUP BY DATE(last_reviewed)
        ORDER BY DATE(last_reviewed)
    """)
    daily = cursor.fetchall()
    conn.close()
    return {
        "total_words": total_words,
        "total_correct": total_correct,
        "total_incorrect": total_incorrect,
        "accuracy": round(total_correct/(total_correct+total_incorrect)*100,2) if (total_correct+total_incorrect)>0 else 0,
        "daily": daily
    }
