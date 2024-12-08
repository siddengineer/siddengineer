from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# Data storage
vehicles = []

# HTML and CSS embedded in Python
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Import Tracking</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
        }
        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 1rem;
        }
        main {
            max-width: 800px;
            margin: 20px auto;
            background: white;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        h1 {
            text-align: center;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #28a745;
            color: white;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        .error {
            color: red;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Vehicle Import Tracking System</h1>
    </header>
    <main>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
        <form method="POST" action="/add">
            <label for="vehicle_name">Vehicle Name:</label>
            <input type="text" id="vehicle_name" name="vehicle_name" required>

            <label for="importer_name">Importer Name:</label>
            <input type="text" id="importer_name" name="importer_name" required>

            <label for="shipment_status">Shipment Status:</label>
            <select id="shipment_status" name="shipment_status" required>
                <option value="Pending">Pending</option>
                <option value="In Transit">In Transit</option>
                <option value="Delivered">Delivered</option>
            </select>

            <label>Required Documents:</label>
            <input type="checkbox" id="bill_of_lading" name="documents" value="Bill of Lading">
            <label for="bill_of_lading">Bill of Lading</label><br>
            <input type="checkbox" id="customs_form" name="documents" value="Customs Form">
            <label for="customs_form">Customs Form</label><br>
            <input type="checkbox" id="insurance" name="documents" value="Insurance">
            <label for="insurance">Insurance</label><br>

            <button type="submit">Add Vehicle</button>
        </form>

        <h2>Tracked Vehicles</h2>
        {% if vehicles %}
        <table>
            <thead>
                <tr>
                    <th>Vehicle Name</th>
                    <th>Importer Name</th>
                    <th>Shipment Status</th>
                    <th>Documents</th>
                </tr>
            </thead>
            <tbody>
                {% for vehicle in vehicles %}
                <tr>
                    <td>{{ vehicle.vehicle_name }}</td>
                    <td>{{ vehicle.importer_name }}</td>
                    <td>{{ vehicle.shipment_status }}</td>
                    <td>{{ ', '.join(vehicle.documents) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p>No vehicles added yet.</p>
        {% endif %}
    </main>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_code, vehicles=vehicles, error=None)

@app.route('/add', methods=['POST'])
def add_vehicle():
    vehicle_name = request.form['vehicle_name']
    importer_name = request.form['importer_name']
    shipment_status = request.form['shipment_status']
    documents = request.form.getlist('documents')

    required_documents = {"Bill of Lading", "Customs Form", "Insurance"}
    missing_docs = required_documents - set(documents)

    if missing_docs:
        return render_template_string(html_code, vehicles=vehicles, error=f"Missing documents: {', '.join(missing_docs)}")

    vehicles.append({
        'vehicle_name': vehicle_name,
        'importer_name': importer_name,
        'shipment_status': shipment_status,
        'documents': documents
    })

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)