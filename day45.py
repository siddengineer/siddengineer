from PIL import Image, ImageTk
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables for image paths and selected chair indices
CHAIR_IMAGES_PATH = ""  # Placeholder for chair images folder
OTHER_IMAGES_PATH = ""  # Placeholder for other images folder
selected_chair_indices = []
image_buttons = []  # To keep track of image buttons for toggling selection

def load_images(image_dir):
    """Load all images from the provided directory."""
    images = []
    try:
        for img_file in os.listdir(image_dir):
            if img_file.lower().endswith(('png', 'jpg', 'jpeg')):  # Check for valid image formats
                img_path = os.path.join(image_dir, img_file)
                images.append(Image.open(img_path))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load images from {image_dir}: {e}")
    return images

def generate_captcha_grid(chairs_count=4, total_images=9):
    """Generate a CAPTCHA grid with a mix of chair and other images."""
    global selected_chair_indices, image_buttons
    selected_chair_indices = []
    image_buttons = []  # Reset image buttons

    if not CHAIR_IMAGES_PATH or not OTHER_IMAGES_PATH:
        messagebox.showwarning("Warning", "Please select both chair and other images folders before generating CAPTCHA.")
        return

    # Load chair images
    chair_images = load_images(CHAIR_IMAGES_PATH)
    if len(chair_images) < chairs_count:
        messagebox.showwarning("Warning", f"Not enough chair images. Available: {len(chair_images)}, Required: {chairs_count}")
        return

    # Load other random images to fill the grid
    other_images = load_images(OTHER_IMAGES_PATH)
    other_count = total_images - chairs_count
    if len(other_images) < other_count:
        messagebox.showwarning("Warning", f"Not enough other images. Available: {len(other_images)}, Required: {other_count}")
        return

    # Randomly select chair and other images
    selected_chair_images = random.sample(chair_images, chairs_count)
    selected_other_images = random.sample(other_images, other_count)

    # Combine and shuffle images
    grid_images = selected_chair_images + selected_other_images
    random.shuffle(grid_images)  # Shuffle the images

    # Create a new window for the CAPTCHA grid
    captcha_window = tk.Toplevel(root)
    captcha_window.title("CAPTCHA Verification")

    # Create buttons for each image
    img_size = 200  # Each image is 200x200
    for i, img in enumerate(grid_images):
        img_resized = img.resize((img_size, img_size))
        img_photo = ImageTk.PhotoImage(img_resized)

        button = tk.Button(captcha_window, image=img_photo, command=lambda idx=i: toggle_selection(idx))
        button.image = img_photo  # Keep a reference
        button.grid(row=i // 3, column=i % 3)
        image_buttons.append(button)  # Store button reference

    # Verification button
    verify_button = tk.Button(captcha_window, text="Verify Selection", command=lambda: verify_selection(selected_chair_images, grid_images))
    verify_button.grid(row=3, columnspan=3)

def toggle_selection(index):
    """Toggle selection of chair images and update button appearance."""
    global selected_chair_indices
    if index in selected_chair_indices:
        selected_chair_indices.remove(index)
        image_buttons[index].config(relief=tk.RAISED)  # Remove highlight
    else:
        selected_chair_indices.append(index)
        image_buttons[index].config(relief=tk.SUNKEN)  # Highlight the selected button

def verify_selection(selected_chair_images, grid_images):
    """Verify the selected images."""
    correct_indices = [grid_images.index(img) for img in selected_chair_images]
    if sorted(selected_chair_indices) == sorted(correct_indices):
        messagebox.showinfo("Success", "CAPTCHA verified! You selected all the chairs correctly.")
    else:
        messagebox.showwarning("Error", "CAPTCHA verification failed. Please try again.")

def set_chair_images_folder():
    global CHAIR_IMAGES_PATH
    CHAIR_IMAGES_PATH = filedialog.askdirectory(title="Select Chair Images Folder")
    if CHAIR_IMAGES_PATH:
        print(f"Chair images folder set to: {CHAIR_IMAGES_PATH}")

def set_other_images_folder():
    global OTHER_IMAGES_PATH
    OTHER_IMAGES_PATH = filedialog.askdirectory(title="Select Other Images Folder")
    if OTHER_IMAGES_PATH:
        print(f"Other images folder set to: {OTHER_IMAGES_PATH}")

# Setup Tkinter window
root = tk.Tk()
root.title("Image Folder Selector")
root.geometry("300x200")

# Buttons for setting image folders and generating CAPTCHA
chair_folder_button = tk.Button(root, text="Select Chair Images Folder", command=set_chair_images_folder)
chair_folder_button.pack(pady=10)

other_folder_button = tk.Button(root, text="Select Other Images Folder", command=set_other_images_folder)
other_folder_button.pack(pady=10)

generate_button = tk.Button(root, text="Generate CAPTCHA", command=lambda: generate_captcha_grid(chairs_count=4))
generate_button.pack(pady=10)

# Keep the window running
root.mainloop()