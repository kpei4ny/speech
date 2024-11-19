import customtkinter as ctk
from  speach import start_speach

class UISpeach(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speech to Text")

        self.geometry("400x200")
        self.grid_columnconfigure((0, 1), weight = 1)


        button = ctk.CTkButton(self, text="Start Listeting", command = None)
        button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan = 2)

        checkbox_1 = ctk.CTkCheckBox(self, text = "some_text")
        checkbox_1.grid(row = 1, column = 0, padx = 20, pady = (0, 20), sticky = "w")

        checkbox_2 = ctk.CTkCheckBox(self, text = "some_text2")
        checkbox_2.grid(row = 1, column = 1, padx = 20, pady = (0, 20), sticky = "w")


app = UISpeach()
app.mainloop()