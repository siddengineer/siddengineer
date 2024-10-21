import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Initialize the main window
root = tk.Tk()
root.title("10K Marathon Registration Portal")
root.geometry("500x600")
root.configure(bg="#d4e6f1")  # Set background color

# Fonts and styles
title_font = ("Arial", 20, "bold")
label_font = ("Helvetica", 12)
button_font = ("Arial", 12, "bold")

# Function to display route and time
def display_route_time():
    messagebox.showinfo(
        "Marathon Route & Time",
        "Start Time: 6:00 AM on 20th October 2024\n"
        "Route: Central Park -> Elm Street -> Riverside Road -> Greenway Plaza (10 km)"
    )

# Function for registration
def register_user():
    name = name_entry.get()
    category = category_var.get()
    tshirt_size = tshirt_size_var.get()
    address = address_entry.get()

    if not name or not address or not category or not tshirt_size:
        messagebox.showwarning("Incomplete", "Please fill all fields!")
        return
    
    # Show confirmation popup
    confirmation_msg = f"Thank you, {name}!\nYou are registered in the '{category}' category.\nT-shirt Size: {tshirt_size}\nAddress: {address}"
    messagebox.showinfo("Registration Successful", confirmation_msg)

    # T-shirt collection info
    collect_time = datetime.now().strftime("%d %B %Y, %I:%M %p")
    tshirt_msg = f"T-shirt collection will be available from {collect_time}."
    messagebox.showinfo("T-shirt Collection", tshirt_msg)

# Create the layout and design
header_frame = tk.Frame(root, bg="#2874A6")
header_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

header_label = tk.Label(header_frame, text="10K Marathon Registration", font=title_font, fg="white", bg="#2874A6")
header_label.pack(pady=10)

# Name entry
name_label = tk.Label(root, text="Enter your Name:", font=label_font, bg="#d4e6f1")
name_label.grid(row=1, column=0, pady=5, sticky="e")
name_entry = tk.Entry(root, font=label_font, width=30)
name_entry.grid(row=1, column=1, pady=5)

# Category selection
category_label = tk.Label(root, text="Select Category:", font=label_font, bg="#d4e6f1")
category_label.grid(row=2, column=0, pady=5, sticky="e")
category_var = tk.StringVar(value="Men")
categories = [("Men", "Men"), ("Women", "Women"), ("Senior Citizens", "Senior Citizens")]

category_frame = tk.Frame(root, bg="#d4e6f1")
category_frame.grid(row=2, column=1, pady=5, sticky="w")

for text, value in categories:
    tk.Radiobutton(category_frame, text=text, variable=category_var, value=value, font=label_font, bg="#d4e6f1").pack(anchor=tk.W)

# T-shirt size selection
tshirt_label = tk.Label(root, text="Select T-shirt Size:", font=label_font, bg="#d4e6f1")
tshirt_label.grid(row=3, column=0, pady=5, sticky="e")
tshirt_size_var = tk.StringVar(value="M")
sizes = ["S", "M", "L", "XL", "XXL"]

tshirt_frame = tk.Frame(root, bg="#d4e6f1")
tshirt_frame.grid(row=3, column=1, pady=5, sticky="w")

for size in sizes:
    tk.Radiobutton(tshirt_frame, text=size, variable=tshirt_size_var, value=size, font=label_font, bg="#d4e6f1").pack(anchor=tk.W)

# Address entry
address_label = tk.Label(root, text="Enter your Address:", font=label_font, bg="#d4e6f1")
address_label.grid(row=4, column=0, pady=5, sticky="e")
address_entry = tk.Entry(root, font=label_font, width=30)
address_entry.grid(row=4, column=1, pady=5)

# Submit button
submit_button = tk.Button(root, text="Register", font=button_font, bg="#1B4F72", fg="white", command=register_user)
submit_button.grid(row=5, column=0, columnspan=2, pady=20)

# Route and time button
route_button = tk.Button(root, text="View Route & Time", font=button_font, bg="#1B4F72", fg="white", command=display_route_time)
route_button.grid(row=6, column=0, columnspan=2, pady=10)

# Footer
footer_label = tk.Label(root, text="Thank you for registering! We look forward to seeing you at the event.", font=label_font, bg="#d4e6f1", fg="#2874A6")
footer_label.grid(row=7, column=0, columnspan=2, pady=30)

# Run the main loop
root.mainloop()