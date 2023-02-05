from threading import Thread
import pyaudio
import Transcription as tr

# Microphone recording
CHANNELS = 1  # Speech recognition works best w/ 1 channel
FRAME_RATE = 16000
RECORD_SECONDS = 5
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

class Microphone:
    def __init__(self, manager):
        self.manager = manager

    def start_recording(self):
        self.manager.appState.put(True)  # Ping for recording to initiate

        # Begin recording
        print("Starting...")

        # stopwatch = Thread(target=timer)  # Timer
        # stopwatch.start()

        record = Thread(target=self.record_microphone)  # Record microphone
        record.start()

        transcribe = Thread(target=tr.speech_recognition, args=(self.manager,))  # Record microphone
        transcribe.start()

    def stop_recording(self):
        self.manager.appState.get()  # Ping for recording to stop
        print("Stopped.")

    def record_microphone(self, chunk=1024):  # Reading 1024 frames at a time
        p = pyaudio.PyAudio()

        stream = p.open(format=AUDIO_FORMAT,
                        channels=CHANNELS,
                        rate=FRAME_RATE,
                        input=True,
                        input_device_index=3,  # Input device, use 'Devices.py' to utilize it
                        frames_per_buffer=chunk)
        frames = []

        while not self.manager.appState.empty():  # Recording is ongoing
            data = stream.read(chunk)  # Read & store 'chunk' sized data from stream
            frames.append(data)

            # Sending frames for transcription
            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk: # RECORD_SECONDS length
                self.manager.recordings.put(b''.join(frames))
                frames = []

        # Closing stream & PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()