import whisper
from Microphone import Microphone
import Transcription as tr

if __name__ == '__main__':
    model = whisper.load_model("base")

    mic = Microphone()

    mic.start_recording()
    input("Press ENTER to stop recording.")
    mic.stop_recording()

    tr.speech_recognition(model, mic.storedAudio)
