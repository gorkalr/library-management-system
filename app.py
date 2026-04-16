from flask import Flask, render_template, request, redirect, session
from db import get_db
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret"

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u = request.form["userid"]
        p = request.form["password"]

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s AND active=1",(u,p))
        user = cur.fetchone()

        if user:
            session["role"] = user["role"]
            return redirect("/admin_home" if user["role"]=="admin" else "/user_home")

    return render_template("login.html")

# HOME
@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

# TRANSACTIONS
@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

# AVAILABILITY
@app.route("/availability")
def availability():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM books")
    return render_template("availability.html", books=cur.fetchall())

# SEARCH
@app.route("/search", methods=["GET","POST"])
def search():
    books=[]
    if request.method=="POST":
        name=request.form["name"]
        db=get_db()
        cur=db.cursor(dictionary=True)
        cur.execute("SELECT * FROM books WHERE name LIKE %s",("%"+name+"%",))
        books=cur.fetchall()
    return render_template("search.html",books=books)

# ISSUE
@app.route("/issue", methods=["GET","POST"])
def issue():
    db=get_db()
    cur=db.cursor(dictionary=True)
    cur.execute("SELECT * FROM books WHERE available=1")
    books=cur.fetchall()

    if request.method=="POST":
        book_id=request.form["book"]
        today=datetime.today()
        ret=today+timedelta(days=15)

        cur.execute("UPDATE books SET available=0 WHERE id=%s",(book_id,))
        cur.execute("INSERT INTO issues(book_id,issue_date,return_date) VALUES(%s,%s,%s)",
                    (book_id,today,ret))
        db.commit()

        return render_template("confirmation.html")

    return render_template("issue.html",books=books)

# RETURN
@app.route("/return", methods=["GET","POST"])
def return_book():
    db = get_db()
    cur = db.cursor(dictionary=True)

    # Get all issued books (not yet returned)
    cur.execute("""
        SELECT issues.id, books.name, issues.return_date, issues.book_id
        FROM issues
        JOIN books ON issues.book_id = books.id
        WHERE issues.actual_return IS NULL
    """)
    issues = cur.fetchall()

    if request.method == "POST":
        issue_id = request.form.get("issue")

        if not issue_id:
            return render_template("cancel.html")

        # Fetch selected issue record
        cur.execute("SELECT * FROM issues WHERE id=%s", (issue_id,))
        record = cur.fetchone()

        # Convert to date (VERY IMPORTANT FIX)
        actual = datetime.today().date()
        expected = record["return_date"]

        fine = 0
        if actual > expected:
            fine = (actual - expected).days * 5

        # Update issue table
        cur.execute("""
            UPDATE issues 
            SET actual_return=%s, fine=%s 
            WHERE id=%s
        """, (actual, fine, issue_id))

        # Make book available again
        cur.execute("""
            UPDATE books 
            SET available=1 
            WHERE id=%s
        """, (record["book_id"],))

        db.commit()

        return render_template("fine.html", fine=fine)

    return render_template("return.html", issues=issues)# REPORTS
@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/books_report")
def books_report():
    db=get_db()
    cur=db.cursor(dictionary=True)
    cur.execute("SELECT * FROM books")
    return render_template("books_report.html",books=cur.fetchall())

@app.route("/active_issues")
def active_issues():
    db=get_db()
    cur=db.cursor(dictionary=True)
    cur.execute("""SELECT books.name,issue_date,return_date 
                   FROM issues JOIN books ON issues.book_id=books.id 
                   WHERE actual_return IS NULL""")
    return render_template("active_issues.html",issues=cur.fetchall())

@app.route("/overdue")
def overdue():
    db=get_db()
    cur=db.cursor(dictionary=True)
    cur.execute("""SELECT books.name,return_date 
                   FROM issues JOIN books ON issues.book_id=books.id 
                   WHERE actual_return IS NULL AND return_date<CURDATE()""")
    return render_template("overdue.html",issues=cur.fetchall())

# MAINTENANCE
@app.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")

@app.route("/add_book", methods=["GET","POST"])
def add_book():
    if request.method=="POST":
        name=request.form["name"]
        author=request.form["author"]

        db=get_db()
        cur=db.cursor()
        cur.execute("INSERT INTO books(name,author,category,available) VALUES(%s,%s,'General',1)",(name,author))
        db.commit()

        return render_template("confirmation.html")

    return render_template("add_book.html")

# USER MGMT
@app.route("/user_management")
def user_management():
    return render_template("user_management.html")

# OTHER
@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

@app.route("/add_membership", methods=["GET","POST"])
def add_membership():
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        address = request.form["address"]
        aadhar = request.form["aadhar"]
        start = request.form["start"]
        end = request.form["end"]

        db = get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO memberships(name,contact,address,aadhar,start_date,end_date,status)
            VALUES(%s,%s,%s,%s,%s,%s,'Active')
        """, (name,contact,address,aadhar,start,end))

        db.commit()

        return render_template("confirmation.html")

    return render_template("add_membership.html")

@app.route("/update_membership", methods=["GET","POST"])
def update_membership():
    db = get_db()
    cur = db.cursor(dictionary=True)

    # Fetch memberships
    cur.execute("SELECT * FROM memberships")
    memberships = cur.fetchall()

    if request.method == "POST":
        mem_id = request.form["id"]
        action = request.form["action"]

        if action == "extend":
            cur.execute("""
                UPDATE memberships 
                SET end_date = DATE_ADD(end_date, INTERVAL 6 MONTH)
                WHERE id=%s
            """, (mem_id,))

        elif action == "cancel":
            cur.execute("""
                UPDATE memberships 
                SET status='Inactive'
                WHERE id=%s
            """, (mem_id,))

        db.commit()

        return render_template("confirmation.html")

    return render_template("update_membership.html", memberships=memberships)

@app.route("/membership_report")
def membership_report():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM memberships")
    data = cur.fetchall()

    return render_template("membership_report.html", memberships=data)

if __name__=="__main__":
    app.run(debug=True)