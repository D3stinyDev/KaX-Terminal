import customtkinter as ctk

class CustomScrolledText(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.text_area = CTkTextbox(self, wrap='word', bg_color='black', text_color='green', font=("Courier", 12))
        self.text_area.pack(side='left', fill='both', expand=True)

        self.scrollbar = CTkScrollbar(self, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.text_area.configure(yscrollcommand=self.scrollbar.set)

    def insert(self, *args, **kwargs):
        self.text_area.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.text_area.delete(*args, **kwargs)

    def configure(self, **kwargs):
        self.text_area.configure(**kwargs)

    def see(self, *args, **kwargs):
        self.text_area.see(*args, **kwargs)

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, border_width=2, corner_radius=8, **kwargs)

class CustomTextbox(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, border_width=2, corner_radius=8, **kwargs)

class CustomButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='green', hover_color='darkgreen')

class CustomLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text_color='green')