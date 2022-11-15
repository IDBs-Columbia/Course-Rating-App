import psycopg2
import psycopg2.extras
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor


def get_all_courses():
    conn, cur = get_connection()

    sql = "select * from course"

    cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_all_courses_with_stat():
    conn, cur = get_connection()

    sql = """
    SELECT C.CALL_NUMBER, NAME, COURSE_NUMBER, RATING, WORKLOAD, DIFFICULTY, INSTITUTION_NAME
    FROM COURSE AS C
    LEFT JOIN  (SELECT CALL_NUMBER,
                avg(COURSE_SATISFACTION) AS RATING,
                avg(WORKLOAD)            AS WORKLOAD,
                avg(DIFFICULTY)          AS DIFFICULTY
                FROM USER_REGULAR_RATES_COURSE
                GROUP BY CALL_NUMBER) AS T
    ON C.CALL_NUMBER = T.CALL_NUMBER
    JOIN INSTITUTION I ON C.INSTITUTION_ID = I.ID;
    """

    cur.execute(sql)
    # fields = [field_md[0] for field_md in cur.description]
    # res = [dict(zip(fields, row)) for row in cur.fetchall()]

    res = cur.fetchall()
    conn.close()

    return res


def get_course_with_stat(call_number):
    conn, cur = get_connection()

    sql = """
        SELECT *
        FROM (
             SELECT avg(COURSE_SATISFACTION) AS RATING,
                    avg(WORKLOAD)            AS WORKLOAD,
                    avg(DIFFICULTY)          AS DIFFICULTY
             FROM USER_REGULAR_RATES_COURSE
             WHERE call_number = (%s)
             ) AS T, COURSE AS C
        WHERE C.CALL_NUMBER = (%s);
        """

    cur.execute(sql, [call_number, call_number])
    res = cur.fetchone()

    conn.close()

    return res


def add_user_rating(call_number, rating, workload, difficulty, uid):
    conn, cur = get_connection()
    sql = """
        INSERT INTO USER_REGULAR_RATES_COURSE
        VALUES ((%s), (%s), (%s), (%s), (%s))
        """

    cur.execute(sql, [int(rating), int(difficulty), int(workload), uid, call_number])
    conn.commit()
    conn.close()
    return
