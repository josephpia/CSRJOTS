from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey123"

# Default accounts
users = {
    "admin": {"password": "1234", "role": "admin"}
}

login_count = 0

@app.route('/')
def home():
    return redirect(url_for('login'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    global login_count
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            message = "User does not have an account"
        elif users[username]["password"] == password:
            session['username'] = username
            session['role'] = users[username]["role"]

            login_count += 1

            if users[username]["role"] == "admin":
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            message = "Wrong password"

    return render_template('login.html', message=message)

# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            message = "Username already exists"
        else:
            users[username] = {"password": password, "role": "user"}
            return redirect(url_for('login'))

    return render_template('signup.html', message=message)

# USER DASHBOARD
@app.route('/userdashboard')
def user_dashboard():
    return render_template('userdashboard.html')

# ADMIN MAIN DASHBOARD
@app.route('/admindashboard')
def admin_dashboard():
    total_users = len(users)
    return render_template('admindashboard.html', total_users=total_users)

# APP MONITOR
@app.route('/appmonitor')
def app_monitor():
    total_users = len(users)
    active_users = total_users - 1
    return render_template('appmonitor.html', total_users=total_users, active_users=active_users)

# HISTORY
@app.route('/history')
def history():
    return render_template('history.html', login_count=login_count)

# SETTINGS
@app.route('/settings')
def settings():
    return render_template('settings.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)