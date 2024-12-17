from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory database to store export records
export_records = []

# Index Page with Tailwind CSS
index_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Export Records</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">
    <nav class="bg-blue-600 text-white py-4 text-center">
        <h1 class="text-2xl font-bold">Dak Ghar Niryat Kendra</h1>
    </nav>

    <div class="container mx-auto my-6 p-6 bg-white rounded shadow-md">
        <h2 class="text-xl font-semibold mb-4">Export Records</h2>
        {% if records %}
        <table class="table-auto w-full border-collapse border border-gray-200">
            <thead>
                <tr class="bg-blue-100">
                    <th class="border border-gray-200 px-4 py-2">Sender</th>
                    <th class="border border-gray-200 px-4 py-2">Receiver</th>
                    <th class="border border-gray-200 px-4 py-2">Weight (kg)</th>
                    <th class="border border-gray-200 px-4 py-2">Country</th>
                </tr>
            </thead>
            <tbody>
                {% for record in records %}
                <tr class="text-center">
                    <td class="border border-gray-200 px-4 py-2">{{ record.sender }}</td>
                    <td class="border border-gray-200 px-4 py-2">{{ record.receiver }}</td>
                    <td class="border border-gray-200 px-4 py-2">{{ record.weight }}</td>
                    <td class="border border-gray-200 px-4 py-2">{{ record.country }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p class="text-gray-500">No records available.</p>
        {% endif %}
        <a href="{{ url_for('add_export') }}" class="inline-block bg-blue-500 text-white px-4 py-2 mt-4 rounded hover:bg-blue-600">Add Export Record</a>
    </div>
</body>
</html>
"""

# Add Export Page with Tailwind CSS
add_export_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Export Record</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">
    <nav class="bg-blue-600 text-white py-4 text-center">
        <h1 class="text-2xl font-bold">Dak Ghar Niryat Kendra</h1>
    </nav>

    <div class="container mx-auto my-6 p-6 bg-white rounded shadow-md w-1/2">
        <h2 class="text-xl font-semibold mb-4">Add Export Record</h2>
        <form method="POST" action="{{ url_for('add_export') }}">
            <label class="block mb-2 font-medium">Sender Name</label>
            <input type="text" name="sender" class="w-full border px-4 py-2 mb-4 rounded" placeholder="Enter sender's name" required>

            <label class="block mb-2 font-medium">Receiver Name</label>
            <input type="text" name="receiver" class="w-full border px-4 py-2 mb-4 rounded" placeholder="Enter receiver's name" required>

            <label class="block mb-2 font-medium">Weight (kg)</label>
            <input type="number" step="0.01" name="weight" class="w-full border px-4 py-2 mb-4 rounded" placeholder="Enter weight" required>

            <label class="block mb-2 font-medium">Country</label>
            <input type="text" name="country" class="w-full border px-4 py-2 mb-4 rounded" placeholder="Enter country" required>

            <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Submit</button>
            <a href="{{ url_for('index') }}" class="ml-4 text-blue-500 hover:underline">Back to Records</a>
        </form>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(index_page, records=export_records)

@app.route('/add', methods=['GET', 'POST'])
def add_export():
    if request.method == 'POST':
        # Fetch form data
        sender = request.form['sender']
        receiver = request.form['receiver']
        weight = request.form['weight']
        country = request.form['country']

        # Add to the export records list
        export_records.append({
            'sender': sender,
            'receiver': receiver,
            'weight': weight,
            'country': country
        })

        # Redirect to the homepage
        return redirect(url_for('index'))

    # Render the add export form
    return render_template_string(add_export_page)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
