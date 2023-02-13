from tkinter import END

import whisper
import langs
from playsound import playsound
from decoding import Decoder
from threading import Thread
import GUI

RECORDING_LIMIT = 6


class Base:
    # Language info and recordings
    input_lang = None
    output_lang = None
    cur_recording = None
    saved_recordings = [None]*6

    # ML model & Whisper decoding
    model = whisper.load_model("base")
    decoder = Decoder(model)

    # GUI components
    gui = None
    console = None
    rec_indicator = None
    save_indicator = None

    # Statuses
    on = False
    save_mode = False

    def __init__(self):
        GUI.init(self)
        self.gui.after(0, self.send_to_console, "!!! Application started!")

    def change_input_lang(self, new_input):
        self.input_lang.set(new_input)
        self.send_to_console(f"<-- : Input language was changed to {new_input}")

    def change_output_lang(self, new_output):
        self.output_lang.set(new_output)
        self.send_to_console(f"--> : Output language was changed to {new_output}")

    def swap(self):
        temp = self.input_lang.get()
        self.input_lang.set(self.output_lang.get())
        self.output_lang.set(temp)

        self.send_to_console(f"<-> : Languages swapped! Now {self.input_lang.get()} to {self.output_lang.get()}")

    def play(self, idx=None):
        if idx != None: # Play recording at idx
            if self.saved_recordings[idx] is not None:
                play = Thread(target=playsound, args=(self.saved_recordings[idx],))
                play.start()
                return
        else:
            # No idx so play current recording
            if self.cur_recording is not None:
                play = Thread(target=playsound, args=(self.cur_recording,))
                play.start()
                return

        # Desired recording not found
        self.send_to_console("X : No message is currently stored!")

    def toggle_saving(self):
        self.save_mode = not self.save_mode
        if self.save_mode: # SAVING - "ON"
            self.save_indicator.configure(fg_color="#0020bf")
        else:              # SAVING - "OFF"
            self.save_indicator.configure(fg_color="#525252")

    def press_preset(self, idx, button):
        if self.save_mode:
            # Save current recording to preset
            if self.cur_recording:
                self.saved_recordings[idx] = self.cur_recording
                button.configure(fg_color="#0020bf")
                self.send_to_console("S : Saved recording to preset #" + str(idx))
            else:
                self.send_to_console("X : No message is currently stored!")
        else:
            # Play preset's recording
            self.play(idx)

    def press(self):
        '''
        press() toggles VoiceBridge's recording
        :return:
        '''
        if not self.on: # RECORDING - "ON"
            self.on = True
            self.change_rec_indicator()
            self.decoder.start_recording(langs.codes[self.input_lang.get()], langs.codes[self.output_lang.get()])
        else:           # RECORDING - "OFF"
            self.on = False
            self.change_rec_indicator()
            self.cur_recording = self.decoder.stop_recording()

            # Speech check
            if not self.cur_recording:
                self.send_to_console("No speech detected.")
            else:
                self.send_to_console(f"\n\"{self.decoder.original}\"\n--->\n\"{self.decoder.translated}\"\n")
                self.play()

            # Reset decoder values
            self.decoder.reset()

    def change_rec_indicator(self):
        if self.on:
            self.rec_indicator.configure(fg_color="red")
        else:
            self.rec_indicator.configure(fg_color="#525252")

    def send_to_console(self, msg):
        self.console.configure(state="normal")
        self.console.insert(END, msg + "\n")
        self.console.see(END)
        self.console.configure(state="disabled")


if __name__ == '__main__':
    app = Base()
    app.gui.mainloop()
