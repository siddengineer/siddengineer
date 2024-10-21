import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Create or connect to a SQLite database
conn = sqlite3.connect('scheme_registration.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS applicants 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, address TEXT, income REAL, reg_id TEXT)''')

# Function to generate registration ID
def generate_registration_id():
    return f"REG{random.randint(1000, 9999)}"

# Function to submit data
def submit_data():
    name = entry_name.get()
    age = int(entry_age.get())
    address = entry_address.get()
    income = float(entry_income.get())
    
    # Eligibility check
    if age < 18 or age > 25:
        messagebox.showerror("Eligibility Error", "Age must be between 10 and 18.")
        return
    if income > 250000:  # Example income threshold
        messagebox.showerror("Eligibility Error", "Income must be below 50,000.")
        return

    reg_id = generate_registration_id()

    # Insert data into the database
    c.execute("INSERT INTO applicants (name, age, address, income, reg_id) VALUES (?, ?, ?, ?, ?)",
              (name, age, address, income, reg_id))
    conn.commit()

    messagebox.showinfo("Success", f"Registration successful! Your ID is {reg_id}")

    # Clear form fields
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_income.delete(0, tk.END)

# Create a Tkinter window
root = tk.Tk()
root.title("Mazi Ladki Bahin Yojana - Registration Portal")

# Labels and entry fields
tk.Label(root, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)

tk.Label(root, text="Address").grid(row=2, column=0)
entry_address = tk.Entry(root)
entry_address.grid(row=2, column=1)

tk.Label(root, text="Family Income").grid(row=3, column=0)
entry_income = tk.Entry(root)
entry_income.grid(row=3, column=1)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=4, column=1)

# Start the Tkinter loop
root.mainloop()

# Close the database connection when done
conn.close()
