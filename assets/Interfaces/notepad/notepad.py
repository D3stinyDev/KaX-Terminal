import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

class Notepad(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Notepad")
        self.geometry("600x400")
        
        self.text_area = ctk.CTkTextbox(self, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)  # Use standard tkinter Menu
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def new_file(self):
        self.text_area.delete(1.0, ctk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"),
                                                           ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, ctk.END)
                self.text_area.insert(ctk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt"),
                                                             ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, ctk.END)
                file.write(content)

if __name__ == "__main__":
    app = ctk.CTk()
    notepad = Notepad(master=app)
    app.mainloop()
