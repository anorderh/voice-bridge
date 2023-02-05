from queue import Queue
from gtts import gTTS
from Microphone import Microphone
import Transcription as tr
import whisper
import Translation as ts

class AppManager:
    def __init__(self, model):
        self.appState = Queue()
        self.model = model
        self.recording = b""
        self.transcription = ""

if __name__ == '__main__':
    model = whisper.load_model("base")  # Application
    input_lang = "en"
    output_lang = "hi"
    app = AppManager(model)

    mic = Microphone(app)

    mic.start_recording()               # 1. Recording microphone
    input("Press ENTER to stop recording.")
    mic.stop_recording()

    tr.speech_recognition(app, input_lang)          # 2. Transcripting audio
    msg = app.transcription
    print(f"OpenAI Whisper: \n" + msg)

    translated = ts.translate(msg, from_code=input_lang, to_code=output_lang) # 3. Translating message
    print(f"Translation: \n" + translated)

    tts = gTTS(translated, lang=output_lang)    # 4. Synthesizing speech
    tts.save('test.mp3')
