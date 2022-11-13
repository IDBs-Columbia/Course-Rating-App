import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    return db_connection


def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()

    sql = "select * from course"

    cur.execute(sql)
    fields = [field_md[0] for field_md in cur.description]
    res = [dict(zip(fields, row)) for row in cur.fetchall()]

    conn.close()

    return res

def get_all_courses_with_stat():
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT *
    FROM (
         SELECT CALL_NUMBER,
                avg(COURSE_SATISFACTION) AS RATING,
                avg(WORKLOAD)            AS WORKLOAD,
                avg(DIFFICULTY)          AS DIFFICULTY
         FROM USER_REGULAR_RATES_COURSE
         GROUP BY CALL_NUMBER) AS T
         JOIN COURSE AS C ON C.CALL_NUMBER = T.CALL_NUMBER;
    """

    cur.execute(sql)
    fields = [field_md[0] for field_md in cur.description]
    res = [dict(zip(fields, row)) for row in cur.fetchall()]

    conn.close()

    return res