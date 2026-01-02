from ..db.db import get_conn
from datetime import datetime, timedelta

def get_training_stats():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_count, incorrect_count FROM progress")
    data = cursor.fetchall()
    conn.close()

    correct = sum(r[0] for r in data)
    incorrect = sum(r[1] for r in data)
    total = correct + incorrect
    avg_percent = int(correct / total * 100) if total > 0 else 0

    return {"correct": correct, "incorrect": incorrect, "average_percent": avg_percent}


def get_streaks():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT DATE(last_reviewed) FROM progress ORDER BY last_reviewed")
    date_rows = cursor.fetchall()
    dates = [datetime.fromisoformat(r[0]).date() for r in date_rows if r[0] is not None]
    conn.close()

    if not dates:
        return {"current_streak": 0, "total_days": 0, "streak_history": []}

    dates = sorted(set(dates))
    streak_history = []
    current_streak = 1
    max_streak = 1

    for i in range(len(dates)):
        if i == 0:
            streak_history.append(1)
            continue
        if dates[i] - dates[i-1] == timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1
        streak_history.append(current_streak)
        max_streak = max(max_streak, current_streak)

    total_days = len(dates)

    return {
        "current_streak": current_streak,
        "total_days": total_days,
        "streak_history": streak_history
    }
