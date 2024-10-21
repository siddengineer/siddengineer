# daily_blog_gui.py
import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Function to set up the SQLite database and create the posts table
def setup_database():
    connection = sqlite3.connect('blog.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

# Function to create a new blog post
def create_post(title, content):
    connection = sqlite3.connect('blog.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Post created successfully!")

# Function to display all blog posts
def display_posts():
    connection = sqlite3.connect('blog.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY date DESC')
    posts = cursor.fetchall()
    connection.close()
    
    # Clear the text area before displaying posts
    text_area.delete(1.0, tk.END)
    
    if not posts:
        text_area.insert(tk.END, "No posts available.")
    else:
        for post in posts:
            text_area.insert(tk.END, f"ID: {post[0]}, Title: {post[1]}, Date: {post[3]}\n")
            text_area.insert(tk.END, f"Content: {post[2]}\n\n")

# Function to handle the creation of a new post
def submit_post():
    title = title_entry.get()
    content = content_entry.get("1.0", tk.END)
    if title and content.strip():
        create_post(title, content)
        title_entry.delete(0, tk.END)
        content_entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter both title and content.")

# Create the main application window
app = tk.Tk()
app.title("Daily Blog Channel")

# Set up the database
setup_database()

# Create input frame
input_frame = tk.Frame(app)
input_frame.pack(pady=10)

# Title label and entry
title_label = tk.Label(input_frame, text="Title:")
title_label.grid(row=0, column=0)
title_entry = tk.Entry(input_frame, width=40)
title_entry.grid(row=0, column=1)

# Content label and entry
content_label = tk.Label(input_frame, text="Content:")
content_label.grid(row=1, column=0)
content_entry = scrolledtext.ScrolledText(input_frame, width=40, height=10)
content_entry.grid(row=1, column=1)

# Submit button
submit_button = tk.Button(app, text="Create Post", command=submit_post)
submit_button.pack(pady=10)

# Display button
display_button = tk.Button(app, text="Display Posts", command=display_posts)
display_button.pack(pady=10)

# Text area for displaying posts
text_area = scrolledtext.ScrolledText(app, width=60, height=15)
text_area.pack(pady=10)

# Run the application
app.mainloop()