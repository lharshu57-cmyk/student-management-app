import sqlite3

DATABASE_NAME = "students.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            course TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks REAL NOT NULL,
            credits REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, email, course):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (name, email, course)
    )
    connection.commit()
    connection.close()


def get_students():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, course FROM students ORDER BY id")
    students = cursor.fetchall()
    connection.close()
    return students


def update_student(student_id, name, email, course):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?",
        (name, email, course, student_id)
    )
    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM marks WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()
    connection.close()


def add_marks(student_id, subject, marks, credits):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO marks (student_id, subject, marks, credits)
           VALUES (?, ?, ?, ?)""",
        (student_id, subject, marks, credits)
    )
    connection.commit()
    connection.close()


def get_marks(student_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT id, subject, marks, credits
           FROM marks WHERE student_id = ? ORDER BY id""",
        (student_id,)
    )
    marks = cursor.fetchall()
    connection.close()
    return marks


def delete_marks(mark_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM marks WHERE id = ?", (mark_id,))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
