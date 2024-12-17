from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simulation Parameters
initial_water_level = 100  # Starting water level (in meters)
leak_rate = 5              # Leak rate per second
threshold_level = 20       # Critical water level threshold

# Home Route (HTML + Tailwind CSS Embedded)
@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dam Water Leakage Simulation</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Water Container Background with Dam Image */
        #water-container {
            background-image: url('/static/dam.jpg');
            background-size: cover;
            background-position: center;
            position: relative;
            height: 200px;
            border: 2px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        #water-level {
            position: absolute;
            bottom: 0;
            width: 100%;
            background-color: #3B82F6; /* Default Blue Color */
            transition: all 0.5s ease-in-out;
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">

    <div class="bg-white shadow-lg rounded-lg p-6 w-full max-w-md text-center">
        <h1 class="text-2xl font-bold text-gray-800 mb-4">🚰 Dam Water Leakage Simulation</h1>
        <div id="water-container">
            <div id="water-level"></div>
        </div>
        <p id="status" class="mt-4 text-gray-600">Water Level: 100 meters</p>
        <button id="start-btn" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Start Simulation
        </button>
    </div>

    <script>
        document.getElementById('start-btn').addEventListener('click', () => {
            console.log("Button Clicked"); // Debugging the button click
            fetch('/simulate')
                .then(response => response.json())
                .then(data => {
                    console.log("Data Received: ", data); // Debugging received data
                    let index = 0;
                    const waterLevelDiv = document.getElementById('water-level');
                    const statusText = document.getElementById('status');
                    const containerHeight = 200; // Height of the container

                    function updateWaterLevel() {
                        if (index >= data.length) {
                            statusText.textContent = "⚠ Dam Fully Drained!";
                            return;
                        }

                        const waterLevel = data[index].water_level;
                        const isCritical = data[index].is_critical;

                        const heightPercent = (waterLevel / 100) * containerHeight;
                        waterLevelDiv.style.height = heightPercent + "px";
                        waterLevelDiv.style.backgroundColor = isCritical ? "#EF4444" : "#3B82F6"; // Red at critical level

                        statusText.textContent = `Water Level: ${waterLevel.toFixed(2)} meters`;

                        if (isCritical) {
                            statusText.innerHTML += " ⚠ Critical Level!";
                        }

                        index++;
                        setTimeout(updateWaterLevel, 500);
                    }

                    updateWaterLevel();
                })
                .catch(error => {
                    console.error('Error fetching simulation data:', error);
                });
        });
    </script>
</body>
</html>
    """)

# Route to Simulate Water Leakage
@app.route('/simulate')
def simulate():
    water_level = initial_water_level
    water_data = []

    # Simulate water level decrease
    while water_level > 0:
        water_data.append({
            'water_level': water_level,
            'is_critical': water_level <= threshold_level
        })
        water_level -= leak_rate
        if water_level < 0:
            water_level = 0

    return jsonify(water_data)

if __name__ == '__main__':
    app.run(debug=True)
