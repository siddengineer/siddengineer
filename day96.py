import time
import geopy.distance
from plyer import notification
from twilio.rest import Client
import random
from flask import Flask, render_template_string, jsonify

# Twilio Account SID and Auth Token (use your own credentials)
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE = 'your_twilio_phone_number'
TO_PHONE = 'recipient_phone_number'

# Predefined coordinates of the ATM zone (latitude, longitude)
ATM_ZONE = (28.704060, 77.102493)  # Example coordinates (Delhi)

# Flask app setup
app = Flask(__name__)

# Function to send an SMS alert to the trusted contact
def send_sms_alert(location):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Emergency Alert: User at location {location}. Please assist immediately!",
        from_=TWILIO_PHONE,
        to=TO_PHONE
    )
    print(f"Alert sent to {TO_PHONE}")

# HTML + Tailwind CSS Frontend Template
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATM Security Assistant</title>
    <script src="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.js"></script>
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
    </style>
</head>

<body class="bg-gray-100">
    <div class="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-lg mt-10">
        <h2 class="text-2xl font-semibold text-center text-blue-600 mb-6">ATM Security Personal Assistant</h2>

        <!-- Location Display -->
        <div id="location" class="text-center text-lg text-gray-800 mb-6">
            <p>Current Location: <span id="lat">N/A</span>, <span id="long">N/A</span></p>
        </div>

        <!-- Emergency Button -->
        <div class="flex justify-center mb-6">
            <button id="emergencyButton" class="bg-red-600 text-white px-6 py-2 rounded-full text-lg">
                Press Emergency Button
            </button>
        </div>

        <!-- Safety Tips -->
        <div class="text-center mb-6">
            <h3 class="text-xl font-medium text-gray-700">Safety Tips:</h3>
            <ul class="list-disc list-inside text-left text-gray-600">
                <li>Do not accept help from strangers.</li>
                <li>Always cover your PIN while entering it.</li>
                <li>Be aware of your surroundings at the ATM.</li>
            </ul>
        </div>

        <!-- Alerts Section -->
        <div id="alerts" class="text-center">
            <p id="alertMessage" class="text-xl text-green-600 font-semibold">Safe to Use ATM</p>
        </div>
    </div>

    <script>
        // Simulate GPS Location Update
        function updateLocation() {
            fetch('/get_location')
                .then(response => response.json())
                .then(data => {
                    const lat = data.location.lat;
                    const long = data.location.long;
                    const alertMessage = data.alert_message;

                    document.getElementById('lat').textContent = lat.toFixed(6);
                    document.getElementById('long').textContent = long.toFixed(6);
                    document.getElementById('alertMessage').textContent = alertMessage;

                    if (alertMessage === "Be Cautious! You're near an ATM.") {
                        document.getElementById('alertMessage').classList.replace('text-green-600', 'text-yellow-600');
                    } else if (alertMessage === "Emergency! Help is on the way.") {
                        document.getElementById('alertMessage').classList.replace('text-yellow-600', 'text-red-600');
                    } else {
                        document.getElementById('alertMessage').classList.replace('text-yellow-600', 'text-green-600');
                    }
                })
        }

        // Handle Emergency Button Press
        document.getElementById('emergencyButton').addEventListener('click', () => {
            alert("Emergency Button Pressed! Help is on the way.");
            document.getElementById('alertMessage').textContent = "Emergency! Help is on the way.";
            document.getElementById('alertMessage').classList.replace('text-green-600', 'text-red-600');
        });

        // Update location every 5 seconds to simulate real-time tracking
        setInterval(updateLocation, 5000);
    </script>
</body>

</html>
"""

# Function to simulate the emergency button press and location tracking
@app.route('/get_location', methods=['GET'])
def track_user_location():
    # Simulate GPS tracking by generating random coordinates near the ATM
    user_location = ATM_ZONE
    user_lat = ATM_ZONE[0] + random.uniform(-0.0002, 0.0002)
    user_lon = ATM_ZONE[1] + random.uniform(-0.0002, 0.0002)
    dist = geopy.distance.distance((user_lat, user_lon), ATM_ZONE).meters
    
    alert_message = "Safe to Use ATM"
    if dist < 100:
        alert_message = "Be Cautious! You're near an ATM."
    
    emergency_button_pressed = random.choice([True, False])
    if emergency_button_pressed:
        send_sms_alert((user_lat, user_lon))
        alert_message = "Emergency! Help is on the way."
    
    return jsonify({
        'location': {'lat': user_lat, 'long': user_lon},
        'alert_message': alert_message
    })

# Main route to serve the HTML
@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)