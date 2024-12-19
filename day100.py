from flask import Flask, render_template_string, request, redirect, flash, send_file
from fpdf import FPDF
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # For Flash messages


# Function to generate unique ticket IDs
def generate_ticket_id():
    return f"T{random.randint(100000, 999999)}"


# Function to save ticket as a PDF with Unicode support
def save_ticket_to_pdf(ticket_id, source, destination, date, passengers, fare):
    pdf = FPDF()
    pdf.add_page()

    # Use DejaVuSans font for Unicode support (check if font exists or download it)
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    if not os.path.exists("fonts"):
        os.makedirs("fonts")
    if not os.path.exists(font_path):
        import urllib.request
        urllib.request.urlretrieve("https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf", font_path)

    pdf.add_font("DejaVu", style="", fname=font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Ticket content
    pdf.cell(200, 10, txt="Local Bus Ticket", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Ticket ID: {ticket_id}", ln=True)
    pdf.cell(200, 10, txt=f"Source: {source}", ln=True)
    pdf.cell(200, 10, txt=f"Destination: {destination}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Passengers: {passengers}", ln=True)
    pdf.cell(200, 10, txt=f"Fare: ₹{fare}", ln=True)
    
    # Save the ticket
    pdf_file = f"ticket_{ticket_id}.pdf"
    pdf.output(pdf_file)
    return pdf_file


# HTML template embedded into the code
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Bus Booking System</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center text-primary mb-4">Local Bus Booking System</h1>

        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        <div class="container">
            {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        {% endwith %}

        <!-- Booking Form -->
        <form method="POST" action="/book" class="bg-white p-4 rounded shadow">
            <div class="mb-3">
                <label for="source" class="form-label">Source</label>
                <input type="text" id="source" name="source" class="form-control" placeholder="Enter source location" required>
            </div>
            <div class="mb-3">
                <label for="destination" class="form-label">Destination</label>
                <input type="text" id="destination" name="destination" class="form-control" placeholder="Enter destination" required>
            </div>
            <div class="mb-3">
                <label for="date" class="form-label">Date</label>
                <input type="date" id="date" name="date" class="form-control" value="{{ today }}" readonly>
            </div>
            <div class="mb-3">
                <label for="passengers" class="form-label">Number of Passengers</label>
                <input type="number" id="passengers" name="passengers" class="form-control" min="1" value="1" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Book Ticket</button>
        </form>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@app.route("/")
def index():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template_string(template, today=today)


@app.route("/book", methods=["POST"])
def book_ticket():
    source = request.form.get("source")
    destination = request.form.get("destination")
    date = request.form.get("date")
    passengers = int(request.form.get("passengers"))

    if source == destination:
        flash("Source and destination cannot be the same!", "danger")
        return redirect("/")

    if passengers <= 0:
        flash("Number of passengers must be at least 1!", "danger")
        return redirect("/")

    # Calculate fare and generate ticket
    ticket_id = generate_ticket_id()
    fare = 50 * passengers  # ₹50 per passenger
    pdf_file = save_ticket_to_pdf(ticket_id, source, destination, date, passengers, fare)

    flash(f"Ticket booked successfully! Ticket ID: {ticket_id}", "success")
    return send_file(pdf_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
