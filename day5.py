import time
from plyer import notification
import tkinter as tk
from tkinter import simpledialog
import winsound  # For sound notification (Windows)

# Function to remind for a break
def remind_break():
    notification.notify(
        title="Take a Break!",
        message="You've been working for a while. Time to take a short break!",
        timeout=10  # notification will stay for 10 seconds
    )
    # Play a beep sound at 1000 Hz for 500 milliseconds (0.5 seconds)
    winsound.Beep(1000, 500)

# Countdown during the break
def break_countdown(minutes):
    for remaining in range(minutes * 60, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_left = f"{mins:02d}:{secs:02d}"
        print(f"Break Time Left: {time_left}", end="\r")
        time.sleep(1)

# Main loop to remind at intervals
def start_reminder():
    while True:
        time.sleep(1 * 60)  # Wait for 1 minute (for testing)
        remind_break()
        print("\nTaking a 5-minute break!")
        break_countdown(5)  # 5-minute break countdown

# Exit the reminder loop
def stop_reminder():
    root.quit()

# GUI for user to input interval
root = tk.Tk()
root.withdraw()  # Hide the main window

# Hardcoded reminder interval for testing (1 minute)
reminder_interval = 1
print(f"Reminders set every {reminder_interval} minute. Press Ctrl+C to stop the program.")

# Start the reminder loop
try:
    start_reminder()
except KeyboardInterrupt:
    print("\nProgram stopped by the user.")
    stop_reminder()
