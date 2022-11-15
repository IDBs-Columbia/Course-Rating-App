import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor

def get_reports():
    connection, cursor = get_connection()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    connection.close()
    return reports