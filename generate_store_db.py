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

connection = get_db_connection()
cursor = connection.cursor()

with open("store.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

commands = sql_script.split(';')
for command in commands:
    command = command.strip()
    if command:
        try:
            cursor.execute(command)
        except Exception as e:
            print(f"Error: {e}\n--> {command}\n")

connection.commit()
cursor.close()
connection.close()

print("✅ Store database and dummy data created successfully!")
