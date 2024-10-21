from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Car lock status (False = locked, True = unlocked)
car_status = {"locked": True}
otp_generated = None  # Variable to store the generated OTP

# HTML template for the main interface
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Vehicle Control with OTP</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            padding-top: 50px;
        }
        h1 {
            color: #333;
        }
        .status {
            font-size: 2em;
            margin-bottom: 20px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 1.5em;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        .button.lock {
            background-color: #dc3545;
        }
        .button.unlock {
            background-color: #28a745;
        }
        .otp-input {
            padding: 10px;
            font-size: 1.2em;
            border-radius: 5px;
            border: 1px solid #ccc;
            width: 150px;
        }
        .heading {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <h1 class="heading">Remote Vehicle Control System</h1>
    <div class="status">
        Car is currently: <strong>{{ status }}</strong>
    </div>

    {% if not otp_requested %}
        <div>
            <a href="/lock"><button class="button lock">Lock Car</button></a>
            <a href="/request-otp"><button class="button unlock">Unlock Car</button></a>
        </div>
    {% elif otp_requested %}
        <div>
            <p><strong>OTP sent to your phone (simulated on desktop).</strong></p>
            <form method="POST" action="/verify-otp">
                <input type="text" name="otp" class="otp-input" placeholder="Enter OTP" required>
                <br><br>
                <button type="submit" class="button unlock">Submit OTP</button>
            </form>
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    status = "locked" if car_status["locked"] else "unlocked"
    otp_requested = session.get('otp_requested', False)
    return render_template_string(html_template, status=status, otp_requested=otp_requested)

@app.route('/lock')
def lock_car():
    car_status["locked"] = True
    session['otp_requested'] = False
    return redirect(url_for('index'))

@app.route('/request-otp')
def request_otp():
    global otp_generated
    otp_generated = random.randint(1000, 9999)  # Generate a 4-digit OTP
    session['otp_requested'] = True
    print(f"Simulated OTP: {otp_generated}")  # Simulating sending OTP (printing on desktop)
    return redirect(url_for('index'))

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form.get('otp')
    if entered_otp == str(otp_generated):
        car_status["locked"] = False
        session['otp_requested'] = False
        return redirect(url_for('index'))
    else:
        return "<h2>Invalid OTP. Please try again.</h2><br><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)