import pygame
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import io
import os

# Initialize Pygame for audio playback
pygame.mixer.init()

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window until splash screen finishes

# Global Variables
playlist = []
current_song_index = 0
volume = 0.5
song_length = 0
is_dragging = False

# Splash Screen Function
def splash_screen():
    splash = tk.Toplevel()
    splash.title("Welcome to PythonTunes")
    splash.geometry("600x400")
    splash.overrideredirect(True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 400) // 2
    splash.geometry(f"+{x}+{y}")

    try:
        logo_img = Image.open("music.jpg").resize((300, 300))
    except FileNotFoundError:
        # If the logo is missing, generate a placeholder image
        logo_img = Image.new("RGB", (300, 300), color="black")
    logo_tk = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(splash, image=logo_tk)
    logo_label.image = logo_tk
    logo_label.pack(pady=10)

    tk.Label(splash, text="Loading...", font=("Arial", 14)).pack(pady=20)
    root.after(2500, lambda: [splash.destroy(), root.deiconify()])

# Load Music Folder
def load_music_folder():
    global playlist
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.endswith(".mp3")]
        play_song()

# Play Song and Display Album Art
def play_song():
    global current_song_index, song_length
    if current_song_index < len(playlist):
        song_path = playlist[current_song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        song_length = MP3(song_path).info.length  # Get song length
        song_label.config(text=os.path.basename(song_path))
        timeline_slider.config(to=song_length)

        # Extract and display album art
        album_art = extract_album_art(song_path)
        if album_art:
            show_album_art(album_art)
        else:
            show_default_logo()

        update_timeline()

# Extract Album Art from MP3 Metadata
def extract_album_art(song_path):
    try:
        audio = ID3(song_path)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):  # Check if the tag is an album art tag
                return Image.open(io.BytesIO(tag.data))
    except Exception as e:
        print(f"Error extracting album art: {e}")
    return None

# Display the Album Art
def show_album_art(image):
    resized_image = image.resize((300, 300))
    album_art_img = ImageTk.PhotoImage(resized_image)
    album_label.config(image=album_art_img)
    album_label.image = album_art_img

# Display Default Logo if No Album Art Found
def show_default_logo():
    try:
        default_logo = Image.open("music_logo.png").resize((300, 300))
    except FileNotFoundError:
        # Generate a placeholder if the default logo is missing
        default_logo = Image.new("RGB", (300, 300), color="gray")
    default_img = ImageTk.PhotoImage(default_logo)
    album_label.config(image=default_img)
    album_label.image = default_img

# Update Timeline Position
def update_timeline():
    if not is_dragging:
        current_time = pygame.mixer.music.get_pos() / 1000  # Get time in seconds
        timeline_slider.set(current_time)

    if pygame.mixer.music.get_busy():
        root.after(500, update_timeline)

# Set Song Position on User Drag
def set_position(val):
    pygame.mixer.music.play(start=float(val))

def on_drag_start(event):
    global is_dragging
    is_dragging = True

def on_drag_end(event):
    global is_dragging
    is_dragging = False
    set_position(timeline_slider.get())

# Control Functions
def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(playlist)
    play_song()

def prev_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(playlist)
    play_song()

def pause_song():
    pygame.mixer.music.pause()

def unpause_song():
    pygame.mixer.music.unpause()

def stop_song():
    pygame.mixer.music.stop()

def set_volume(val):
    global volume
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

# Main Window Widgets
album_label = tk.Label(root)  # Label to display album art or logo
album_label.pack(pady=10)

song_label = tk.Label(root, text="", font=("Arial", 14))
song_label.pack(pady=10)

# Timeline Slider
timeline_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=set_position)
timeline_slider.pack(fill=tk.X, padx=10, pady=5)
timeline_slider.bind("<Button-1>", on_drag_start)
timeline_slider.bind("<ButtonRelease-1>", on_drag_end)

# Control Buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

prev_button = tk.Button(control_frame, text="Previous", command=prev_song)
prev_button.grid(row=0, column=0, padx=5)

play_button = tk.Button(control_frame, text="Play", command=unpause_song)
play_button.grid(row=0, column=1, padx=5)

pause_button = tk.Button(control_frame, text="Pause", command=pause_song)
pause_button.grid(row=0, column=2, padx=5)

stop_button = tk.Button(control_frame, text="Stop", command=stop_song)
stop_button.grid(row=0, column=3, padx=5)

next_button = tk.Button(control_frame, text="Next", command=next_song)
next_button.grid(row=0, column=4, padx=5)

# Volume Slider
volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_slider.set(50)
volume_slider.pack(pady=10)

# Load Music Button
load_button = tk.Button(root, text="Load Music Folder", command=load_music_folder)
load_button.pack(pady=10)

# Run Splash Screen and Main Application
splash_screen()
root.mainloop()

