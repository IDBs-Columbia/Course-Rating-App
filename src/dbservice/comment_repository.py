import psycopg2
import psycopg2.extras
import dbservice.config as config
from datetime import datetime, date

from random import randint

from random import randint


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor

def get_comments():
    conn, cur = get_connection()
    sql = """
        SELECT *
        FROM comment
    """
    cur.execute(sql)
    res = cur.fetchall()
    conn.close()
    return res

def get_likes_dislikes():
    conn, cur = get_connection()
    sql = """
        SELECT *
        FROM comment
    """
    cur.execute(sql)
    res = cur.fetchall()
    conn.close()
    return res

def get_author_by_comment_id(comment_id):
    conn, cur = get_connection()
    sql = """
        SELECT *
        FROM USER
        WHERE ID = (
            SELECT user_id
            FROM Comment
            WHERE id = (%s)
        )
    """
    cur.execute(sql, [comment_id])
    res = cur.fetchone()
    conn.close()
    return res


def find_main_comment_by_thread(thread_id):
    conn, cur = get_connection()

    sql = """
                SELECT *
                FROM COMMENT
                WHERE THREAD_ID = (%s) AND REPLY_ID IS NULL
            """

    cur.execute(sql, [thread_id])

    res = cur.fetchall()
    conn.close()

    for i, main in enumerate(res):
        sub = find_sub_comment_by_main_comment(main['id'])
        res[i]['sub'] = sub

    return res


def find_sub_comment_by_main_comment(main_id):
    conn, cur = get_connection()
    sql = """
        SELECT *
        FROM COMMENT
        WHERE REPLY_ID = (%s)
    """
    cur.execute(sql, [main_id])
    res = cur.fetchall()
    conn.close()

    if len(res) == 0: return None

    for i, main in enumerate(res):
        sub = find_sub_comment_by_main_comment(main['id'])
        res[i]['sub'] = sub
    return res

def add_new_comment(content, date, uid, tid):
    conn, cur = get_connection()

    comment_id_hash = str(hash(content))[:6]
    comment_id = abs(int(comment_id_hash)) + randint(1, 10000)

    date = str(datetime.now())

    sql = """
            INSERT INTO COMMENT(content, date, user_id, thread_id)
            VALUES ((%s), (%s), (%s), (%s))
        """
    cur.execute(sql, [content, date, uid, tid])
    conn.commit()
    conn.close()
    return
