import json
import subprocess
from threading import Thread
from queue import Queue
import time
import pyaudio
from vosk import Model, KaldiRecognizer

messages = Queue()          # Tracks when recording is desired - thread communication
recordings = Queue()        # Holds all recording files in 20 sec increments

# Microphone recording
CHANNELS = 1                # Speech recognition works best w/ 1 channel
FRAME_RATE = 16000
RECORD_SECONDS = 5
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

# Speech recognition
model = Model(model_name="vosk-model-en-us-0.22")   # Creating model, downloads it if not present
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)                                  # Confidence probabilities


def start_recording():
    messages.put(True, block=True)      # Ping for recording to initiate

    # Begin recording
    print("Starting...")
    record = Thread(target=record_microphone)
    record.start()

    # Begin transcription
    transcribe = Thread(target=speech_recognition)
    transcribe.start()

def stop_recording():
    messages.get()          # Ping for recording to stop
    print("Stopped.")


def record_microphone(chunk=1024):          # Reading 1024 frames at a time
    p = pyaudio.PyAudio()

    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=3,   # Arctic Steel Series 7 - Chat index
                    frames_per_buffer=chunk)
    frames = []

    while not messages.empty():     # Recording is ongoing
        data = stream.read(chunk)   # Read & store 'chunk' sized data from stream
        frames.append(data)

        # Once 20 secs of audio recorded
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []

    # Closing stream & PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()


def speech_recognition():
    while not messages.empty():     # Recording desired
        frames = recordings.get()   # Pulling saved frames

        rec.AcceptWaveform(b''.join(frames)) # Joining frames into binary string
        result = rec.Result()
        text = json.loads(result)["text"]

        # Running shell command "repunc", applying punctuation to text
        # Can be optimized by integrating recasepunc.py
        print(text)


if __name__ == '__main__':
    start_recording()

    print("Press ENTER to stop recording.")
    input()

    stop_recording()