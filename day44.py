from flask import Flask, request, redirect, url_for, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
db = SQLAlchemy(app)

# Database models
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    votes = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        voter = Voter(username=username, password=hashed_password)
        db.session.add(voter)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template_string(register_template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        voter = Voter.query.filter_by(username=username).first()

        if voter and check_password_hash(voter.password, password):
            if voter.has_voted:
                flash('You have already voted!', 'danger')
                return redirect(url_for('home'))
            return redirect(url_for('vote', voter_id=voter.id))
        else:
            flash('Login Unsuccessful. Check username and password.', 'danger')
    return render_template_string(login_template)

@app.route('/vote/<int:voter_id>', methods=['GET', 'POST'])
def vote(voter_id):
    voter = Voter.query.get(voter_id)
    candidates = Candidate.query.all()

    if request.method == 'POST':
        selected_candidate = request.form.get('candidate')
        candidate = Candidate.query.filter_by(name=selected_candidate).first()

        if candidate:
            candidate.votes += 1
            voter.has_voted = True
            db.session.commit()

            flash(f'Your vote for {selected_candidate} has been recorded!', 'success')
            return redirect(url_for('home'))
    return render_template_string(vote_template, candidates=candidates)

@app.route('/results')
def results():
    candidates = Candidate.query.all()
    return render_template_string(results_template, candidates=candidates)

if __name__ == '__main__':
    db.create_all()  # Creates database tables
    app.run(debug=True)

# HTML Templates embedded in Python code
home_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Voting App - Home</title>
</head>
<body>
    <h1>Welcome to the Voting App</h1>
    <a href="/register">Register</a> | <a href="/login">Login</a> | <a href="/results">View Results</a>
</body>
</html>
"""

register_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br>
        <label>Password:</label>
        <input type="password" name="password" required><br>
        <button type="submit">Register</button>
    </form>
    <a href="/login">Already have an account? Login</a>
</body>
</html>
"""

login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br>
        <label>Password:</label>
        <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

vote_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Vote</title>
</head>
<body>
    <h1>Cast Your Vote</h1>
    <form method="POST">
        {% for candidate in candidates %}
            <input type="radio" name="candidate" value="{{ candidate.name }}" required>
            {{ candidate.name }}<br>
        {% endfor %}
        <button type="submit">Submit Vote</button>
    </form>
</body>
</html>
"""

results_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Results</title>
</head>
<body>
    <h1>Results</h1>
    <ul>
        {% for candidate in candidates %}
            <li>{{ candidate.name }}: {{ candidate.votes }} votes</li>
        {% endfor %}
    </ul>
    <a href="/">Back to Home</a>
</body>
</html>
"""
