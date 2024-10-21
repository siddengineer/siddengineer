import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import getpass  # To hide the password input

# Create a database to store user and subscription info
def create_database():
    conn = sqlite3.connect('netflix_subscriptions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        plan TEXT,
        start_date TEXT,
        end_date TEXT)''')
    conn.commit()
    conn.close()

# Register a user
def register_user(name, email, password, plan):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  # 30-day subscription
    conn = sqlite3.connect('netflix_subscriptions.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password, plan, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, password, plan, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    print(f"{name} registered successfully!")

# Display available subscription plans
def show_plans():
    plans = {
        'Basic': {'price': 649, 'quality': 'SD', 'screens': 1},
        'Standard': {'price': 899, 'quality': 'HD', 'screens': 2},
        'Premium': {'price': 1099, 'quality': '4K', 'screens': 4},
    }
    print("\nAvailable Subscription Plans (INR):")
    for plan, details in plans.items():
        print(f"{plan}: ₹{details['price']} - {details['quality']} quality, {details['screens']} screens")
    return plans

# Check subscription status and send reminders
def check_subscription_status():
    conn = sqlite3.connect('netflix_subscriptions.db')
    c = conn.cursor()
    c.execute("SELECT name, email, plan, end_date FROM users")
    users = c.fetchall()
    print("\n--- Subscription Status ---")
    for user in users:
        name, email, plan, end_date = user
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days_remaining = (end_date - datetime.now()).days
        if days_remaining > 0:
            print(f"{name} ({email}) - Plan: {plan}, Days Remaining: {days_remaining}")
        else:
            print(f"{name} ({email}) - Plan: {plan}, Expired!")
    conn.close()

# Send renewal reminder
def send_renewal_reminder(name, email, days_remaining):
    subject = "Netflix Subscription Renewal Reminder"
    body = f"Dear {name},\nYour Netflix subscription will expire in {days_remaining} days. Please renew your subscription!"
    send_email(email, subject, body)

# Simulated email function
def send_email(recipient_email, subject, body):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Process payment (simulated)
def process_payment(name, plan, amount):
    print(f"Processing payment of ₹{amount} for {name} (Plan: {plan})")
    # Simulate successful payment
    print("Payment successful!\n")
    return True

# Main menu
def main():
    create_database()
    while True:
        print("\n--- Netflix Subscription System ---")
        print("1. Register")
        print("2. View Plans")
        print("3. Check Subscription Status")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = getpass.getpass("Enter your password (hidden): ")  # Hides password input
            plans = show_plans()
            plan = input("Choose a subscription plan (Basic, Standard, Premium): ").capitalize()

            if plan in plans:
                amount = plans[plan]['price']
                if process_payment(name, plan, amount):
                    register_user(name, email, password, plan)
            else:
                print("Invalid plan selected. Please try again.")

        elif choice == '2':
            show_plans()

        elif choice == '3':
            check_subscription_status()

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
