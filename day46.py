import random
import string
import tkinter as tk
from tkinter import messagebox

# Function to generate a random captcha
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    captcha_label.config(text=captcha_text)
    captcha_label.config(fg=random.choice(["blue", "green", "red", "purple", "orange"]))

# Function to verify the entered captcha
def verify_captcha():
    entered_text = captcha_entry.get()
    captcha_text = captcha_label.cget("text")
    
    if entered_text == captcha_text:
        messagebox.showinfo("Success", "Captcha Verified!")
    else:
        messagebox.showerror("Error", "Invalid Captcha. Try Again!")
    generate_captcha()  # Generate a new captcha for next verification
    captcha_entry.delete(0, tk.END)  # Clear the entry box

# Create the main tkinter window
root = tk.Tk()
root.title("Captcha Generator & Verifier")
root.geometry("300x250")

# Display the captcha text
captcha_label = tk.Label(root, text="", font=("Arial", 24))
captcha_label.pack(pady=10)

# Input field for the user to enter captcha
captcha_entry = tk.Entry(root, font=("Arial", 14))
captcha_entry.pack(pady=10)

# Button to verify the captcha
verify_button = tk.Button(root, text="Verify Captcha", command=verify_captcha, font=("Arial", 14))
verify_button.pack(pady=10)

# Button to refresh the captcha manually
refresh_button = tk.Button(root, text="Refresh Captcha", command=generate_captcha, font=("Arial", 12))
refresh_button.pack(pady=10)

# Generate an initial captcha when the app starts
generate_captcha()

# Start the tkinter loop
root.mainloop()