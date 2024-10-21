import tkinter as tk
import pyautogui
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

class SimpleScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Screen Recorder and Screenshot App")
        
        # UI Buttons
        self.record_btn = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.record_btn.pack(pady=10)

        self.stop_btn = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_btn.pack(pady=10)

        self.screenshot_btn = tk.Button(self.root, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_btn.pack(pady=10)

        self.is_recording = False
        self.video_writer = None

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            screen_size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            filename = f"screen_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
            self.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)
            
            self.record_screen()
        else:
            print("Recording already in progress...")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            print("Recording stopped.")
        else:
            print("No recording is in progress...")

    def record_screen(self):
        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)
            self.root.update()  # Keep Tkinter responsive during recording

        print("Recording saved.")

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot.save(f"screenshot_{timestamp}.png")
        print(f"Screenshot saved as screenshot_{timestamp}.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleScreenRecorderApp(root)
    root.mainloop()
