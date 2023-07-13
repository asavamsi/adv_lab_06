from flask import Flask, render_template, request, session
from waitress import serve
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    username = request.form['username']
    password = request.form['password']

    # Password format checking
    is_valid = (
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        password[-1].isdigit() and
        len(password) >= 8
    )
    is_valid1 = 1
    is_valid2 = 1
    is_valid3 = 1
    is_valid4 = 1
    if any(c.islower() for c in password) :
        is_valid1 = 0
    if any(c.isupper() for c in password) :
        is_valid2 = 0
    if password[-1].isdigit() :
        is_valid3 = 0
    if  len(password) >= 8:
        is_valid4 = 0
    if is_valid:
        # Store username and password in the database
        c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
        conn.commit()
    else:
        # Check failed attempts and display warning if necessary
        session['failed_attempts'] = session.get('failed_attempts', 0) + 1
        if session['failed_attempts'] >= 3:
            warning = "Three consecutive failed attempts. Please try again later."
            return render_template('index.html', warning=warning)
            
    return render_template('report.html', is_valid=is_valid,is_valid1=is_valid1,is_valid2=is_valid2,is_valid3=is_valid3,is_valid4=is_valid4)
    
    

if __name__ == '__main__':
    serve(app, host="127.0.0.1", port=5000)
    app.run(debug=True)

    