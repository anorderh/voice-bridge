from tkinter import END

import whisper
from playsound import playsound
from decoding import Decoder
import GUI

RECORDING_LIMIT = 6

class Base:
    input_lang = None
    output_lang = None

    cur_recording = None
    model = whisper.load_model("base")
    decoder = Decoder(model)

    gui = None
    console = None

    on = False

    def __init__(self):
        GUI.init(self)
        self.gui.after(0, self.sendToConsole, "Application started!")

    def change_input_lang(self):
        self.sendToConsole(f"<-- : Input language was changed to {self.input_lang.get()}")

    def change_output_lang(self):
        self.sendToConsole(f"--> : Output language was changed to {self.output_lang.get()}")

    def swap(self):
        temp = self.input_lang.get()
        self.input_lang.set(self.output_lang.get())
        self.output_lang.set(temp)

        self.sendToConsole(f"--> : Languages swapped! Now {self.input_lang.get()} to {self.output_lang.get()}")

    def play(self, idx=None):
        if not self.cur_recording:
            self.sendToConsole("X : No message is currently stored!")
        else:
            playsound(self.cur_recording)
            # Include 'idx' for playing stored recordings letter

    def sendToConsole(self, msg):
        self.console.configure(state="normal")
        self.console.insert(END, msg + "\n")
        self.console.configure(state="disabled")

    def press(self):
        if not self.on:
            self.decoder.start_recording(self.input_lang.get(), self.output_lang.get())
            self.on = True
        else:
            self.cur_recording = self.decoder.stop_recording()

            self.sendToConsole(f"\n{self.decoder.original}\"\n--->\n\"{self.decoder.translated}\"\n")
            self.play()

            self.on = False

if __name__ == '__main__':
    app = Base()
    app.gui.mainloop()
