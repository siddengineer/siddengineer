import pandas as pd
from flask import Flask, request, render_template_string, jsonify

# Initialize Flask app
app = Flask(__name__)

def load_and_prepare_data(train_path, test_path):
    """Load data, validate columns, and handle missing values."""
    # Load the datasets
    try:
        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)
    except Exception as e:
        return None, None, None, None, f"Error loading CSV files: {e}"

    # Clean column names
    train_data.columns = train_data.columns.str.strip()
    test_data.columns = test_data.columns.str.strip()

    # Print the columns to debug
    print("Train CSV Columns:", train_data.columns.tolist())
    print("Test CSV Columns:", test_data.columns.tolist())

    # Check for required columns (no required columns since we're removing price)
    required_columns = []  # No required columns

    for col in required_columns:
        if col not in train_data.columns:
            return None, None, None, None, f"Missing required column in training data: {col}"
        if col not in test_data.columns:
            return None, None, None, None, f"Missing required column in testing data: {col}"

    # No features or target
    return None, None, None, None, None

# Load the training and testing data
X_train, y_train, X_test, y_test, error_message = load_and_prepare_data(
    r'C:\Users\K\Documents\coding\python\SIDDENGINEER PYTHON PROJECTS\train.csv', 
    r'C:\Users\K\Documents\coding\python\SIDDENGINEER PYTHON PROJECTS\test.csv'
)

if error_message:
    print(error_message)
    exit()

# Use a default value for prediction (no actual training since we're removing the price)
dummy_prediction = 100000  # Placeholder prediction value

# HTML Template as a String
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Price Prediction</title>
</head>
<body>
    <h2>Car Price Prediction</h2>
    <form action="/predict" method="POST">
        <label for="car_name">Enter Car Name:</label>
        <input type="text" id="car_name" name="car_name" required><br><br>
        <button type="submit">Predict Price</button>
    </form>
    <div id="result"></div>
</body>
</html>
"""

# Define the home route
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Using a dummy prediction
        return jsonify({'predicted_price': f'The estimated price is ₹{round(dummy_prediction, 2)}'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
