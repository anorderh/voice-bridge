from threading import Thread
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
        # Begin recording
        print("Starting...")

        record = Thread(target=self.record_microphone)
        record.start()  # Start recording

        transcribe = Thread(target=tr.realtime_transcribe, args=(self.manager, lang))
        transcribe.start()  # Starting transcribing

    def stop_recording(self):
        self.manager.appState.get()  # "OFF"
        while not self.manager.recordings.empty():      # Waiting for transcription to complete
            pass
        print("Stopped.")

    def record_microphone(self):  # Reading 1024 frames at a time
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        r.energy_threshold = 500

        with sr.Microphone(sample_rate=16000) as source:
            while not self.manager.appState.empty():  # Recording is ongoing
                # Recording bytes until pause detected
                audio = r.listen(source)
                data = io.BytesIO(audio.get_wav_data()).read()

                # Sending stored bytes into manager recordings
                self.manager.recordings.put(data)
