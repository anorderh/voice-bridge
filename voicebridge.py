from tkinter import END

import whisper
import langs
from playsound import playsound
from decoding import Decoder
from threading import Thread
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
        self.gui.after(0, self.sendToConsole, "!!! Application started!")

    def change_input_lang(self, new_input):
        self.input_lang.set(new_input)
        self.sendToConsole(f"<-- : Input language was changed to {new_input}")

    def change_output_lang(self, new_output):
        self.output_lang.set(new_output)
        self.sendToConsole(f"--> : Output language was changed to {new_output}")

    def swap(self):
        temp = self.input_lang.get()
        self.input_lang.set(self.output_lang.get())
        self.output_lang.set(temp)

        self.sendToConsole(f"<-> : Languages swapped! Now {self.input_lang.get()} to {self.output_lang.get()}")

    def play(self, idx=None):
        if not self.cur_recording:
            self.sendToConsole("X : No message is currently stored!")
        else:
            play = Thread(target=playsound, args=(self.cur_recording,))
            play.start()  # Start playing

            # Include 'idx' for playing stored recordings letter

    def sendToConsole(self, msg):
        self.console.configure(state="normal")
        self.console.insert(END, msg + "\n")
        self.console.see(END)
        self.console.configure(state="disabled")

    def press(self):
        if not self.on:
            self.on = True
            self.decoder.start_recording(langs.codes[self.input_lang.get()], langs.codes[self.output_lang.get()])
        else:
            self.on = False
            self.cur_recording = self.decoder.stop_recording()

            if not self.cur_recording:
                self.sendToConsole("No speech detected.")
            else:
                self.sendToConsole(f"\n\"{self.decoder.original}\"\n--->\n\"{self.decoder.translated}\"\n")
                self.play()

            self.decoder.reset()


if __name__ == '__main__':
    app = Base()
    app.gui.mainloop()
