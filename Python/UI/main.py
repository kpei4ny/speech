import customtkinter as ctk
from speach import Choose_Device
import threading
import time


class UISpeach(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speech to Text")
        self.geometry("800x500")
        self.grid_columnconfigure((0, 1), weight=1)

        self.label = LabelInfo(self)
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        self.button = StartSpeachButton(self, text="Start Listening", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

        self.drop_down_list = DropDownList(self, class_for_listeting=self.button.class_for_listeting)
        self.drop_down_list.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

    def button_callback(self):
        # Зміна стану кнопки
        StartSpeachButton.processing = not StartSpeachButton.processing
        print(StartSpeachButton.processing)
        if StartSpeachButton.processing:
            self.button.configure(text="Listening")
            self.label.change_text("Listening...")
        else:
            self.button.configure(text="Not Listening")
            self.label.change_text("Stopped Listening")



class LabelInfo(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            text_color="#0871db",
            font=("Arial", 20),
            text="You can press the button to start listening",
        )

    def change_text(self, text):
        print(text)
        self.configure(text=text)


class StartSpeachButton(ctk.CTkButton):
    class_for_listeting = Choose_Device()
    speach_thread = None
    processing = False

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.configure(fg_color="black")

    def _on_enter(self, event=None):
        self.configure(text_color="black", fg_color="white")

    def _on_leave(self, event=None):
        self.configure(text_color="white", fg_color="black")

    def _on_click(self, event=None):
        if StartSpeachButton.processing and not StartSpeachButton.speach_thread:
            StartSpeachButton.speach_thread = threading.Thread(target=self._start_processing)
            StartSpeachButton.speach_thread.daemon = True
            StartSpeachButton.speach_thread.start()

    def _start_processing(self):
        while StartSpeachButton.processing:
            recognized_text = StartSpeachButton.class_for_listeting.start_speech()

            # Оновлення UI через метод `after` в основному потоці
            self.master.after(0, lambda: self.master.label.change_text(recognized_text))



class DropDownList(ctk.CTkOptionMenu):
    def __init__(self, master, class_for_listeting, **kwargs):
        self.class_for_listeting = class_for_listeting

        necessary_devices = self.class_for_listeting.necessary_devices

        self.option_var = ctk.StringVar(value=StartSpeachButton.class_for_listeting.get_name_of_current_device())
        super().__init__(master, values=necessary_devices, variable=self.option_var, **kwargs, command=self.Change_Device)

    def Change_Device(self, selected_value):
        self.class_for_listeting.change_output_device(selected_value)

    def get_selected_value(self):
        return self.option_var.get()


# Запуск програми
app = UISpeach()
app.mainloop()
