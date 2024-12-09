from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# This will hold our offers temporarily (in-memory storage)
offers = []

# HTML template with embedded CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Sellers Offers</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            margin: 20px 0;
        }
        input[type="text"], input[type="url"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #5cb85c;
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
            border-radius: 4px;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #4cae4c;
        }
        .offers {
            margin-top: 20px;
        }
        .offer {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Local Sellers Offers</h1>
        <form method="POST">
            <input type="text" name="seller_name" placeholder="Seller Name" required>
            <input type="text" name="offer" placeholder="Offer Details" required>
            <input type="url" name="link" placeholder="Link to Offer (URL)" required>
            <input type="submit" value="Submit Offer">
        </form>
        <div class="offers">
            <h2>Current Offers</h2>
            {% for offer in offers %}
                <div class="offer">
                    <strong>{{ offer.seller_name }}</strong><br>
                    <p>{{ offer.offer }}</p>
                    <a href="{{ offer.link }}" target="_blank">View Offer</a>
                </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get data from the form
        seller_name = request.form['seller_name']
        offer = request.form['offer']
        link = request.form['link']

        # Store offer in the list
        offers.append({'seller_name': seller_name, 'offer': offer, 'link': link})
        return redirect(url_for('home'))

    return render_template_string(HTML_TEMPLATE, offers=offers)

if __name__ == '__main__':
    app.run(debug=True)