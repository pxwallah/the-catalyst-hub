import flask # type: ignore
import os

app = flask.Flask(__name__)
app.secret_key = "sj_toppers_secret_key"

# =========================================
# CREATE USERS FILE IF NOT EXISTS
# =========================================
if not os.path.exists("users.txt"):
    open("users.txt", "w").close()


# =========================================
# HOME PAGE
# URL -> /
# =========================================
@app.route('/')
@app.route('/index.html')
def home():
    return flask.render_template('index.html')


# =========================================


# =========================================
# ABOUT US PAGE
# URL -> /aboutus.html
# =========================================
@app.route('/aboutus.html')
def aboutus():
    return flask.render_template('about us.html')


# =========================================
# LOGIN PAGE
# URL -> /login.html
# =========================================
@app.route('/login.html')
def login():
    return flask.render_template('login.html')
#--------------------------------
#Features Page
@app.route('/features.html')
def features():
    return flask.render_template('features.html')


# =========================================
# SIGNUP PAGE
# URL -> /signup.html
# =========================================
@app.route('/signup.html')
def signup():
    return flask.render_template('signup.html')


# =========================================
# REGISTER USER
# =========================================
@app.route('/register', methods=['POST'])
def register():

    username = flask.request.form['username']
    password = flask.request.form['password']

    # CHECK IF USER ALREADY EXISTS
    with open("users.txt", "r") as file:
        users = file.readlines()

    for user in users:

        data = user.strip().split(",")

        if len(data) >= 2:

            if username == data[0]:
                return "Username Already Exists"

    # SAVE NEW USER
    with open("users.txt", "a") as file:
        file.write(username + "," + password + "\n")

    return flask.redirect('/login.html')


# =========================================
# CHECK LOGIN
# =========================================
@app.route('/checklogin', methods=['POST'])
def checklogin():

    username = flask.request.form['username']
    password = flask.request.form['password']

    with open("users.txt", "r") as file:
        users = file.readlines()

    for user in users:

        data = user.strip().split(",")

        if len(data) >= 2:

            if username == data[0] and password == data[1]:

                flask.session['username'] = username

                return flask.redirect('/dashboard.html')

    return "Wrong Username or Password"


# =========================================
# DASHBOARD PAGE
# =========================================
@app.route('/dashboard.html')
def dashboard():

    if 'username' not in flask.session:
        return flask.redirect('/login.html')

    return flask.render_template(

        'dashboard.html',

        username=flask.session['username'],

        score=0,
        accuracy=0,
        percentile="0",

        physics=0,
        chemistry=0,
        maths=0,

        correct=0,
        wrong=0,

        attempted=0,

        strong_subject="None",
        weak_subject="None"
    )


# =========================================
# ANALYZE TEST
# =========================================
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'username' not in flask.session:
        return flask.redirect('/login.html')

    physics = int(flask.request.form['physics'])
    chemistry = int(flask.request.form['chemistry'])
    maths = int(flask.request.form['maths'])

    correct = int(flask.request.form['correct'])
    wrong = int(flask.request.form['wrong'])

    # TOTAL SCORE
    total_score = physics + chemistry + maths

    # ATTEMPTED QUESTIONS
    attempted = correct + wrong

    # ACCURACY
    if attempted > 0:
        accuracy = round((correct / attempted) * 100, 2)
    else:
        accuracy = 0

    # PERCENTILE PREDICTION
    if total_score >= 250:
        percentile = "99+"

    elif total_score >= 200:
        percentile = "98+"

    elif total_score >= 150:
        percentile = "95+"

    elif total_score >= 120:
        percentile = "90+"

    else:
        percentile = "Below 90"

    # SUBJECT ANALYSIS
    subjects = {
        "Physics": physics,
        "Chemistry": chemistry,
        "Maths": maths
    }

    strong_subject = max(subjects, key=subjects.get)
    weak_subject = min(subjects, key=subjects.get)

    # RETURN DATA
    return flask.render_template(

        'dashboard.html',

        username=flask.session['username'],

        score=total_score,
        accuracy=accuracy,
        percentile=percentile,

        physics=physics,
        chemistry=chemistry,
        maths=maths,

        correct=correct,
        wrong=wrong,

        attempted=attempted,

        strong_subject=strong_subject,
        weak_subject=weak_subject
    )


# =========================================
# LOGOUT
# =========================================
@app.route('/logout')
def logout():

    flask.session.pop('username', None)

    return flask.redirect('/login.html')


# =========================================
# RUN APP
# =========================================
if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
    # ==========================================
# ABOUT US PAGE
# ==========================================
@app.route('/about.html')
def about():
    return flask.render_template('about.html')
# Logout Route
from flask import Flask, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/logout")
def logout():
    session.clear()      # Clear session data
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return "Login Page"

@app.route('/contact.html')
def contact():
    return flask.render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)