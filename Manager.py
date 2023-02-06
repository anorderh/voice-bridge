from queue import Queue
from gtts import gTTS
from Microphone import Microphone
import Transcription as tr
import whisper
import Translation as ts
import time

class AppManager:
    def __init__(self, model):
        self.appState = Queue()
        self.model = model
        self.recording = b""
        self.transcription = ""

if __name__ == '__main__':
    model = whisper.load_model("base")  # Application
    input_lang = "en"
    output_lang = "es"
    start_time =  None
    app = AppManager(model)
    mic = Microphone(app)

    print("1. Recording microphone")
    start_time = time.time()

    mic.start_recording()               # 1. Recording microphone
    input("Press ENTER to stop recording.")
    mic.stop_recording()

    print(f"Step #1 took {time.time() - start_time} seconds!")


    print("2. Audio transcription")
    start_time = time.time()

    tr.speech_recognition(app, input_lang)          # 2. Transcripting audio
    msg = app.transcription
    print(f"OpenAI Whisper: \n" + msg)

    print(f"Step #2 took {time.time() - start_time} seconds!")


    print("3. Transation")
    start_time = time.time()

    translated = ts.translate(msg, from_code=input_lang, to_code=output_lang) # 3. Translating message
    print(f"Translation: \n" + translated)

    print(f"Step #3 took {time.time() - start_time} seconds!")

    print("4. Speech synthesis")
    start_time = time.time()

    tts = gTTS(translated, lang=output_lang)    # 4. Synthesizing speech
    tts.save('test.mp3')

    print(f"Step #4 took {time.time() - start_time} seconds!")
