from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'replace-this-with-a-secure-random-key'

# Demo credentials - replace with secure auth in production
VALID = {'username': 'admin', 'password': 'admin123'}


@app.route('/')
def home():
    # serve the existing index.html from project root
    return app.send_static_file('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == VALID['username'] and password == VALID['password']:
            session['user'] = username
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        flash('Incorrect credentials', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please sign in to view the dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session.get('user'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
