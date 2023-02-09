from queue import Queue
from gtts import gTTS
from Microphone import Microphone
import whisper
import Translation as ts
import time
from playsound import playsound

class AppManager:
    def __init__(self, model):
        self.recording = False
        self.processing = False

        self.model = model
        self.recordings = Queue()
        self.transcription = []

def formatText(text: str):
    size = len(text)
    for i in range(60,size,60):
        text = text[:i] + "\n" + text[i:]
    return text

if __name__ == '__main__':
    model = whisper.load_model("base")  # Application

    input_lang = "en"
    output_lang = "es"
    start_time = None
    app = AppManager(model)
    mic = Microphone(app)

    print("1. Recording & transcribing microphone")

    start_time = time.time()
    mic.start_recording(input_lang)          # 1. Recording microphone w/ live transcription
    input("Press ENTER to stop recording.")
    mic.stop_recording()
    msg = " ".join(app.transcription)
    print(f"OpenAI Whisper: \n" + msg)
    print(f"Step #1 took {time.time() - start_time} seconds!")

    print("2. Translation")

    start_time = time.time()
    translated = ts.translate(msg, from_code=input_lang, to_code=output_lang)  # 2. Translating message
    print(f"Translation: \n" + translated)
    print(f"Step #3 took {time.time() - start_time} seconds!")

    print("3. Speech synthesis")

    start_time = time.time()
    tts = gTTS(translated, lang=output_lang)    # 3. Synthesizing speech
    tts.save('test.mp3')
    print(f"Step #4 took {time.time() - start_time} seconds!")

    print("4. Play translated speech")

    playsound('test.mp3')


