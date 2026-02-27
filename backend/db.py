import mysql.connector
from mysql.connector import Error

def get_connection(db_host, db_user, db_password, db_name):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None


def insert_lesson(conn, subject, topic, grade, duration, lesson_text):
    if conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO lesson_plans (subject, topic, grade, duration, lesson_text)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (subject, topic, grade, duration, lesson_text))
        conn.commit()
        cursor.close()


def fetch_lessons(conn):
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lesson_plans ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    return []