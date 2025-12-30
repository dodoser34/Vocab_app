from ..db.db import get_conn

def get_statistics():
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
