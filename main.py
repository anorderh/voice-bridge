import whisper
from playsound import playsound
from decoding import Decoder

RECORDING_LIMIT = 6

class Base:
    input_lang = "en"
    output_lang = "es"

    cur_recording = None
    model = whisper.load_model("base")
    decoder = Decoder(model)

    on = False
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
        print(msg)

    def press(self):
        if not self.on:
            self.decoder.start_recording(self.input_lang, self.output_lang)
        else:
            self.cur_recording = self.decoder.stop_recording()

            self.sendToConsole(self.decoder.original + "\nto\n" + self.decoder.translated) # Display translation
            self.play()

    # # Implement later for playing saved recordings
    # def save(self):


