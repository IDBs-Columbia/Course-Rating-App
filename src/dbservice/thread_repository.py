import psycopg2
import psycopg2.extras
import dbservice.config as config
from datetime import datetime

def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor


def find_all_thread_by_course(call_number):
    conn, cur = get_connection()

    sql = """
            SELECT *
            FROM THREAD
            WHERE CALL_NUMBER = (%s)
        """

    cur.execute(sql, [call_number])

    res = cur.fetchall()
    conn.close()

    return res


def get_thread_by_id(id):
    conn, cur = get_connection()
    sql = """
            SELECT T.*, C.COURSE_NUMBER
            FROM THREAD AS T
            JOIN COURSE AS C ON T.CALL_NUMBER = C.CALL_NUMBER
            WHERE id = (%s)
        """
    cur.execute(sql, [id])
    res = cur.fetchone()
    conn.close()
    return res

def add_thread(title, description, user_id, call_number):
    conn, cur = get_connection()
    id_hash = str(hash(description))[:6]
    id = abs(int(id_hash))

    date = "NOW()"
    sql = """
            INSERT INTO THREAD(id, title, description, date, user_id, call_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    cur.execute(sql, (id, title, description, date, user_id, call_number))
    conn.commit()
    conn.close()

def check_user_like_thread(uid, tid):
    conn, cur = get_connection()
    sql = """
                SELECT is_helpful
                FROM USER_REGULAR_RATES_THREAD
                WHERE user_id = (%s) and thread_id = (%s)
            """
    cur.execute(sql, [uid, tid])
    res = cur.fetchone()
    conn.close()

    if not res: return False, False

    return True, res['is_helpful']

def user_rate_thread(uid, tid, like):
    conn, cur = get_connection()
    sql = """
        INSERT INTO USER_REGULAR_RATES_THREAD(is_helpful, user_id, thread_id)
        VALUES ((%s), (%s), (%s))
    """
    cur.execute(sql, [like, uid, tid])
    conn.commit()
    conn.close()
    return
def add_new_thread(title, desc, date, uid, call_number):
    conn, cur = get_connection()
    sql = """
            INSERT INTO THREAD(title, description, date, user_id, call_number)
            VALUES ((%s), (%s), (%s), (%s), (%s))
        """
    cur.execute(sql, [title, desc, date, uid, call_number])
    conn.commit()
    conn.close()
    return
