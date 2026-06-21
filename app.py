from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "sj_toppers_secret_key"

# Create users file if not exists
if not os.path.exists("users.txt"):
    open("users.txt", "w").close()


# ======================
# HOME PAGE
# ======================
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')


# ======================
# ABOUT PAGE
# ======================
@app.route('/about.html')
def about():
    return render_template('about.html')


# ======================
# CONTACT PAGE
# ======================
@app.route('/contact.html')
def contact():
    return render_template('contact.html')


# ======================
# FEATURES PAGE
# ======================
@app.route('/features.html')
def features():
    return render_template('features.html')


# ======================
# LOGIN PAGE
# ======================
@app.route('/login.html')
def login():
    return render_template('login.html')


# ======================
# SIGNUP PAGE
# ======================
@app.route('/signup.html')
def signup():
    return render_template('signup.html')


# ======================
# REGISTER USER
# ======================
@app.route('/register', methods=['POST'])
def register():

    username = request.form['username']
    password = request.form['password']

    with open("users.txt", "r") as file:
        users = file.readlines()

    for user in users:
        data = user.strip().split(",")

        if len(data) >= 2:
            if username == data[0]:
                return "Username Already Exists"

    with open("users.txt", "a") as file:
        file.write(username + "," + password + "\n")

    return redirect('/login.html')


# ======================
# CHECK LOGIN
# ======================
@app.route('/checklogin', methods=['POST'])
def checklogin():

    username = request.form['username']
    password = request.form['password']

    with open("users.txt", "r") as file:
        users = file.readlines()

    for user in users:
        data = user.strip().split(",")

        if len(data) >= 2:
            if username == data[0] and password == data[1]:
                session['username'] = username
                return redirect('/dashboard.html')

    return "Wrong Username or Password"


# ======================
# DASHBOARD PAGE
# ======================
@app.route('/dashboard.html')
def dashboard():

    if 'username' not in session:
        return redirect('/login.html')

    return render_template(
        'dashboard.html',
        username=session['username'],
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


# ======================
# ANALYZE TEST
# ======================
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'username' not in session:
        return redirect('/login.html')

    physics = int(request.form['physics'])
    chemistry = int(request.form['chemistry'])
    maths = int(request.form['maths'])

    correct = int(request.form['correct'])
    wrong = int(request.form['wrong'])

    total_score = physics + chemistry + maths
    attempted = correct + wrong

    accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0

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

    subjects = {
        "Physics": physics,
        "Chemistry": chemistry,
        "Maths": maths
    }

    strong_subject = max(subjects, key=subjects.get)
    weak_subject = min(subjects, key=subjects.get)

    return render_template(
        'dashboard.html',
        username=session['username'],
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


# ======================
# LOGOUT
# ======================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login.html')


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
