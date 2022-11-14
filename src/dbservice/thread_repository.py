import psycopg2
import psycopg2.extras
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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
