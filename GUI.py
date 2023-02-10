import tkinter
import customtkinter as ctk

def init(appBase):
    root = ctk.CTk()
    root.state('zoomed')

    # Base frame
    main = ctk.CTkFrame(master=root)
    main.pack(pady=20, padx=60, fill="both", expand=True)


    # Demo buttons
    inputFrame = ctk.CTkFrame(main)
    inputFrame.pack(pady=0, padx=0)

    input_lang_box = ctk.CTkComboBox(inputFrame, values=["en", "es"])
    input_lang_box.pack(pady=20, padx=20, side=tkinter.LEFT)

    swap_button = ctk.CTkButton(master=inputFrame, text="Swap")
    swap_button.pack(pady=20, padx=20, side=tkinter.LEFT)

    output_lang_box = ctk.CTkComboBox(inputFrame, values=["es", "en"])
    output_lang_box.pack(pady=20, padx=20, side=tkinter.LEFT)

    root.mainloop()


