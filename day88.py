from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML and CSS embedded
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cheaper Ticket Finder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cheaper Ticket Finder</h1>
        <form method="POST">
            <input type="text" name="city1" placeholder="Enter City 1" required>
            <input type="text" name="city2" placeholder="Enter City 2" required>
            <select name="class">
                <option value="economy">Economy</option>
                <option value="business">Business</option>
                <option value="first">First Class</option>
            </select>
            <button type="submit">Find Cheapest Ticket</button>
        </form>
        {% if result %}
        <div class="result">Cheapest Ticket: {{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# Mocked distances between cities (in km)
CITY_DISTANCES = {
    ("New York", "Los Angeles"): 3940,
    ("Delhi", "Mumbai"): 1400,
    ("London", "Paris"): 344,
    ("Tokyo", "Seoul"): 1150,
}

# Pricing logic constants
BASE_RATE_PER_KM = 0.1  # $ per km
CLASS_MULTIPLIERS = {
    "economy": 1.0,
    "business": 1.5,
    "first": 2.0,
}

@app.route("/", methods=["GET", "POST"])
def cheaper_ticket():
    result = None
    if request.method == "POST":
        city1 = request.form["city1"].strip().title()
        city2 = request.form["city2"].strip().title()
        travel_class = request.form["class"]

        # Calculate ticket price based on distance
        distance = CITY_DISTANCES.get((city1, city2)) or CITY_DISTANCES.get((city2, city1))
        if distance:
            base_price = distance * BASE_RATE_PER_KM
            final_price = base_price * CLASS_MULTIPLIERS[travel_class]
            result = f"${final_price:.2f} ({travel_class.capitalize()} Class)"
        else:
            result = "No ticket information available for these cities."

    return render_template_string(HTML_PAGE, result=result)

if __name__ == "__main__":
    app.run(debug=True)