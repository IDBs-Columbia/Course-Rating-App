import os

def get_db_info():

    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)
    db_database = os.environ.get("DBDATABASE", None)

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "database": db_database
        }
    else:
        db_info = {
            "host": "w4111project1part2db.cisxo09blonu.us-east-1.rds.amazonaws.com",
            "user": "hz2771",
            "password": "6832",
            "database": "proj1part2"
        }

    return db_info