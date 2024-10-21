import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import os
from plyer import notification
import threading
import matplotlib.pyplot as plt

# Functions

# 1. Mood Logger
def log_mood(mood):
    with open("mood_log.txt", "a") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        file.write(f"{time} - {mood}\n")
    messagebox.showinfo("Logged", f"Mood '{mood}' logged successfully!")
    
    # Display supportive message
    if mood == "Stressed":
        messagebox.showinfo("Support", "Take a deep breath. You can overcome anything!")
    elif mood == "Sad":
        messagebox.showinfo("Support", "It's okay to feel sad sometimes. Try calling home!")
    elif mood == "Happy":
        messagebox.showinfo("Support", "Stay positive and keep up the great work!")

# 2. Study Reminder
def set_study_reminder():
    time = study_time.get()
    if time:
        threading.Thread(target=study_reminder_thread, args=(time,)).start()
        messagebox.showinfo("Reminder Set", f"Reminder set for {time}!")
    else:
        messagebox.showwarning("Warning", "Please set a valid time.")

def study_reminder_thread(time):
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == time:
            notification.notify(
                title="Study Time!",
                message="It's time to start your study session!",
                timeout=10
            )
            break

# 3. Health & Food Logger
def log_health(food, water):
    with open("health_log.txt", "a") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        file.write(f"{time} - Food: {food}, Water: {water} glasses\n")
    messagebox.showinfo("Logged", "Health data logged successfully!")

def show_health_trend():
    dates, water_intakes = [], []
    if os.path.exists("health_log.txt"):
        with open("health_log.txt", "r") as file:
            for line in file:
                parts = line.split(" - ")
                dates.append(parts[0])
                water = int(parts[1].split(",")[1].split(":")[1].strip().split()[0])
                water_intakes.append(water)
        
        plt.plot(dates, water_intakes, marker='o')
        plt.title("Water Intake Over Time")
        plt.xlabel("Date")
        plt.ylabel("Water Intake (glasses)")
        plt.xticks(rotation=45)
        plt.show()
    else:
        messagebox.showinfo("No Data", "No health data available.")

# 4. Message Home Feature
def send_message_home():
    message = home_message.get()
    if message:
        with open("message_home.txt", "a") as file:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            file.write(f"{time} - Message to Parents: {message}\n")
        messagebox.showinfo("Sent", "Message sent to parents successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter a message.")

# 5. Meditation/Relaxation
def start_meditation():
    messagebox.showinfo("Relax", "Take 5 minutes to focus on your breathing.")
    # Simple breathing guide - could be expanded with more features
    for i in range(3):
        messagebox.showinfo("Breath In", "Breath in deeply...")
        root.after(3000)  # Pause for 3 seconds
        messagebox.showinfo("Breath Out", "Breath out slowly...")
        root.after(3000)  # Pause for 3 seconds

# GUI

root = tk.Tk()
root.title("Hostel Companion App")
root.geometry("500x500")

# Tabbed interface for different features
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Mood Tracker")
tabControl.add(tab2, text="Study Buddy")
tabControl.add(tab3, text="Health & Food")
tabControl.add(tab4, text="Message Home")
tabControl.add(tab5, text="Meditation")

tabControl.pack(expand=1, fill="both")

# Tab 1: Mood Tracker
mood_label = tk.Label(tab1, text="How are you feeling today?", font=("Arial", 14))
mood_label.pack(pady=10)

moods = ["Happy", "Stressed", "Sad", "Excited"]
for mood in moods:
    mood_button = tk.Button(tab1, text=mood, width=20, command=lambda m=mood: log_mood(m))
    mood_button.pack(pady=5)

# Tab 2: Study Buddy
study_label = tk.Label(tab2, text="Set a study reminder (HH:MM):", font=("Arial", 12))
study_label.pack(pady=10)

study_time = tk.Entry(tab2)
study_time.pack(pady=5)

set_study_button = tk.Button(tab2, text="Set Reminder", command=set_study_reminder)
set_study_button.pack(pady=10)

# Tab 3: Health & Food
food_label = tk.Label(tab3, text="What did you eat today?", font=("Arial", 12))
food_label.pack(pady=5)

food_entry = tk.Entry(tab3)
food_entry.pack(pady=5)

water_label = tk.Label(tab3, text="How many glasses of water?", font=("Arial", 12))
water_label.pack(pady=5)

water_entry = tk.Entry(tab3)
water_entry.pack(pady=5)

log_health_button = tk.Button(tab3, text="Log Health", command=lambda: log_health(food_entry.get(), water_entry.get()))
log_health_button.pack(pady=10)

show_trend_button = tk.Button(tab3, text="Show Health Trend", command=show_health_trend)
show_trend_button.pack(pady=5)

# Tab 4: Message Home
home_label = tk.Label(tab4, text="Send a message home:", font=("Arial", 12))
home_label.pack(pady=10)

home_message = tk.Entry(tab4, width=40)
home_message.pack(pady=5)

send_message_button = tk.Button(tab4, text="Send Message", command=send_message_home)
send_message_button.pack(pady=10)

# Tab 5: Meditation
meditation_label = tk.Label(tab5, text="Need a moment to relax?", font=("Arial", 12))
meditation_label.pack(pady=10)

start_meditation_button = tk.Button(tab5, text="Start Meditation", command=start_meditation)
start_meditation_button.pack(pady=10)

root.mainloop()