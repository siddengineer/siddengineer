from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Custom header
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Code to PDF Converter', 0, 1, 'C')

    def footer(self):
        # Custom footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(code, output_file):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Courier', size=10)  # Use monospace font for code

    # Add code to PDF
    for line in code.splitlines():
        pdf.cell(0, 10, line, 0, 1)

    pdf.output(output_file)
    print(f"PDF saved as '{output_file}'")

if __name__ == "__main__":
    # Paste your code here as a multi-line string
    code_to_convert = """
 Code Breakdown

import numpy as np
from scipy.io.wavfile import write

Imports:

numpy: A fundamental package for numerical computations in Python. It provides support for arrays and mathematical functions.

write from scipy.io.wavfile: A function to save data as a WAV audio file.




---

def generate_sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)  # Time array
    wave = 0.5 * np.sin(2 * np.pi * freq * t)  # Generate sine wave
    return wave

Function generate_sine_wave:

Parameters:

freq: Frequency of the sine wave in Hertz (Hz).

duration: Duration of the wave in seconds.

sample_rate: Number of samples per second (default is 44,100 Hz, standard for audio).


Process:

np.linspace(0, duration, int(sample_rate * duration), False): Generates an array t containing time values from 0 to the specified duration.

wave = 0.5 * np.sin(2 * np.pi * freq * t): Creates the sine wave using the sine function, scaled to 0.5 (to avoid clipping).


Return Value: The generated sine wave array.




---

def save_wave(filename, wave, sample_rate=44100):
    write(filename, sample_rate, wave.astype(np.float32))  # Save as WAV file

Function save_wave:

Parameters:

filename: Name of the output WAV file.

wave: The waveform data to be saved.

sample_rate: Sample rate for the WAV file (default is 44,100 Hz).


Process:

write(filename, sample_rate, wave.astype(np.float32)): Uses the write function from SciPy to save the sine wave as a WAV file. The wave data is converted to a float32 format.





---

def create_melody():
    sample_rate = 44100  # Sample rate
    duration = 0.5       # Duration of each note (in seconds)
    
    # Frequencies for musical notes (C4, D4, E4, F4, G4, A4, B4)
    frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C4 to B4
    melody = np.array([])  # Initialize empty array for melody
    
    # Generate melody by concatenating sine waves for each frequency
    for freq in frequencies:
        wave = generate_sine_wave(freq, duration)
        melody = np.concatenate((melody, wave))  # Concatenate each note

    # Save the generated melody to a .wav file
    save_wave("simple_melody.wav", melody)
    print("Melody generated and saved as simple_melody.wav")

Function create_melody:

Purpose: To create a melody by generating sine waves for specific musical frequencies.

Process:

Initializes sample_rate and duration for each note.

Defines an array frequencies containing the frequencies for musical notes from C4 to B4.

Initializes an empty array melody to store the concatenated sine waves.

A loop iterates over each frequency:

Calls generate_sine_wave to create a sine wave for each frequency and appends it to the melody array using np.concatenate.


After generating the entire melody, it calls save_wave to save the melody as a WAV file named "simple_melody.wav".

Prints a confirmation message.





---

if _name_ == "_main_":
    create_melody()

Entry Point:

This conditional statement checks if the script is being run directly (not imported as a module).

If true, it calls the create_melody function to execute the melody generation.



Concepts Covered

1. Functions: Encapsulation of reusable code into functions (generate_sine_wave, save_wave, create_melody).


2. Array Manipulation: Use of NumPy for creating and manipulating arrays, particularly for time and waveform data.


3. Mathematics: Application of sine functions to create sound waves, using trigonometric principles.


4. File I/O: Saving audio data to a WAV file format using the SciPy library.


5. Audio Synthesis: Basics of sound wave generation and how to create melodies by combining different frequencies.
"""

    # Specify output PDF file name
    output_pdf_file = "code_output.pdf"
    create_pdf(code_to_convert, output_pdf_file)