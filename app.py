from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace in production

votes = {"Python": 0, "Java": 0, "Go": 0}
admin_credentials = {'username': 'admin', 'password': 'admin123'}

@app.route('/')
def index():
    return render_template('index.html', votes=votes, logged_in=session.get('logged_in'))

@app.route('/vote', methods=['POST'])
def vote():
    language = request.form.get('language')
    if language in votes:
        votes[language] += 1
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_votes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    for key in votes:
        votes[key] = 0
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form.get('username') == admin_credentials['username'] and
                request.form.get('password') == admin_credentials['password']):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/data')
def data():
    return jsonify(votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
