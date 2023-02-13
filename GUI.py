import tkinter
import customtkinter as ctk
from PIL import Image

import langs


def init(appBase):
    root = ctk.CTk(fg_color="#040329")
    root.state('zoomed')
    root.geometry("750x450")
    root.winfo_toplevel().title("VoiceBridge")

    ctk.set_default_color_theme("blue")

    # Base frame
    main = ctk.CTkFrame(master=root, width=1200, fg_color="#3b3982")
    main.pack(pady=20, padx=60, fill="both", expand=True)

    # Language frame, holding language info
    langFrame = ctk.CTkFrame(main, fg_color="#0c0a40")
    langFrame.pack(pady=10, padx=0, side=tkinter.TOP)

    input_lang_frame = ctk.CTkFrame(langFrame, fg_color="#0c0a40")

    # --> Language info variables
    input_s, output_s = "english", "spanish"  # Starting values
    input_lang_var = ctk.StringVar(value=input_s)
    output_lang_var = ctk.StringVar(value=output_s)
    appBase.input_lang, appBase.output_lang = input_lang_var, output_lang_var

    input_lang_label = ctk.CTkLabel(input_lang_frame, text="Input").grid(row=0, column=0)
    input_lang_box = ctk.CTkComboBox(input_lang_frame, values=langs.codes.keys(), variable=input_lang_var,
                                     command=appBase.change_input_lang, state="readonly").grid(row=1, column=0)
    input_lang_frame.pack(pady=10, padx=10, side=tkinter.LEFT)

    swap_button = ctk.CTkButton(master=langFrame, text="Swap", command=appBase.swap)
    swap_button.pack(pady=10, padx=5, side=tkinter.LEFT)

    output_lang_frame = ctk.CTkFrame(langFrame, fg_color="#0c0a40")

    output_lang_label = ctk.CTkLabel(output_lang_frame, text="Output").grid(row=0, column=0)
    output_lang_box = ctk.CTkComboBox(output_lang_frame, values=langs.codes.keys(), variable=output_lang_var,
                                      command=appBase.change_output_lang, state="readonly").grid(row=1, column=0)
    output_lang_frame.pack(pady=10, padx=10, side=tkinter.LEFT)

    # Control Frame
    control_frame = ctk.CTkFrame(main, fg_color="#0c0a40")
    console_output = ctk.CTkTextbox(master=control_frame, height=200, state="disabled", activate_scrollbars=False,
                                    fg_color="#070708")

    logo = ctk.CTkImage(dark_image=Image.open("voicebridgeLogo.png"), size=(60, 60))

    # --> Button frame
    button_frame = ctk.CTkFrame(control_frame, fg_color="#0c0a40")
    logo_widget = ctk.CTkLabel(master=button_frame, text="", image=logo)
    record_button = ctk.CTkButton(master=button_frame, text="REC", fg_color="#525252", command=appBase.press)
    play_button = ctk.CTkButton(master=button_frame, text="PLAY", fg_color="green", command=appBase.play)
    save_button = ctk.CTkButton(master=button_frame, text="SAVE", fg_color="#525252", command=appBase.toggle_saving)

    logo_widget.pack(pady=10, padx=10, side=tkinter.TOP)
    record_button.pack(pady=10, side=tkinter.TOP)
    play_button.pack(pady=10, side=tkinter.TOP)
    save_button.pack(pady=10, side=tkinter.TOP)

    # Storing indicators to dynamically change
    appBase.rec_indicator = record_button
    appBase.save_indicator = save_button

    # --> Presets
    preset_frame = ctk.CTkFrame(button_frame, fg_color="#0c0a40")
    preset1 = ctk.CTkButton(master=preset_frame, text="1", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(1, preset1))
    preset2 = ctk.CTkButton(master=preset_frame, text="2", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(2, preset2))
    preset3 = ctk.CTkButton(master=preset_frame, text="3", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(3, preset3))
    preset4 = ctk.CTkButton(master=preset_frame, text="4", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(4, preset4))
    preset5 = ctk.CTkButton(master=preset_frame, text="5", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(5, preset5))
    preset6 = ctk.CTkButton(master=preset_frame, text="6", fg_color="#7e7e80", width=25, height=25,
                            command=lambda: appBase.press_preset(6, preset6))
    preset1.pack(side=tkinter.LEFT)
    preset2.pack(side=tkinter.LEFT)
    preset3.pack(side=tkinter.LEFT)
    preset4.pack(side=tkinter.LEFT)
    preset5.pack(side=tkinter.LEFT)
    preset6.pack(side=tkinter.LEFT)

    preset_frame.pack(pady=10, padx=10, side=tkinter.BOTTOM)
    console_output.pack(pady=10, padx=10, side=tkinter.LEFT, fill="both", expand=1)
    button_frame.pack(pady=10, padx=10, side=tkinter.RIGHT)
    control_frame.pack(pady=10, padx=10, side=tkinter.BOTTOM, fill="both", expand=1)

    # Integrating frontend w/ backend
    appBase.console = console_output
    appBase.gui = root
