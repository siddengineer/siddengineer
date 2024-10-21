import tkinter as tk
from tkinter import scrolledtext
from gtts import gTTS
import os
import playsound
import time
import threading


class RatanTataChatbot:
    def __init__(self, root):  # Correct __init__ method with double underscores
        self.root = root
        self.root.title("Chat with Ratan Tata")
        self.root.geometry("400x600")
        self.root.configure(bg="#ecf0f1")

        # Custom fonts and styles
        self.title_font = ("Times New Roman", 18, "bold")
        self.chat_font = ("Helvetica", 12)
        self.user_font = ("Helvetica", 12, "bold")

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#ecf0f1", font=self.chat_font, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input area
        self.input_area = tk.Entry(self.root, font=self.user_font, bg="#3498db", fg="white")
        self.input_area.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.input_area.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, bg="#2980b9", fg="white", font=self.user_font)
        self.send_button.pack(pady=(0, 10))

        # Message list
        self.messages = []

        # Welcome message
        self.display_message("Ratan Tata", "Hello! I'm Ratan Tata. Ask me anything about my journey, mindset, or experiences!")
        self.speak("Hello! I'm Ratan Tata. Ask me anything about my journey, mindset, or experiences!")

    def send_message(self, event=None):
        user_message = self.input_area.get()
        if user_message:
            self.display_message("User", user_message)
            self.input_area.delete(0, tk.END)

            # Simulate bot typing
            threading.Thread(target=self.simulate_typing).start()

            # Generate a bot response
            bot_response = self.generate_response(user_message)
            self.messages.append((user_message, bot_response))

            # Speak bot response
            threading.Thread(target=self.speak, args=(bot_response,)).start()

    def simulate_typing(self):
        self.display_message("Ratan Tata", "...")
        time.sleep(1)
        self.chat_area.delete("end-1c", "end")  # Remove typing indicator

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')

        if sender == "User":
            self.chat_area.insert(tk.END, f"You: {message}\n", "user")
        else:
            self.chat_area.insert(tk.END, f"Ratan Tata: {message}\n", "bot")

        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

        # Configure chat bubbles without padding
        self.chat_area.tag_configure("user", background="#3498db", foreground="white", font=self.chat_font, relief='flat')
        self.chat_area.tag_configure("bot", background="#ecf0f1", foreground="#2c3e50", font=self.chat_font, relief='flat')

    def generate_response(self, message):
        # Simple predefined responses
        responses = {
            "journey": "My journey has been filled with challenges and opportunities. I believe in staying grounded and focused.",
            "mindset": "I maintain a positive mindset and embrace challenges as opportunities for growth.",
            "life": "Life is all about learning and adapting. One must be open to new experiences.",
            "failure": "Failure is not the opposite of success; it's part of success. Learn from it and move on.",
            "dream": "Dream big, and don't let anyone tell you that you can't achieve your goals."
        }
        
        # Return a response based on keywords in the user's message
        for keyword in responses:
            if keyword in message.lower():
                return responses[keyword]
        
        return "That's an interesting question! Let me think about it."

    def speak(self, message):
        try:
            # Create and play text-to-speech audio
            tts = gTTS(text=message, lang='en')
            audio_file = "response.mp3"
            tts.save(audio_file)
            playsound.playsound(audio_file)
            os.remove(audio_file)  # Clean up audio file
        except Exception as e:
            print(f"Error in speaking: {e}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        chatbot = RatanTataChatbot(root)
        root.mainloop()
    except Exception as e:
        print(f"Error occurred: {e}")
