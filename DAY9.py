import tkinter as tk
from tkinter import messagebox
import random

# Create the main app window
root = tk.Tk()
root.title("Feelings Reflection App")
root.geometry("500x600")

# Writing prompts to help guide users
writing_prompts = [
    "How are you feeling right now?",
    "What is one thing that has been on your mind?",
    "What do you want to let go of today?",
    "What is one challenge you're facing?",
    "What's something good that happened today?"
]

# Gratitude list to store positive thoughts
gratitude_list = []

# Function to start breathing timer (5 seconds as an example)
def start_breathing_exercise():
    def countdown(i):
        if i > 0:
            breathing_label.config(text=f"Breathe deeply... Time left: {i} seconds")
            root.after(1000, countdown, i-1)  # Call countdown function every 1 second
        else:
            breathing_label.config(text="")
            show_congratulations()

    countdown(5)  # Start countdown from 5 seconds

# Function to show congratulations message
def show_congratulations():
    messagebox.showinfo("Congratulations!", "You’ve let go of your feelings and completed your breathing exercise!")

# Function to handle when the user "throws" the plane
def throw_plane():
    feelings = text_entry.get("1.0", "end").strip()
    if feelings:
        messagebox.showinfo("Reflection", "Take a deep breath, you've written down your feelings.")
        text_entry.delete("1.0", "end")

        # Show affirmation after "throwing the plane"
        affirmations = [
            "You are strong!",
            "You can handle whatever comes your way.",
            "You are enough, just as you are.",
            "Breathe in peace, breathe out stress."
        ]
        affirmation = random.choice(affirmations)
        messagebox.showinfo("Affirmation", affirmation)

        # Start breathing exercise after throwing the plane
        start_breathing_exercise()
    else:
        messagebox.showwarning("No Feelings", "Please write down your feelings before throwing the plane.")

# Function to add to gratitude journal
def add_gratitude():
    gratitude = gratitude_entry.get().strip()
    if gratitude:
        gratitude_list.append(gratitude)
        messagebox.showinfo("Gratitude Added", "Your gratitude has been added!")
        gratitude_entry.delete(0, 'end')
    else:
        messagebox.showwarning("No Gratitude", "Please write something you're grateful for.")

# App Title
title_label = tk.Label(root, text="Write down your feelings", font=("Helvetica", 14))
title_label.pack(pady=10)

# Random writing prompt
prompt_label = tk.Label(root, text=random.choice(writing_prompts), font=("Helvetica", 10))
prompt_label.pack(pady=5)

# Text area for users to write their feelings
text_entry = tk.Text(root, height=5, width=40)
text_entry.pack(pady=10)

# Button to "throw" the paper plane
throw_button = tk.Button(root, text="Throw the Plane", command=throw_plane)
throw_button.pack(pady=20)

# Gratitude Journal section
gratitude_label = tk.Label(root, text="What are you grateful for today?", font=("Helvetica", 12))
gratitude_label.pack(pady=10)
gratitude_entry = tk.Entry(root, width=30)
gratitude_entry.pack(pady=5)
gratitude_button = tk.Button(root, text="Add to Gratitude Journal", command=add_gratitude)
gratitude_button.pack(pady=10)

# Breathing instruction label
breathing_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")
breathing_label.pack(pady=10)

# Run the app
root.mainloop()