import speech_recognition as sr
import pyttsx3
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Define fitness tasks for each day of the week
fitness_schedule = {
    "monday": ["Chest Press", "Push-ups", "Incline Bench Press"],
    "tuesday": ["Leg Press", "Squats", "Lunges"],
    "wednesday": ["Lat Pull", "Deadlifts", "Pull-ups"],
    "thursday": ["Bicep Curls", "Tricep Dips", "Hammer Curls"],
    "friday": ["Shoulder Press", "Front Raise", "Lateral Raise"],
    "saturday": ["Cardio", "Cycling", "Jump Rope"],
    "sunday": ["Rest day, focus on stretching and recovery!"]
}

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for user's question
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your fitness question...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there's an issue with the service.")
            return ""

# Function to provide fitness task based on the current day
def provide_fitness_task():
    command = listen_command()

    if "what's my fitness day today" in command:
        # Get the current day of the week
        current_day = datetime.datetime.now().strftime("%A").lower()

        # Retrieve exercises based on the current day
        if current_day in fitness_schedule:
            exercises = ", ".join(fitness_schedule[current_day])
            response = f"Today is {current_day.capitalize()}. Your exercises for today are: {exercises}."
            print(response)
            speak(response)
        else:
            speak("I don't have a fitness plan for today.")
    else:
        speak("Ask me about your fitness tasks!")

# Run the fitness task bot
provide_fitness_task()
