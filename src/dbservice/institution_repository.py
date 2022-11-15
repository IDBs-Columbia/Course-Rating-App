import psycopg2
import dbservice.config as config


def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, cursor


def get_institutions():
    connection, cursor = get_connection()
    cursor.execute("SELECT * FROM institution")
    institutions = cursor.fetchall()
    connection.close()
    return institutions

def add_institution(institution_name):
    connection, cursor = get_connection()
    id_hash = str(hash(institution_name))[:6]
    id = abs(int(id_hash))

    cursor.execute("INSERT INTO institution(id, institution_name) VALUES (%s, %s)", (id, institution_name,))
    connection.commit()
    connection.close()