from queue import Queue
from Microphone import Microphone
import whisper

class AppManager:
    def __init__(self, model):
        self.appState = Queue()
        self.recordings = Queue()
        self.model = model
        self.msg = ""

if __name__ == '__main__':
    model = whisper.load_model("base")
    app = AppManager(model)

    mic = Microphone(app)

    mic.start_recording()
    input("Press ENTER to stop recording.")
    mic.stop_recording()

    print(f"OpenAI Whisper: \n" + app.msg)
