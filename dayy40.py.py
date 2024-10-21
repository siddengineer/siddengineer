from flask import Flask, render_template_string, request, redirect, flash, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audits.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database model for Fire Audit
class FireAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    equipment_status = db.Column(db.String(200), nullable=False)
    compliance_score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    issued_by = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Home route
@app.route('/')
def index():
    return render_template_string(index_html)

# Route to add a new audit
@app.route('/add_audit', methods=['GET', 'POST'])
def add_audit():
    if request.method == 'POST':
        new_audit = FireAudit(
            location=request.form['location'],
            equipment_status=request.form['equipment_status'],
            compliance_score=int(request.form['compliance_score']),
            description=request.form['description'],
            contact_number=request.form['contact_number'],
            issued_by=request.form['issued_by']
        )
        db.session.add(new_audit)
        db.session.commit()
        flash('Audit added successfully!', 'success')
        return redirect('/audits')
    return render_template_string(add_audit_html)

# Route to view all audits
@app.route('/audits')
def view_audits():
    audits = FireAudit.query.order_by(FireAudit.date.desc()).all()
    return render_template_string(audit_list_html, audits=audits)

# Route to export audits as CSV
@app.route('/export_csv')
def export_csv():
    audits = FireAudit.query.all()
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Location', 'Status', 'Score', 'Description', 'Contact', 'Issued By', 'Date'])

    for audit in audits:
        writer.writerow([
            audit.id, audit.location, audit.equipment_status, audit.compliance_score,
            audit.description, audit.contact_number, audit.issued_by, audit.date.strftime('%Y-%m-%d')
        ])

    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=audits.csv"
    return output

# HTML and CSS templates embedded as strings
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fire Audit Management System</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
        h1 { text-align: center; margin-top: 50px; }
        .container { width: 80%; margin: auto; padding: 20px; }
        a { text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <h1>Fire Audit Management System</h1>
    <div class="container">
        <a href="/add_audit">Add New Audit</a> | 
        <a href="/audits">View Audits</a> | 
        <a href="/export_csv">Export as CSV</a>
    </div>
</body>
</html>
"""

add_audit_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Fire Audit</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #e9ecef; }
        .form-container { width: 50%; margin: auto; margin-top: 50px; padding: 20px; background: white; border-radius: 8px; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
        input[type="submit"] { background-color: #007bff; color: white; border: none; cursor: pointer; }
        a { display: block; text-align: center; margin-top: 10px; color: #007bff; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Add New Audit</h1>
        <form method="POST">
            <input type="text" name="location" placeholder="Audit Location" required>
            <input type="text" name="equipment_status" placeholder="Equipment Status" required>
            <input type="number" name="compliance_score" placeholder="Compliance Score (0-100)" required>
            <textarea name="description" rows="4" placeholder="Description" required></textarea>
            <input type="text" name="contact_number" placeholder="Contact Number" required>
            <input type="text" name="issued_by" placeholder="Issued By" required>
            <input type="submit" value="Add Audit">
        </form>
        <a href="/">Back to Home</a>
    </div>
</body>
</html>
"""

audit_list_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audit List</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f8f9fa; }
        .container { width: 80%; margin: auto; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #007bff; color: white; }
        a { display: block; text-align: center; margin-top: 10px; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Audit List</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Location</th>
                <th>Status</th>
                <th>Score</th>
                <th>Description</th>
                <th>Contact</th>
                <th>Issued By</th>
                <th>Date</th>
            </tr>
            {% for audit in audits %}
            <tr>
                <td>{{ audit.id }}</td>
                <td>{{ audit.location }}</td>
                <td>{{ audit.equipment_status }}</td>
                <td>{{ audit.compliance_score }}</td>
                <td>{{ audit.description }}</td>
                <td>{{ audit.contact_number }}</td>
                <td>{{ audit.issued_by }}</td>
                <td>{{ audit.date.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/">Back to Home</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

