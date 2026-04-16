from database import get_db
from werkzeug.security import generate_password_hash

def init_db():
    db = get_db()

    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        issue_date TEXT,
        return_date TEXT
    )
    ''')

    # Insert default admin (only once)
    db.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
               ("admin", generate_password_hash("admin123"), "Admin"))

    db.commit()