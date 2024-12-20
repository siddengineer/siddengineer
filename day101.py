from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import qrcode
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create Machines Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT UNIQUE NOT NULL,
            owner_name TEXT NOT NULL,
            calibration_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Create Reports Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Insert Sample Machines
    machines = [
        ("MACHINE123", "Govt Ration Shop 1", "2024-01-15", "Calibrated"),
        ("MACHINE456", "Farmer Market Stall 2", "2023-12-10", "Pending Calibration"),
        ("MACHINE789", "Govt Ration Shop 3", "2024-02-05", "Calibrated")
    ]
    for machine in machines:
        try:
            c.execute('''
                INSERT INTO machines (machine_id, owner_name, calibration_date, status)
                VALUES (?, ?, ?, ?)
            ''', machine)
        except sqlite3.IntegrityError:
            pass  # Prevent duplicates
    
    conn.commit()
    conn.close()

# Generate QR Code for Machines
def generate_qr_codes():
    machines = ["MACHINE123", "MACHINE456", "MACHINE789"]
    for machine in machines:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(machine)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f'{machine}.png')

# Fetch Location using IP Address
def get_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        location = data['loc'].split(',')
        lat, lon = location[0], location[1]
        
        geolocator = Nominatim(user_agent="geoapiExercises")
        address = geolocator.reverse((lat, lon))
        return address.address
    except:
        return "Unable to detect location"

# HTML Templates
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Jaago Grahak Jaago</title>
</head>
<body>
    <h1>Welcome to Jaago Grahak Jaago</h1>
    <p>Enter the Machine ID from the QR Code:</p>
    <form action="/machine" method="POST">
        <input type="text" name="machine_id" placeholder="Enter Machine ID" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

machine_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Machine Details</title>
</head>
<body>
    <h1>Machine Details</h1>
    <p><strong>Machine ID:</strong> {{ machine[1] }}</p>
    <p><strong>Owner:</strong> {{ machine[2] }}</p>
    <p><strong>Calibration Date:</strong> {{ machine[3] }}</p>
    <p><strong>Status:</strong> {{ machine[4] }}</p>
    <p><strong>Detected Location:</strong> {{ location }}</p>
    <a href="{{ url_for('report', machine_id=machine[1]) }}">Report Fraud</a>
</body>
</html>
"""

report_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Report Fraud</title>
</head>
<body>
    <h1>Report Fraud</h1>
    <p><strong>Machine ID:</strong> {{ machine_id }}</p>
    <form method="POST">
        <textarea name="description" placeholder="Describe the issue" required></textarea>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/machine', methods=['POST'])
def machine():
    machine_id = request.form['machine_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM machines WHERE machine_id = ?', (machine_id,))
    machine = c.fetchone()
    conn.close()
    
    if machine:
        location = get_location()
        return render_template_string(machine_html, machine=machine, location=location)
    else:
        return "Machine not found", 404

@app.route('/report/<machine_id>', methods=['GET', 'POST'])
def report(machine_id):
    if request.method == 'POST':
        description = request.form['description']
        location = get_location()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO reports (machine_id, location, description) VALUES (?, ?, ?)', 
                  (machine_id, location, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template_string(report_html, machine_id=machine_id)

if __name__ == '__main__':
    init_db()  # Initialize database
    generate_qr_codes()  # Generate QR codes
    app.run(debug=True)
