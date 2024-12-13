import tkinter as tk
from tkinter import messagebox

# Function to display safety checklist completion message
def check_safety():
    if all(var.get() for var in checks):
        messagebox.showinfo("Safety Check", "All safety measures are verified! You are good to go.")
    else:
        messagebox.showwarning("Safety Check", "Please complete all safety measures before proceeding.")

# Function to estimate days left for cylinder refill
def estimate_refill_days():
    try:
        cylinder_capacity = float(cylinder_capacity_entry.get())
        daily_usage = float(daily_usage_entry.get())
        
        if daily_usage <= 0:
            raise ValueError("Daily usage must be greater than 0.")
        
        days_left = cylinder_capacity / daily_usage
        messagebox.showinfo("Refill Estimate", f"Estimated days left for a refill: {days_left:.2f} days")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create main window
root = tk.Tk()
root.title("Gas Cylinder Safety & Monitoring Tool")

# Safety Checklist Section
tk.Label(root, text="Gas Cylinder Safety Checklist", font=("Arial", 14, "bold")).pack(pady=10)
safety_points = [
    "Check for gas leaks (soap solution test).",
    "Ensure proper ventilation in the room.",
    "Check the cylinder valve is closed when not in use.",
    "Verify the regulator and pipe connections.",
    "Keep flammable materials away from the cylinder."
]
checks = [tk.BooleanVar() for _ in safety_points]
for i, point in enumerate(safety_points):
    tk.Checkbutton(root, text=point, variable=checks[i]).pack(anchor='w')

tk.Button(root, text="Verify Safety", command=check_safety).pack(pady=10)

# Gas Consumption Monitoring Section
tk.Label(root, text="Gas Consumption Monitoring", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(root, text="Enter Cylinder Capacity (kg):").pack()
cylinder_capacity_entry = tk.Entry(root)
cylinder_capacity_entry.pack()

tk.Label(root, text="Enter Daily Usage (kg):").pack()
daily_usage_entry = tk.Entry(root)
daily_usage_entry.pack()

tk.Button(root, text="Estimate Refill Days", command=estimate_refill_days).pack(pady=10)

# Run the application
root.mainloop()