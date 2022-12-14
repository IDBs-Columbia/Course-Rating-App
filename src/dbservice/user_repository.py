import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor

def get_user_name_by_id(user_id):
    conn, cur = get_connection()

    sql = """
            SELECT name
            FROM USER_ALL
            WHERE email = (
                SELECT email
                FROM USER_REGULAR
                WHERE id = (%s)
                LIMIT 1
            )
            LIMIT 1
    """
    cur.execute(sql, [user_id])
    res = cur.fetchone()
    
    return res

def get_user_info_by_email(email):
    conn, cur = get_connection()

    sql = """
                SELECT T.*, name
                FROM
                    (SELECT email, status, id
                    FROM USER_REGULAR
                    UNION ALL
                    SELECT email, 'admin' as status, id
                    FROM USER_ADMIN) AS T
                    JOIN USER_ALL AS UA ON UA.EMAIL = T.EMAIL
                WHERE T.email = (%s)
            """

    cur.execute(sql, [email])
    res = cur.fetchone()
    return res

def validate_login(email, password):
    conn, cur = get_connection()

    sql = """
            SELECT *
            FROM USER_ALL
            WHERE email = (%s)
        """

    cur.execute(sql, [email])
    res = cur.fetchone()
    if res is None: return False
    return res['password'] == password

def check_email_duplicate(email):
    conn, cur = get_connection()

    sql = """
            SELECT *
            FROM USER_ALL
            WHERE email = (%s)
        """
    cur.execute(sql, [email])
    res = cur.fetchone()
    return res is not None

def create_new_user(email, pw):
    conn, cur = get_connection()
    sql1 = """
        INSERT INTO USER_ALL(email, name, password)
        VALUES (%s, 'anonymous', %s)
    """
    sql2 = """
        INSERT INTO USER_REGULAR(status, email)
        VALUES ('unrestricted', %s)
    """
    try:
        cur.execute(sql1, [email, pw])
        cur.execute(sql2, [email])
    except:
        conn.rollback()
        conn.close()
        return False
    else:
        conn.commit()
        conn.close()
        return True

def get_all_regular_users():
    conn, cur = get_connection()

    sql = """
            SELECT 
                user_regular.id, name, user_all.email, strikes, status
            FROM 
                user_all
            JOIN 
                user_regular
            ON 
                user_all.email = user_regular.email
        """

    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_all_staff_users():
    conn, cur = get_connection()

    sql = """
            SELECT 
                name, user_admin.*
            FROM 
                user_all
            JOIN 
                user_admin
            ON 
                user_all.email = user_admin.email
        """

    cur.execute(sql)
    res = cur.fetchall()
    return res
    
def get_admin_permision(email):
    conn, cur = get_connection()
    sql = """
            SELECT can_manage_report, can_manage_course, can_manage_comment, can_manage_user
            FROM USER_ADMIN
            WHERE email = (%s)
        """
    cur.execute(sql, [email])
    res = cur.fetchone()

    return res