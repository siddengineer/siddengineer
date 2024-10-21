import speech_recognition as sr
import pyttsx3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Global variables for tracking text
content = []
current_page = 1

# Function to recognize speech and convert to text
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return ""

# Function to speak back to the user
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to add text to the PDF
def add_to_pdf(pdf, text, is_heading=False):
    if is_heading:
        pdf.setFont("Helvetica-Bold", 14)
    else:
        pdf.setFont("Helvetica", 12)
    
    pdf.drawString(100, 750, text)
    pdf.showPage()

# Function to generate PDF from the content list
def generate_pdf(content):
    pdf = canvas.Canvas(f"verbal_notes_page_{current_page}.pdf", pagesize=A4)
    pdf.setTitle(f"Notes - Page {current_page}")

    for item in content:
        if item["type"] == "heading":
            add_to_pdf(pdf, item["text"], is_heading=True)
        else:
            add_to_pdf(pdf, item["text"], is_heading=False)

    pdf.save()
    print(f"PDF saved as verbal_notes_page_{current_page}.pdf")

# Main function to take voice commands
def verbal_notes_maker():
    global current_page
    content = []

    while True:
        command = recognize_speech()

        if "heading" in command:
            speak("Adding a heading")
            print("Heading detected")
            content.append({"type": "heading", "text": command.replace("heading", "").strip()})

        elif "next line" in command:
            speak("Adding to the next line")
            print("Next line detected")
            content.append({"type": "text", "text": command.replace("next line", "").strip()})

        elif "next page" in command:
            speak("Moving to the next page")
            generate_pdf(content)  # Save the current page's content
            current_page += 1
            content = []  # Start fresh for the new page

        elif "stop" in command:
            speak("Saving and stopping")
            generate_pdf(content)  # Save the last page
            break

        else:
            content.append({"type": "text", "text": command})
            print(f"Text added: {command}")

if __name__ == "__main__":
    
    verbal_notes_maker()