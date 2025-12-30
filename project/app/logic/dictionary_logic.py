from ..db.db import get_conn


def get_full_dictionary(order_by_time=False):

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
