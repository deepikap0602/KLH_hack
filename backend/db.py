import mysql.connector
from mysql.connector import Error
import hashlib
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(conn, username, email, password):
    if conn:
        cursor = conn.cursor()
        hashed_pw = hash_password(password)
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (username, email, hashed_pw))
            conn.commit()
        except Error as e:
            print("Error creating user:", e)
        cursor.close()

def check_user(conn, username, password):
    if conn:
        cursor = conn.cursor(dictionary=True)
        hashed_pw = hash_password(password)
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, hashed_pw))
        user = cursor.fetchone()
        cursor.close()
        return user
    return None