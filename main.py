import whisper
from playsound import playsound

RECORDING_LIMIT = 6

class Base:
    input_lang = "en"
    output_lang = "es"

    cur_recording = None
    model = whisper.load_model("base")
    # recordings = []

    def change_input_lang(self, input_lang):
        self.input_lang = input_lang
        self.sendToConsole(f"<-- : Input language was changed to {input_lang}")

    def change_output_lang(self, output_lang):
        self.output_lang = output_lang
        self.sendToConsole(f"--> : Output language was changed to {output_lang}")

    def swap(self):
        self.input_lang, self.output_lang = self.output_lang, self.input_lang

    def play(self, idx=None):
        if not self.cur_recording:
            self.sendToConsole("X : No message is currently stored!")
        else:
            playsound(self.cur_recording)
            # Include 'idx' for playing stored recordings letter

    def sendToConsole(self, msg):
        # Implement later with console box

    def start(self):

    def stop(self):

    # # Implement later for playing saved recordings
    # def save(self):


