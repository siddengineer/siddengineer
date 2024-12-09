"""
user_score = 12 #define user_score or any integer value

if user_score > 10: #check if the user_score is greater than zero
   print("you have got highest score") """



"""
user_choice = 'B'
if user_choice == 'A':
   print("You have chosen A")
else:
   print("you have not chosen A")
"""
"""
user_chose = 'C'
if user_chose == 'A':
    print("you have chosen A")
elif user_chose == 'B':
    print("You have chosen B")    
else:
    print("You neither chose A and B")"""

"""
def print_greeting(name):
    print("hello "+ name)
print_greeting("John")  """ 

"""
def multiply(num1,num2):
    return num1*num2
result = multiply(5,3)
print(result) """

import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meanings = data[0].get('meanings', [])
        result = []

        for meaning in meanings:
            part_of_speech = meaning['partOfSpeech']
            definitions = [d['definition'] for d in meaning['definitions']]
            result.append(f"{part_of_speech}: {', '.join(definitions)}")
        
        return "\n\n".join(result)
    else:
        return "Meaning not found. Please try another word."

def show_meaning():
    word = entry.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word!")
        return
    
    meaning = get_meaning(word)
    text_area.config(state=tk.NORMAL)  # Enable text area to insert content
    text_area.delete(1.0, tk.END)      # Clear previous content
    text_area.insert(tk.END, meaning)  # Insert new meaning
    text_area.config(state=tk.DISABLED)  # Disable editing after inserting

# Create the main window
root = tk.Tk()
root.title("Dictionary App")
root.geometry("500x400")
root.resizable(False, False)

# UI Elements
title_label = tk.Label(root, text="Word Meaning Finder", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

entry_label = tk.Label(frame, text="Enter Word:", font=("Arial", 14))
entry_label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, font=("Arial", 14), width=20)
entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(frame, text="Search", font=("Arial", 12), command=show_meaning)
search_button.grid(row=0, column=2, padx=5)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), height=10, width=45)
text_area.pack(pady=10)
text_area.config(state=tk.DISABLED)  # Disable editing initially

# Run the application
root.mainloop()

