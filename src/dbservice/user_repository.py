import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor


def check_password(username, password):
    conn, cur = get_connection()

    sql = """
            SELECT *
            FROM USER_ALL
            WHERE name = (%s)
        """

    cur.execute(sql, [username])
    res = cur.fetchone()
    if res is None: return False
    return res['password'] == password
