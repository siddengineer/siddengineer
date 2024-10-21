import pygame
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT
import io
import os

# Initialize Pygame for audio playback
pygame.mixer.init()

# Initialize the main Tkinter window
root = tk.Tk()
root.title("PythonTunes - Music Player")
root.geometry("800x600")
root.withdraw()  # Hide main window initially

# Function to load the logo image for the splash screen
def load_splash_logo():
    try:
        img = Image.open("music.jpg").resize((300, 300))  # Adjust size if needed
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print("Logo image not found! Using placeholder.")
        img = Image.new("RGB", (300, 300), (255, 255, 255))
        return ImageTk.PhotoImage(img)

# Function to create the splash screen
def show_splash():
    splash = tk.Toplevel()
    splash.geometry("400x400")
    splash.title("PythonTunes")
    splash.overrideredirect(True)  # Remove window borders for a clean look

    logo_img = load_splash_logo()
    logo_label = tk.Label(splash, image=logo_img)
    logo_label.image = logo_img  # Keep reference to avoid garbage collection
    logo_label.pack(expand=True)

    # Automatically close splash after 3 seconds and show the main app
    splash.after(3000, lambda: [splash.destroy(), root.deiconify()])

# Frame to display album art, control buttons, etc.
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Label for album art (with default logo image)
image_label = tk.Label(left_frame)
image_label.pack(pady=5)

song_label = tk.Label(root, text="", font=("Arial", 14), pady=10)
song_label.pack()

lyrics_text = tk.Text(root, wrap=tk.WORD, height=20, width=40, font=("Arial", 12))
lyrics_text.pack(side=tk.RIGHT, padx=10, pady=10)

playlist = []  # List of songs
current_song_index = 0
volume = 0.5
song_length = 0

# Load music folder and play the first song
def load_music_folder():
    global playlist
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist = [
            os.path.join(folder_selected, file)
            for file in os.listdir(folder_selected)
            if file.endswith(".mp3")
        ]
        play_song()

# Extract album art from MP3 metadata
def extract_album_art(song_path):
    try:
        audio = ID3(song_path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                img_data = io.BytesIO(tag.data)
                img = Image.open(img_data).resize((150, 150))
                return ImageTk.PhotoImage(img)
        print("No album art found.")
    except Exception as e:
        print(f"Error extracting album art: {e}")
    return None

# Display album art or default logo
def show_album_art_or_default(song_path):
    album_art = extract_album_art(song_path)
    if album_art:
        image_label.config(image=album_art)
        image_label.image = album_art
    else:
        image_label.config(image=load_splash_logo())

# Extract lyrics from MP3 metadata
def extract_lyrics(song_path):
    try:
        audio = MP3(song_path, ID3=ID3)
        lyrics = ""
        for tag in audio.tags.values():
            if isinstance(tag, USLT):
                lyrics = tag.text
                break

        lyrics_text.delete(1.0, tk.END)
        lyrics_text.insert(tk.END, lyrics if lyrics else "Lyrics not found.")
    except Exception as e:
        print(f"Error extracting lyrics: {e}")
        lyrics_text.delete(1.0, tk.END)
        lyrics_text.insert(tk.END, "Error loading lyrics.")

# Play the selected song
def play_song():
    global current_song_index, song_length
    if current_song_index < len(playlist):
        song_path = playlist[current_song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        song_length = MP3(song_path).info.length
        song_label.config(text=os.path.basename(song_path))
        timeline_slider.config(to=song_length)

        show_album_art_or_default(song_path)
        extract_lyrics(song_path)

        update_timeline()

# Update timeline slider in real-time
def update_timeline():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        timeline_slider.set(current_time)
        root.after(1000, update_timeline)

# Control song position with the timeline slider
def set_song_position(val):
    pygame.mixer.music.play(loops=0, start=float(val))

# Control functions
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

# Create control buttons
control_frame = tk.Frame(left_frame)
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

# Volume control slider
volume_slider = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_slider.set(50)
volume_slider.pack(pady=10)

# Timeline slider for song progress
timeline_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=set_song_position)
timeline_slider.pack(fill=tk.X, padx=10, pady=5)

# Load music folder button
load_button = tk.Button(root, text="Load Music Folder", command=load_music_folder)
load_button.pack(pady=10)

# Show the splash screen and start the main loop
show_splash()
root.mainloop()
