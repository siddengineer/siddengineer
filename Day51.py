import tkinter as tk
from tkintermapview import TkinterMapView
from geopy.distance import geodesic
import random
import time

# Initialize GUI
root = tk.Tk()
root.title("Simulated Real-Time GPS Tracker")
root.geometry("600x600")

# Map widget setup
map_widget = TkinterMapView(root, width=600, height=450, corner_radius=0)
map_widget.pack()

# Label for showing the total distance
total_distance_label = tk.Label(root, text="Total Distance: 0.00 km", font=("Arial", 14))
total_distance_label.pack(pady=10)

# Tracking variables
total_distance = 0.0
previous_location = (28.7041, 77.1025)  # Start location (e.g., New Delhi coordinates)

# Function to generate simulated GPS data
def get_simulated_gps_data():
    # Small random change to latitude and longitude to simulate movement
    lat_change = random.uniform(-0.0005, 0.0005)
    lon_change = random.uniform(-0.0005, 0.0005)
    
    latitude = previous_location[0] + lat_change
    longitude = previous_location[1] + lon_change
    return (latitude, longitude)

# Function to update tracker
def update_tracker():
    global previous_location, total_distance

    # Get the simulated GPS coordinates
    current_location = get_simulated_gps_data()

    # Calculate distance if we have a previous location
    if previous_location:
        distance_segment = geodesic(previous_location, current_location).kilometers
        total_distance += distance_segment

    # Update map and display
    map_widget.set_position(*current_location)
    map_widget.set_marker(*current_location, text="Current Position")
    total_distance_label.config(text=f"Total Distance: {total_distance:.2f} km")

    # Update previous location for the next calculation
    previous_location = current_location

    # Schedule next update (every 3 seconds)
    root.after(3000, update_tracker)

# Start live tracker
update_tracker()

root.mainloop()