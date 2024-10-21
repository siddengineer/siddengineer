import tkinter as tk
from tkinter import messagebox
import geocoder
import requests

# Function to get user's location using IP
def get_location():
    try:
        g = geocoder.ip('me')
        city, country = g.city, g.country
        if city and country:
            return city, country
        else:
            return "Unknown", "Unknown"
    except Exception as e:
        return "Unknown", "Unknown"

# Function to fetch emergency contacts based on location
def get_emergency_contacts(country):
    emergency_numbers = {
        'India': {'Police': '100', 'Ambulance': '102'},
        
        # Add more countries and their respective numbers
    }
    return emergency_numbers.get(country, {'Police': '12234567', 'Ambulance': '12345678'})

# Function to fetch safety tips based on the selected activity
def get_safety_tips(activity):
    tips = {
        'Selfie': "Be aware of your surroundings. Avoid taking selfies near cliffs, ledges, or bodies of water.",
        'Solo Travel': "Share your itinerary with family or friends. Avoid isolated areas and stay vigilant.",
        'Alcohol': "Excessive drinking can impair judgment. Stay in groups and avoid engaging in dangerous activities.",
        'Reels': "Creating reels in dangerous places can lead to accidents. Prioritize your safety over social media trends.",
        'Overconfidence': "Don't overestimate your abilities in unfamiliar situations. Always plan and stay cautious."
    }
    return tips.get(activity, "Stay safe and enjoy responsibly!")

# Function to display safety tips and emergency contacts
def show_info(activity):
    city, country = get_location()
    contacts = get_emergency_contacts(country)
    safety_tip = get_safety_tips(activity)
    
    # Display the information in a message box
    info_message = f"Location: {city}, {country}\n\n"
    info_message += f"Police: {contacts['Police']}\nAmbulance: {contacts['Ambulance']}\n\n"
    info_message += f"Safety Tip for {activity}:\n{safety_tip}"
    
    messagebox.showinfo("Safety Info", info_message)

# Function to report a dangerous location
def report_danger():
    city, country = get_location()
    danger_report = danger_entry.get()
    
    if danger_report:
        with open("reports.txt", "a") as file:
            file.write(f"Report: {danger_report}, Location: {city}, {country}\n")
        
        messagebox.showinfo("Report Submitted", "Thank you for your report!")
        danger_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid danger report.")

# Function to display user-generated reports
def show_reports():
    try:
        with open("reports.txt", "r") as file:
            reports = file.read()
        messagebox.showinfo("Danger Reports", reports)
    except FileNotFoundError:
        messagebox.showinfo("Danger Reports", "No danger reports found.")

# GUI window setup
def create_gui():
    window = tk.Tk()
    window.title("Travel Safety Alert and Rescue Info")

    # Welcome label
    welcome_label = tk.Label(window, text="Select your activity to get safety tips and emergency numbers:")
    welcome_label.pack(pady=10)

    # Buttons for different activities
    activities = ['Selfie', 'Solo Travel', 'Alcohol', 'Reels', 'Overconfidence']
    
    for activity in activities:
        btn = tk.Button(window, text=activity, width=20, command=lambda act=activity: show_info(act))
        btn.pack(pady=5)

    # Label for danger report
    report_label = tk.Label(window, text="Report a Dangerous Spot or Incident:")
    report_label.pack(pady=10)
    
    global danger_entry
    danger_entry = tk.Entry(window, width=50)
    danger_entry.pack(pady=5)

    # Button to submit danger report
    report_btn = tk.Button(window, text="Submit Report", command=report_danger)
    report_btn.pack(pady=5)

    # Button to show danger reports
    show_reports_btn = tk.Button(window, text="View Danger Reports", command=show_reports)
    show_reports_btn.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()

# Run the GUI
create_gui()