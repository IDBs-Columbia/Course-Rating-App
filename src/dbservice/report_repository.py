import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor


def user_has_reported_thread(uid, tid):
    conn, cur = get_connection()
    sql = """
                SELECT id
                FROM REPORT
                WHERE user_id = (%s) AND thread_id = (%s)
            """
    cur.execute(sql, [uid, tid])
    res = cur.fetchone()
    conn.close()
    return res is not None


def user_report_thread(uid, tid, cate, desc, date):
    conn, cur = get_connection()
    sql = """
            INSERT INTO report(category, description, date, user_id, thread_id)
            VALUES ((%s), (%s), (%s), (%s), (%s))
        """
    cur.execute(sql, [cate, desc, date, uid, tid])
    conn.commit()
    conn.close()
    return


def user_has_reported_comment(uid, cid):
    conn, cur = get_connection()
    sql = """
                SELECT id
                FROM REPORT
                WHERE user_id = (%s) AND comment_id = (%s)
            """
    cur.execute(sql, [uid, cid])
    res = cur.fetchone()
    conn.close()
    return res is not None


def user_report_comment(uid, cid, cate, desc, date):
    conn, cur = get_connection()
    sql = """
                INSERT INTO report(category, description, date, user_id, comment_id)
                VALUES ((%s), (%s), (%s), (%s), (%s))
            """
    cur.execute(sql, [cate, desc, date, uid, cid])
    conn.commit()
    conn.close()
    return

def get_all_report():
    conn, cur = get_connection()
    sql = """
                SELECT *
                FROM report
            """
    cur.execute(sql)
    res = cur.fetchall()
    return res
