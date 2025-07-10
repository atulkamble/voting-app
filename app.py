from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

votes = {"Python": 0, "Java": 0, "Go": 0}

@app.route('/')
def index():
    return render_template('index.html', votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    language = request.form.get('language')
    if language in votes:
        votes[language] += 1
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_votes():
    for key in votes:
        votes[key] = 0
    return redirect(url_for('index'))

@app.route('/data')
def data():
    return jsonify(votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
