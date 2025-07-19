import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='0599817844',
        db='store',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    