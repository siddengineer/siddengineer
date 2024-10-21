from flask import Flask, render_template_string, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = 'supersecretkey'

# Configuring SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fire_audit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for Fire Audit
class FireAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    equipment_status = db.Column(db.String(200), nullable=False)
    compliance_score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Audit {self.location} - {self.date}>"

# Home route
@app.route('/')
def index():
    index_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fire Audit Management System</title>
    </head>
    <body>
        <h1>Fire Audit Management System</h1>
        <a href="/add_audit">Add New Audit</a><br><br>
        <a href="/audits">View Audits</a>
    </body>
    </html>
    """
    return render_template_string(index_html)

# Route to add a new audit
@app.route('/add_audit', methods=['GET', 'POST'])
def add_audit():
    if request.method == 'POST':
        try:
            location = request.form['location']
            equipment_status = request.form['equipment_status']
            compliance_score = int(request.form['compliance_score'])  # Convert to integer

            # Create new audit object
            new_audit = FireAudit(
                location=location,
                equipment_status=equipment_status,
                compliance_score=compliance_score
            )

            # Add to the database
            db.session.add(new_audit)
            db.session.commit()
            flash('Audit added successfully!', 'success')
            return redirect('/')

        except ValueError:
            flash('Compliance score must be a number.', 'error')
        except Exception as e:
            flash(f"There was an issue: {e}", 'error')

    add_audit_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Fire Audit</title>
    </head>
    <body>
        <h1>Add Fire Audit</h1>
        <form method="POST">
            <label for="location">Audit Location:</label>
            <input type="text" name="location" required><br><br>

            <label for="equipment_status">Equipment Status:</label>
            <input type="text" name="equipment_status" required><br><br>

            <label for="compliance_score">Compliance Score (0-100):</label>
            <input type="number" name="compliance_score" required><br><br>

            <input type="submit" value="Add Audit">
        </form>
        <br>
        <a href="/">Back to Home</a>
        {% with messages = get_flashed_messages(with_categories=True) %}
            {% if messages %}
                <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    </body>
    </html>
    """
    return render_template_string(add_audit_html)

# Route to view the audit list
@app.route('/audits')
def audits():
    audits = FireAudit.query.order_by(FireAudit.date.desc()).all()
    audit_list_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Audit List</title>
    </head>
    <body>
        <h1>Audit List</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Location</th>
                <th>Equipment Status</th>
                <th>Compliance Score</th>
                <th>Date</th>
            </tr>
            {% for audit in audits %}
            <tr>
                <td>{{ audit.id }}</td>
                <td>{{ audit.location }}</td>
                <td>{{ audit.equipment_status }}</td>
                <td>{{ audit.compliance_score }}</td>
                <td>{{ audit.date.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </table>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(audit_list_html, audits=audits)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database
    app.run(debug=True)
