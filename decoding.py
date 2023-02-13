from queue import Queue
from threading import Thread
import time
import numpy as np
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS


class Decoder:
    def __init__(self, model, change_status):
        self.states = Queue()
        self.record_thread = self.transcribe_thread = None
        self.model = model
        self.recog = self.init_recognizer()

        self.bytes = Queue()
        self.transcriptions = []
        self.id = 1

        self.change_status = change_status # To change voicebridge.py mode

        self.original = self.translated = self.filepath = self.output_lang = self.input_lang = None

    def init_recognizer(self):
        recog = sr.Recognizer()
        recog.non_speaking_duration = 0.1
        recog.pause_threshold = 0.3
        recog.energy_threshold = 500

        return recog

    def start_recording(self, input_lang, output_lang):
        """
        Record and transcribe audio. Processes per SpeechRecognizer segment.
        :param input_lang:
        :param output_lang:
        :return:
        """
        self.states.put(True)  # "ON"

        self.input_lang = input_lang
        self.output_lang = output_lang

        record = Thread(target=self.record_microphone)
        transcribe = Thread(target=self.realtime_transcribe)
        self.record_thread, self.transcribe_thread = record, transcribe

        record.start()  # Start recording
        transcribe.start()  # Start transcribing

    def record_microphone(self):
        # Speech Recognizer settings
        with sr.Microphone(sample_rate=16000) as source:
            try: # try-block incase timeout occurs
                while not self.states.empty():  # App status check
                    audio = self.recog.listen(source=source, timeout=3)  # Blocking until 'pause_threshold' met
                    self.bytes.put(audio.get_raw_data())
            except sr.WaitTimeoutError:
                # Turn off device
                self.change_status()
                self.states.get()

    def realtime_transcribe(self, force=False):
        # If app is on or forced transcription
        while not self.states.empty() or force:
            if not self.bytes.empty():
                frames = self.bytes.get()

                # Translating np.array holding bytes into Tensor, per OpenAI Whisper formatting
                # https://github.com/openai/whisper/discussions/450
                np_audio = (np.frombuffer(frames, np.int16).flatten().astype(np.float32) / 32768.0)

                result = self.model.transcribe(np_audio, language=self.input_lang)
                self.transcriptions.append(result["text"])

            force = False
            time.sleep(0.5) # To reduce frequent iterations

    def stop_recording(self):
        """
        Stop recording, translate whole transcription, and generate speech.
        :return:
        """
        self.states.get() # "OFF"

        # Waiting for threads to finish
        self.record_thread.join()
        self.transcribe_thread.join()

        if not self.bytes.empty():  # Completing transcription if bytes present
            self.realtime_transcribe(True)

        self.original = " ".join(self.transcriptions)[1:]  # Remove extra space on end
        if self.original == "":
            return None
        self.translate(self.original)
        self.generateSpeech()

        # Return filepath, original audio, and translation
        return self.filepath, self.original, self.translated

    def translate(self, text):
        self.translated = GoogleTranslator(source=self.input_lang, target=self.output_lang).translate(text)

    def generateSpeech(self):
        tts = gTTS(self.translated, lang=self.output_lang)

        # Generate file w/ unique ID
        identifier = "recordings/" + str(self.id) + ".mp3"
        tts.save(identifier)
        self.id += 1

        self.filepath = identifier

    def reset(self):
        self.transcriptions.clear()
        self.record_thread = self.transcribe_thread = None
        self.original = self.translated = self.filepath = self.output_lang = self.input_lang = None
