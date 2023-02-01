import json
from threading import Thread
from queue import Queue
import pyaudio
import time
from fastpunct import FastPunct
from vosk import Model, KaldiRecognizer

messages = Queue()  # Tracks when recording is desired - thread communication
recordings = []

# Microphone recording
CHANNELS = 1  # Speech recognition works best w/ 1 channel
FRAME_RATE = 16000
RECORD_SECONDS = 5
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

# Speech recognition
# -> Loads model's data, downloads model into cache if not present
model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
fastpunct = FastPunct()

rec.SetWords(True)  # Confidence probabilities


def timer():
    print("Starting timer!")
    secs = 0

    while True:
        time.sleep(1)
        secs += 1

        if messages.empty():  # More accuracy within thread for timer
            break
        else:
            print(f"{secs} seconds...")


def start_recording():
    messages.put(True)  # Ping for recording to initiate

    # Begin recording
    print("Starting...")

    # stopwatch = Thread(target=timer)  # Timer
    # stopwatch.start()

    record = Thread(target=record_microphone)  # Record microphone
    record.start()


def stop_recording():
    messages.get()  # Ping for recording to stop
    print("Stopped.")


def record_microphone(chunk=1024):  # Reading 1024 frames at a time
    p = pyaudio.PyAudio()

    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=6,  # Input device, use 'Devices.py' to utilize it
                    frames_per_buffer=chunk)

    while not messages.empty():  # Recording is ongoing
        data = stream.read(chunk)  # Read & store 'chunk' sized data from stream
        recordings.append(data)

    # Closing stream & PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()


def speech_recognition(chunks):
    rec.AcceptWaveform(b''.join(chunks))  # Joining frames into binary string

    result = rec.Result()  # Result, VOSK returns JSON object
    text = json.loads(result)["text"]

    print(f"VOSK:\n {text}")
    correct_punctuation(text)


def correct_punctuation(text):
    data = fastpunct.punct(text)
    result = ""

    for fragment in data:
        result += fragment

    print(f"VOSK + FastPunct:\n {result}")


if __name__ == '__main__':
    start_recording()

    input("Press ENTER to stop recording.")
    stop_recording()

    speech_recognition(recordings)
