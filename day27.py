import tkinter as tk
import random
import datetime
import pyttsx3
import speech_recognition as sr
import nltk
from nltk.corpus import wordnet

# Ensure you have downloaded WordNet
nltk.download('wordnet')

# Initialize the speech engine
engine = pyttsx3.init()

# Grammar questions list
questions_list = [
    {"question": "Choose the correct article: ____ apple.", "choices": ["A", "An", "The"], "correct": "An"},
    {"question": "What is the past tense of 'eat'?", "choices": ["eated", "ate", "eat"], "correct": "ate"},
    {"question": "Which sentence is correct?", "choices": ["He go to school.", "He goes to school.", "He going to school."], "correct": "He goes to school."},
    {"question": "Choose the correct form: She ____ (go) to the market every day.", "choices": ["goes", "going", "gone"], "correct": "goes"},
    {"question": "Select the correct word: I have ____ apples.", "choices": ["many", "much", "more"], "correct": "many"}
]

# Get daily questions based on the date
def get_daily_questions():
    today = datetime.datetime.now().day
    random.seed(today)
    return random.sample(questions_list, 3)

# Load today's questions
daily_questions = get_daily_questions()

# Initialize the main application window
window = tk.Tk()
window.title("Grammar Quiz & Language Learning App")

# Function to pronounce a word
def say_word(word):
    engine.say(word)
    engine.runAndWait()

# Function to check the spelling
def check_spelling():
    word = "example"  # You can change this to any word you want
    say_word(word)  # Spell the word
    user_input = entry_spelling.get().lower()
    if user_input == word:
        label_result.config(text="Correct!")
    else:
        label_result.config(text=f"Wrong! The correct spelling is: {word}")

# Function to start speaking test
def speaking_test():
    recognizer = sr.Recognizer()
    sentence = "Python is an interesting language."
    label_sentence.config(text="Speak this sentence: " + sentence)
    
    with sr.Microphone() as source:
        label_result.config(text="Listening...")
        audio = recognizer.listen(source)
    
    try:
        spoken_text = recognizer.recognize_google(audio)
        label_result.config(text="You said: " + spoken_text)
        if spoken_text.lower() == sentence.lower():
            label_result.config(text="Correct!")
        else:
            label_result.config(text="Incorrect pronunciation.")
    except sr.UnknownValueError:
        label_result.config(text="Could not understand speech.")
    except sr.RequestError:
        label_result.config(text="Error with speech recognition service.")

# Function to run jumbled word test
def jumbled_word_test():
    word = "python"  # You can change this to any word you want
    jumbled_word = ''.join(random.sample(word, len(word)))
    label_jumbled.config(text="Jumbled word: " + jumbled_word)
    user_input = entry_jumbled.get().lower()
    if user_input == word:
        label_result.config(text="Correct!")
    else:
        label_result.config(text=f"Wrong! The correct word is: {word}")

# Function to search word in dictionary using NLTK's WordNet
def search_word():
    word = entry_word.get()
    synonyms = wordnet.synsets(word)
    
    if synonyms:
        definitions = "\n".join([f"Definition: {syn.definition()}\nExample: {syn.examples()}" for syn in synonyms])
        label_result.config(text=f"Meaning:\n{definitions}")
    else:
        label_result.config(text="Word not found!")

# Create UI components for the grammar quiz
label_question = tk.Label(window, text="Daily Grammar Quiz", font=("Arial", 16))
label_question.pack(pady=10)

for question in daily_questions:
    label_q = tk.Label(window, text=question['question'], font=("Arial", 12))
    label_q.pack(pady=5)

# Spelling test section
label_spelling = tk.Label(window, text="Spelling Test: Listen and Write", font=("Arial", 16))
label_spelling.pack(pady=10)
entry_spelling = tk.Entry(window)
entry_spelling.pack(pady=5)
button_spelling = tk.Button(window, text="Submit Spelling", command=check_spelling)
button_spelling.pack(pady=5)

# Speaking test section
label_sentence = tk.Label(window, text="Speaking Test", font=("Arial", 16))
label_sentence.pack(pady=10)
button_speaking = tk.Button(window, text="Start Speaking Test", command=speaking_test)
button_speaking.pack(pady=5)

# Jumbled word test section
label_jumbled = tk.Label(window, text="Jumbled Word Test", font=("Arial", 16))
label_jumbled.pack(pady=10)
entry_jumbled = tk.Entry(window)
entry_jumbled.pack(pady=5)
button_jumbled = tk.Button(window, text="Submit Jumbled Word", command=jumbled_word_test)
button_jumbled.pack(pady=5)

# Dictionary search section
label_dictionary = tk.Label(window, text="Dictionary Search", font=("Arial", 16))
label_dictionary.pack(pady=10)
entry_word = tk.Entry(window)
entry_word.pack(pady=5)
button_search = tk.Button(window, text="Search Word", command=search_word)
button_search.pack(pady=5)

# Result output
label_result = tk.Label(window, text="", font=("Arial", 12))
label_result.pack(pady=20)

# Run the application
window.mainloop()