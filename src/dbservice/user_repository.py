import psycopg2
import dbservice.config as config

def get_connection():
    db_info = config.get_db_info()
    db_connection = psycopg2.connect(
        **db_info
    )
    return db_connection