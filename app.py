from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy user for authentication (replace with database logic)
USER_CREDENTIALS = {
    "admin@example.com": "password123"
}


# Initialize Database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                literacy_score INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                message TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/literacy-scale', methods=['GET', 'POST'])
def literacy_scale():
    if request.method == 'POST':
        name = request.form['name']
        score = int(request.form['score'])
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, literacy_score) VALUES (?, ?)", (name, score))
            conn.commit()
        return redirect(url_for('home'))
    return render_template("literacy_scale.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (user, message) VALUES (?, ?)", (user, message))
            conn.commit()
        return redirect(url_for('home'))
    return render_template("feedback.html")

@app.route('/news')
def news():
    news_articles = [
        {"title": "Stock Market Update", "source": "Financial Times"},
        {"title": "Bitcoin Reaches New High", "source": "CoinDesk"}
    ]
    return render_template("news.html", news=news_articles)

@app.route("/signIn", methods=["GET", "POST"])
def signIn():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Dummy authentication check (replace with actual authentication logic)
        if email == "admin" and password == "password":
            return redirect(url_for('index.html'))  # Redirect to a dashboard or home page
        
        return render_template("signIn.html", error="Invalid credentials. Please try again.")

    return render_template("signIn.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
            return redirect(url_for('dashboard'))  # Redirect after successful login
        
        return render_template('login.html', error="Invalid email or password. Try again.")

    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    return "Welcome to the Dashboard!"


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
