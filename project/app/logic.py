from datetime import datetime
from .db import get_conn


# ------------------ Добавление слова ------------------
def add_word(english, translation, type_=None, past_simple=None, past_participle=None, example=None, tags=None):
    """
    Добавляет слово в базу.
    """
    english = english.strip()
    translation = translation.strip()
    if not english or not translation:
        return  # не добавляем пустые слова

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words (english, translation, type, past_simple, past_participle, example, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (english, translation, type_, past_simple, past_participle, example, tags))
    conn.commit()
    conn.close()

# ------------------ Обновление прогресса ------------------
def update_progress(word_id, correct=True):
    """Обновляет прогресс слова и дату последнего ответа"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_count, incorrect_count FROM progress WHERE word_id=?", (word_id,))
    record = cursor.fetchone()
    now = datetime.now()

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

# ------------------ Получение слов для тренировки ------------------
def get_words(limit=100, errors_only=False):
    """
    Возвращает список слов для тренировки.
    Сортировка: новые слова + слова с ошибками чаще.
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

    # Приоритет слов: новые + слова с ошибками
    def word_priority(x):
        correct, incorrect = x[3], x[4]
        total = correct + incorrect
        if total == 0:
            return 1.0
        return incorrect / total + 0.01

    words.sort(key=word_priority, reverse=True)
    return words

# ------------------ Последние добавленные слова ------------------
def get_last_words(limit=10):
    """Возвращает последние добавленные слова"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, english, translation
        FROM words
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    words = cursor.fetchall()
    conn.close()
    return words

# ------------------ Полный словарь ------------------
def get_full_dictionary():
    """Возвращает все слова с переводами"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, english, translation
        FROM words
        ORDER BY english ASC
    """)
    words = cursor.fetchall()
    conn.close()
    return words

# ------------------ Статистика ------------------
def get_statistics(min_attempts=0):
    """
    Возвращает общую статистику и по дням.
    min_attempts - игнорировать слова с меньше чем min_attempts попыток
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
