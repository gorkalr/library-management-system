from flask import Flask, render_template, request, redirect, session
from database import get_db
from models import init_db
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "super_secret"

init_db()

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?",
                          (request.form['username'],)).fetchone()

        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['id']
            session['role'] = user['role']
            return redirect('/dashboard')

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', role=session.get('role'))


# ---------------- ADD BOOK ----------------
@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if session.get('role') != 'Admin':
        return "Access Denied"

    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']

        if not name or not author:
            return render_template('add_book.html', error="All fields required")

        db = get_db()
        db.execute("INSERT INTO books (name,author) VALUES (?,?)", (name, author))
        db.commit()

        return render_template('add_book.html', success="Book added successfully")

    return render_template('add_book.html')


# ---------------- ISSUE BOOK ----------------
@app.route('/issue', methods=['GET','POST'])
def issue():
    db = get_db()

    if request.method == 'POST':
        book_id = request.form['book_id']

        issue_date = datetime.today()
        return_date = issue_date + timedelta(days=15)

        db.execute("INSERT INTO issues (user_id,book_id,issue_date,return_date) VALUES (?,?,?,?)",
                   (session['user'], book_id, issue_date, return_date))
        db.commit()

        return render_template('issue.html', success="Book issued successfully")

    books = db.execute("SELECT * FROM books").fetchall()
    return render_template('issue.html', books=books)


# ---------------- RETURN BOOK ----------------
@app.route('/return', methods=['GET','POST'])
def return_book():
    db = get_db()

    if request.method == 'POST':
        issue_id = request.form['issue_id']

        issue = db.execute("SELECT * FROM issues WHERE id=?", (issue_id,)).fetchone()

        return_date = datetime.strptime(issue['return_date'], "%Y-%m-%d %H:%M:%S.%f")
        today = datetime.today()

        days_late = (today - return_date).days
        fine = max(0, days_late * 5)

        return render_template('fine.html', fine=fine, issue_id=issue_id)

    issues = db.execute("SELECT issues.id, books.name FROM issues JOIN books ON issues.book_id = books.id").fetchall()
    return render_template('return.html', issues=issues)


# ---------------- PAY FINE ----------------
@app.route('/pay_fine', methods=['POST'])
def pay_fine():
    paid = request.form.get('paid')

    if not paid:
        return render_template('fine.html', error="Please pay fine")

    db = get_db()
    db.execute("DELETE FROM issues WHERE id=?", (request.form['issue_id'],))
    db.commit()

    return "✅ Book Returned Successfully"


# ---------------- REPORT ----------------
@app.route('/report')
def report():
    db = get_db()

    total_books = db.execute("SELECT COUNT(*) as total FROM books").fetchone()['total']
    issued_books = db.execute("SELECT COUNT(*) as total FROM issues").fetchone()['total']

    return render_template('report.html', total_books=total_books, issued_books=issued_books)


if __name__ == "__main__":
    app.run(debug=True)