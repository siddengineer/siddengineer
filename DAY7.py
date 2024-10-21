import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# File to store entries
file_name = "food_collection.csv"

# Function to add food collection entry
def add_entry(donor_name, food_type, quantity, contact_info):
    entry = {
        "Donor Name": donor_name,
        "Food Type": food_type,
        "Quantity (kg)": quantity,
        "Contact Info": contact_info,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Write the entry to a CSV file
    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=entry.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(entry)

    # Ask user if they want to see the thank-you message
    show_message = messagebox.askyesno("Thank You Message", "Do you want to generate thank you message?")
    
    if show_message:
        show_thank_you_message(donor_name)

# Function to show thank you message
def show_thank_you_message(donor_name):
    thank_you_window = tk.Toplevel(root)
    thank_you_window.title("Thank You")

    # Load the dog footprint image
    image_path = "python/dog print.jpg"
    if not os.path.exists(image_path):
        messagebox.showerror("File Error", f"Image not found at {image_path}")
        return

    try:
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load image: {e}")
        return

    # Add the donor's name to the image
    draw = ImageDraw.Draw(image)
    
    # Use a custom font
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Ensure the font file exists
    except IOError:
        messagebox.showerror("Font Error", "Font file not found")
        return

    # Add the text "Thank you [donor_name]!" to the image
    text = f"Thank you {donor_name}!"
    text_position = (10, 130)  # Adjust text position if needed
    draw.text(text_position, text, (0, 0, 0), font=font)

    # Convert to a Tkinter-compatible image
    img = ImageTk.PhotoImage(image)

    # Create a label for the image
    img_label = tk.Label(thank_you_window, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)

    # Create a label for the thank-you text
    message_label = tk.Label(thank_you_window, text=f"Thank you {donor_name} for feeding!", font=("Helvetica", 16))
    message_label.pack(pady=10)

    # Button to close the thank-you window
    close_button = tk.Button(thank_you_window, text="Close", command=thank_you_window.destroy)
    close_button.pack(pady=10)

# Main program window
def main_window():
    global root
    root = tk.Tk()
    root.title("Food Collection for Stray Dogs")

    tk.Label(root, text="Donor Name:").pack(pady=5)
    donor_name_entry = tk.Entry(root)
    donor_name_entry.pack(pady=5)

    tk.Label(root, text="Food Type:").pack(pady=5)
    food_type_entry = tk.Entry(root)
    food_type_entry.pack(pady=5)

    tk.Label(root, text="Quantity (kg):").pack(pady=5)
    quantity_entry = tk.Entry(root)
    quantity_entry.pack(pady=5)

    tk.Label(root, text="Contact Info:").pack(pady=5)
    contact_info_entry = tk.Entry(root)
    contact_info_entry.pack(pady=5)

    def submit():
        donor_name = donor_name_entry.get()
        food_type = food_type_entry.get()
        quantity = quantity_entry.get()
        contact_info = contact_info_entry.get()

        if donor_name and food_type and quantity.isdigit():
            add_entry(donor_name, food_type, quantity, contact_info)
        else:
            messagebox.showerror("Input Error", "Please enter valid details")

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
