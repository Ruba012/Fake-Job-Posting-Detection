import os
import sqlite3  # Import the library to work with the database

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "fjpd_system.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Function to create the database file and tables
def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create 'User' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name TEXT NOT NULL
    )
    ''')

    # Create 'JobPost' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS JobPost (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        description TEXT NOT NULL,
        submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    )
    ''')

    # Create 'Result' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Result (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL UNIQUE,
        prediction TEXT NOT NULL,
        confidence_score FLOAT,
        FOREIGN KEY (post_id) REFERENCES JobPost (post_id) ON DELETE CASCADE
    )
    ''')

    # Create 'ADMIN' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ADMIN (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Create 'FEEDBACK' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FEEDBACK (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        post_id INTEGER,
        contact TEXT,
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (post_id) REFERENCES JobPost (post_id) ON DELETE CASCADE
    )
    ''')

    conn.commit()

    # Add contact column if database already exists from old version
    try:
        cursor.execute("ALTER TABLE FEEDBACK ADD COLUMN contact TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists, so ignore
        pass

    conn.close()


# Function to add a new job post (Insert)
def add_job_post(title, description, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Using placeholders (?) to prevent SQL Injection
    cursor.execute('''
        INSERT INTO JobPost (title, description, user_id)
        VALUES (?, ?, ?)
    ''', (title, description, user_id))

    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id


# Function to get all stored jobs (Select)
def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM JobPost')
    jobs = cursor.fetchall()
    conn.close()
    return jobs


# Function to delete a specific job using its ID
def delete_job(post_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM JobPost WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()
    print(f"Job number {post_id} deleted successfully")


# Function to save AI analysis results
def add_analysis_result(post_id, prediction, confidence_score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Result (post_id, prediction, confidence_score)
        VALUES (?, ?, ?)
    ''', (post_id, prediction, confidence_score))
    conn.commit()
    conn.close()
    print(f"Analysis result for job {post_id} saved successfully")


# Function to get all jobs with AI results for Dashboard
def get_all_jobs_with_results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT JobPost.post_id, JobPost.title, Result.prediction, Result.confidence_score
        FROM JobPost
        LEFT JOIN Result ON JobPost.post_id = Result.post_id
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


# Function to add an Admin (Based on ADMIN table)
def add_admin(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO ADMIN (username, password, role) VALUES (?, ?, ?)',
        (username, password, role)
    )
    conn.commit()
    conn.close()
    print(f"Admin {username} added successfully")


# Function to add Feedback (Based on FEEDBACK table)
def add_feedback(user_id, post_id, contact, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO FEEDBACK (user_id, post_id, contact, message)
        VALUES (?, ?, ?, ?)
    ''', (user_id, post_id, contact, message))
    conn.commit()
    conn.close()
    print("Feedback added successfully")


# Main Entry Point: Runs only when executing this file directly
if __name__ == "__main__":
    init_database()
    print("Database is ready and tables are created successfully")


def ensure_default_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM User WHERE user_id = 1")
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO User (user_id, display_name) VALUES (?, ?)",
            (1, "Default User")
        )
        conn.commit()

    conn.close()


def get_all_feedback():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT feedback_id, user_id, post_id, contact, message, created_at
        FROM FEEDBACK
        ORDER BY created_at DESC
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


def get_feedback_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM FEEDBACK')
    count = cursor.fetchone()[0]

    conn.close()
    return count