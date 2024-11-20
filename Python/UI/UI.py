import customtkinter as ctk
from  speach import Choose_Device
import threading
import time

class UISpeach(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speech to Text")

        self.geometry("800x500")
        self.grid_columnconfigure((0, 1), weight = 1)

        self.label = Label_info(self)
        self.label.grid(row = 0, column = 0, padx = 20, pady = 20, columnspan = 2)

        self.button = StartSpeachButton(self, text = "Start Listeting", command = self.button_callback)
        self.button.grid(row = 1, column = 0, padx = 20, pady = 20, columnspan = 2)
    def button_callback(self):
        StartSpeachButton.processing = not StartSpeachButton.processing

        if(StartSpeachButton.processing):
            StartSpeachButton.text = "Listening"
        elif(not StartSpeachButton.processing):
            StartSpeachButton.text = "Doesn't listening"

        self.label.change_text(StartSpeachButton.text)


class Label_info(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text_color = "#0871db", font = ("Arial", 20), text = "You can press on the button to start listening")
    def change_text(self, text):
        print(text)
        self.configure(text = text)


class StartSpeachButton(ctk.CTkButton):
    speach_thread = None
    processing = False
    text = None
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.configure(fg_color="black")

    def _on_enter(self, event=None):
        self.hover_function()

    def _on_leave(self, event=None):
        self.leave_function()

    def _on_click(self, event=None):
        if(StartSpeachButton.processing):
            StartSpeachButton.speach_thread = threading.Thread(target=self._start_processing)
            StartSpeachButton.speach_thread.start()


    def _start_processing(self):
        class_for_listeting = Choose_Device()

        while(StartSpeachButton.processing):
            class_for_listeting.start_speech()

    def hover_function(self):
        self.configure(text_color="black", fg_color="white")

    def leave_function(self):
        self.configure(text_color="white", fg_color="black")

    def get_text(self):
        return self.text


app = UISpeach()
app.mainloop()