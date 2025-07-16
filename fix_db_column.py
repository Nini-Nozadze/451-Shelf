import sqlite3

db_path = 'instance/books.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE user ADD COLUMN image TEXT;")
    print(" 'image' სვეტი დაემატა User ცხრილში.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ'image' სვეტი უკვე არსებობს.")
    else:
        print(" შეცდომა:", e)

conn.commit()
conn.close()
