from queue import Queue
from Microphone import Microphone
import Transcription as tr
import whisper

class AppManager:
    def __init__(self, model):
        self.appState = Queue()
        self.model = model
        self.recording = b""
        self.transcription = ""

if __name__ == '__main__':
    model = whisper.load_model("base")  # Application
    app = AppManager(model)

    mic = Microphone(app)

    mic.start_recording()               # Recording microphone
    input("Press ENTER to stop recording.")
    mic.stop_recording()

    tr.speech_recognition(app)          # Transcripting audio
    print(f"OpenAI Whisper: \n" + app.transcription)

    
