from flask import Flask, render_template_string, request, flash, send_file
import sqlite3
import os
import qrcode
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret_key"

# Database setup
DB_FILE = "medicine_db.sqlite"

# Create database if it doesn't exist
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        name TEXT PRIMARY KEY,
        manufacturer TEXT,
        batch TEXT,
        expiry TEXT
    )
    """)
    # Insert sample data
    sample_data = [
        ("Paracetamol-500", "ABC Pharma", "A123", "2025-12"),
        ("Ibuprofen-200", "XYZ Pharma", "B456", "2024-06"),
        ("Amoxicillin-250", "LMN Pharma", "C789", "2026-03")
    ]
    cursor.executemany("INSERT OR REPLACE INTO medicines VALUES (?, ?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

# HTML template embedded in Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medicine Verification System</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center text-primary">Medicine Verification System</h1>
        <div class="card mt-4">
            <div class="card-body">
                <form method="POST" action="/" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="medicine_name" class="form-label">Medicine Name</label>
                        <input
                            type="text"
                            class="form-control"
                            id="medicine_name"
                            name="medicine_name"
                            placeholder="e.g., Paracetamol-500"
                        />
                    </div>
                    <div class="mb-3">
                        <label for="batch_number" class="form-label">Batch Number</label>
                        <input
                            type="text"
                            class="form-control"
                            id="batch_number"
                            name="batch_number"
                            placeholder="e.g., A123"
                        />
                    </div>
                    <button type="submit" class="btn btn-primary">Verify</button>
                </form>
            </div>
        </div>
        <div class="card mt-4">
            <div class="card-body">
                <h5>QR Code Verification</h5>
                <form method="POST" action="/verify-qr" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="qr_file" class="form-label">Upload QR Code</label>
                        <input type="file" class="form-control" id="qr_file" name="qr_file" />
                    </div>
                    <button type="submit" class="btn btn-secondary">Verify QR</button>
                </form>
            </div>
        </div>
        <div class="card mt-4">
            <div class="card-body">
                <h5>Generate QR Code</h5>
                <form method="POST" action="/generate-qr">
                    <div class="mb-3">
                        <label for="medicine_name_qr" class="form-label">Medicine Name</label>
                        <input
                            type="text"
                            class="form-control"
                            id="medicine_name_qr"
                            name="medicine_name_qr"
                            placeholder="e.g., Paracetamol-500"
                        />
                    </div>
                    <button type="submit" class="btn btn-success">Generate QR Code</button>
                </form>
            </div>
        </div>

        <!-- Flash messages -->
        <div class="mt-4">
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                <div class="alert alert-{{ category }}" role="alert">
                    {{ message }}
                </div>
                {% endfor %}
            {% endif %}
            {% endwith %}
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        medicine_name = request.form.get("medicine_name")
        batch_number = request.form.get("batch_number")

        if not medicine_name or not batch_number:
            flash("Please enter both medicine name and batch number.", "danger")
            return render_template_string(HTML_TEMPLATE)

        # Database query
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        query = "SELECT * FROM medicines WHERE name = ?"
        result = cursor.execute(query, (medicine_name,)).fetchone()
        conn.close()

        if result:
            db_name, manufacturer, db_batch, expiry = result
            if db_batch == batch_number:
                flash(
                    f"Medicine Verified! Manufacturer: {manufacturer}, Expiry: {expiry}",
                    "success",
                )
            else:
                flash(
                    "Batch number does not match. This could be a counterfeit.", "warning"
                )
        else:
            flash("Medicine not found in the database. Please check again.", "danger")

    return render_template_string(HTML_TEMPLATE)

# Route to generate a QR code
@app.route("/generate-qr", methods=["POST"])
def generate_qr():
    medicine_name = request.form.get("medicine_name_qr")
    if not medicine_name:
        flash("Please enter a medicine name to generate QR code.", "danger")
        return render_template_string(HTML_TEMPLATE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM medicines WHERE name = ?"
    result = cursor.execute(query, (medicine_name,)).fetchone()
    conn.close()

    if result:
        db_name, manufacturer, db_batch, expiry = result
        qr_data = f"Medicine: {db_name}\nManufacturer: {manufacturer}\nBatch: {db_batch}\nExpiry: {expiry}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return send_file(buffer, mimetype="image/png", as_attachment=True, download_name=f"{medicine_name}_QR.png")
    else:
        flash("Medicine not found in the database.", "danger")
        return render_template_string(HTML_TEMPLATE)

# Route to verify a QR code
@app.route("/verify-qr", methods=["POST"])
def verify_qr():
    if "qr_file" not in request.files or not request.files["qr_file"].filename:
        flash("Please upload a QR code file to verify.", "danger")
        return render_template_string(HTML_TEMPLATE)

    qr_file = request.files["qr_file"]
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode

        img = Image.open(qr_file)
        decoded_data = decode(img)
        if not decoded_data:
            flash("Unable to decode the QR code. Please check the file.", "danger")
        else:
            flash(f"QR Code Verified: {decoded_data[0].data.decode('utf-8')}", "success")
    except Exception as e:
        flash(f"Error reading QR code: {e}", "danger")

    return render_template_string(HTML_TEMPLATE)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
