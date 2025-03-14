import sounddevice as sd
import numpy as np
from time import sleep 
def beep(frequency=1000, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate=sample_rate)
    sd.wait()


def error():
    beep(2500, 0.3)
    beep(2000, 0.5)
    beep(2500, 0.3)
    beep(2000, 0.5)
    beep(2500, 0.3)
    beep(2000, 0.5)
    beep(2500, 0.3)
    beep(2000, 0.5)

def done():
    pass
beep(1000, 0.3)



