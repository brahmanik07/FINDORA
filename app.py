from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "findora_secret"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home
@app.route('/')
def home():
    return render_template("index.html")

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        db.execute("INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)",
                   (name, phone, email, password))
        db.commit()

        return redirect('/login')
    return render_template("register.html")

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?",
                          (email, password)).fetchone()

        if user:
            session['user'] = user['id']
            return redirect('/dashboard')
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# Report Lost
@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        item = request.form['item']
        description = request.form['description']

        db = get_db()
        db.execute("INSERT INTO items (name, description, type) VALUES (?, ?, ?)",
                   (item, description, "lost"))
        db.commit()

        return redirect('/dashboard')

    return render_template("report_lost.html")

# Report Found
@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        item = request.form['item']
        description = request.form['description']

        db = get_db()
        db.execute("INSERT INTO items (name, description, type) VALUES (?, ?, ?)",
                   (item, description, "found"))
        db.commit()

        return redirect('/dashboard')

    return render_template("report_found.html")

# Search
@app.route('/search', methods=['GET', 'POST'])
def search():
    db = get_db()
    items = db.execute("SELECT * FROM items").fetchall()
    return render_template("search.html", items=items)

# Run
if __name__ == '__main__':
    app.run(debug=True)