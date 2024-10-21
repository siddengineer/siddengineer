import numpy as np
from scipy.io.wavfile import write


def generate_sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)  
    wave = 0.5 * np.sin(2 * np.pi * freq * t)  
    return wave


def save_wave(filename, wave, sample_rate=44100):
    write(filename, sample_rate, wave.astype(np.float32)) 

def create_different_melody():
    sample_rate = 44100  
    duration = 0.5       
    
    frequencies = [329.63, 392.00, 440.00, 523.25, 587.33]  
    melody = np.array([])  
    
    for freq in frequencies:
        wave = generate_sine_wave(freq, duration)
        melody = np.concatenate((melody, wave))  

    
    pause = np.zeros(int(sample_rate * 0.2))  
    melody = np.concatenate((melody, pause))  

    for freq in reversed(frequencies):  
        wave = generate_sine_wave(freq, duration)
        melody = np.concatenate((melody, wave))  

    save_wave("different_tune.wav", melody)
    print("Different melody generated and saved as different_tune.wav")

if __name__ == "__main__":
    create_different_melody()