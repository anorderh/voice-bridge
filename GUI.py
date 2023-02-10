import tkinter
import customtkinter as ctk


def init(appBase):
    root = ctk.CTk()
    root.state('zoomed')

    ctk.set_default_color_theme("blue")

    # Base frame
    main = ctk.CTkFrame(master=root)
    main.pack(pady=20, padx=60, fill="both", expand=True)

    # Language frame, holding language info
    langFrame = ctk.CTkFrame(main)
    langFrame.pack(pady=0, padx=0, side=tkinter.TOP)

    input_lang_frame = ctk.CTkFrame(langFrame)

    # --> Language info variables
    input_lang_var = ctk.StringVar(value="en")
    output_lang_var = ctk.StringVar(value="es")
    appBase.input_lang = input_lang_var
    appBase.output_lang = output_lang_var

    input_lang_label = ctk.CTkLabel(input_lang_frame, text="Input").grid(row=0, column=0)
    input_lang_box = ctk.CTkComboBox(input_lang_frame, values=["en", "es"], variable=input_lang_var).grid(row=1, column=0)
    input_lang_box.bind("<<ComboboxSelected>>", appBase.change_input_lang)
    input_lang_frame.pack(pady=10, padx=10, side=tkinter.LEFT)

    swap_button = ctk.CTkButton(master=langFrame, text="Swap")
    swap_button.pack(pady=10, padx=5, side=tkinter.LEFT)

    output_lang_frame = ctk.CTkFrame(langFrame)

    output_lang_label = ctk.CTkLabel(output_lang_frame, text="Output").grid(row=0, column=0)
    output_lang_box = ctk.CTkComboBox(output_lang_frame, values=["es", "en"], variable=output_lang_var).grid(row=1, column=0)
    output_lang_box.bind("<<ComboboxSelected>>", appBase.change_output_lang)
    output_lang_frame.pack(pady=10, padx=10, side=tkinter.LEFT)

    # Control Frame
    control_frame = ctk.CTkFrame(main)
    console_output = ctk.CTkTextbox(master=control_frame, height=200, state="disabled", activate_scrollbars=False)

    # --> # Button frame
    button_frame = ctk.CTkFrame(control_frame)
    record_button = ctk.CTkButton(master=button_frame, text="REC", fg_color="red", command=appBase.press)
    play_button = ctk.CTkButton(master=button_frame, text="PLAY", fg_color="green",command=appBase.play)
    record_button.pack(pady=10, side=tkinter.TOP)
    play_button.pack(pady=10, side=tkinter.BOTTOM)

    console_output.pack(pady=10, padx=10, side=tkinter.LEFT, fill="both", expand=1)
    button_frame.pack(pady=10, padx=10, side=tkinter.RIGHT)
    control_frame.pack(pady=10, padx=10, side=tkinter.BOTTOM, fill="both", expand=1)

    # Integrating frontend w/ backend
    appBase.console = console_output
    appBase.gui = root
