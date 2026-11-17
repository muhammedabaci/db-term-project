from backend.db_connection import get_connection


def get_comments_by_airport(airport_ref, limit=20):
    """Returns the latest comments of one airport."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, thread_ref, airport_ref, airport_ident,
                   comment_date, member_nickname, subject, body
            FROM airport_comments
            WHERE airport_ref = %s
            ORDER BY comment_date DESC
            LIMIT %s
            """,
            (airport_ref, limit),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Hata (get_comments_by_airport): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_comment(comment_id, thread_ref, airport_ref, airport_ident,
                   member_nickname, subject, body):
    """Inserts one comment (date = now). Returns True on success."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO airport_comments
                (id, thread_ref, airport_ref, airport_ident,
                 comment_date, member_nickname, subject, body)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s)
            """,
            (comment_id, thread_ref, airport_ref, airport_ident,
             member_nickname, subject, body),
        )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Hata (insert_comment): {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()