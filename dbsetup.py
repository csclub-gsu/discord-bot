import sqlite3

def setup_db():
    connection = sqlite3.connect("reminders.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TIMESTAMP,
                message TEXT,
                link TEXT
        )
    """)

    connection.commit()
    connection.close()