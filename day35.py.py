import os
import time
import logging
import tkinter as tk
from tkinter import scrolledtext
import threading

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
logging.basicConfig(
    filename='logs/access_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a'  # Append to the log file instead of overwriting
)

# Simulated function to track employee access
def track_employee_access(directory):
    while True:
        time.sleep(5)  # Check every 5 seconds
        # Simulate access to sensitive files
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):  # Assuming .txt files are sensitive
                employee_id = "Employee123"  # Simulated employee ID
                logging.info(f"{employee_id} accessed file: {filename}")
                print(f"Alert: {employee_id} accessed {filename}")

class LogViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Access Logs")
        self.text_area = scrolledtext.ScrolledText(master, width=50, height=20)
        self.text_area.pack()
        self.update_logs()

    def update_logs(self):
        try:
            with open('logs/access_log.log', 'r') as log_file:
                self.text_area.delete(1.0, tk.END)  # Clear previous content
                self.text_area.insert(tk.END, log_file.read())
        except FileNotFoundError:
            self.text_area.insert(tk.END, "No logs available yet.\n")
        self.master.after(5000, self.update_logs)  # Refresh every 5 seconds

if __name__ == "__main__":
    # Ensure the monitored directory exists
    monitored_directory = monitored_directory = "C:/Users/K/Desktop/sensitivedata"


    if not os.path.exists(monitored_directory):
        print(f"Directory '{monitored_directory}' does not exist.")
        exit(1)

    # Start tracking access in a separate thread
    access_thread = threading.Thread(target=track_employee_access, args=(monitored_directory,))
    access_thread.daemon = True  # Exit thread when the main program exits
    access_thread.start()

    # Start the Tkinter GUI
    root = tk.Tk()
    viewer = LogViewer(root)
    root.mainloop()
