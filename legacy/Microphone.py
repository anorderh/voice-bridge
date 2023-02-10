import time
from threading import Thread
from multiprocessing import Process
import pyaudio
import speech_recognition as sr
import Transcription as tr
import io

# Microphone recording
CHANNELS = 1  # Speech recognition works best w/ 1 channel
FRAME_RATE = 16000
RECORD_SECONDS = 1
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2


class Microphone:
    def __init__(self, manager):
        self.manager = manager

    def start_recording(self, lang):
        self.manager.recording = True
        # Begin recording
        print("Starting...")

        record = Thread(target=self.record_microphone)
        record.start()  # Start recording

        transcribe = Thread(target=tr.realtime_transcribe, args=(self.manager, lang))
        transcribe.start()  # Starting transcribing

    def stop_recording(self):
        self.manager.recording = False  # "OFF"
        while self.manager.processing:      # Waiting for transcription to complete
            pass
        print("Stopped.")

    def record_microphone(self):
        r = sr.Recognizer()
        r.non_speaking_duration = 0.1
        r.pause_threshold = 0.3
        r.energy_threshold = 300

        with sr.Microphone(sample_rate=16000) as source:
            while self.manager.recording:  # Recording is ongoing
                self.manager.processing = True
                # Recording bytes until pause detected
                audio = r.listen(source)
                self.manager.recordings.put(audio.get_raw_data()) # Sending stored bytes into manager recordings
