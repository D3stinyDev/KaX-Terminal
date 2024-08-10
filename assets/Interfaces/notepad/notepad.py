import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD  # Importing TkinterDnD2 for drag-and-drop support
import os

class KaXNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("KaX Notepad")
        self.root.geometry("950x570")
        self.root.resizable(False, False)

        # Set up the text widget with word wrapping
        self.text_area = tk.Text(root, wrap=tk.WORD, font=("Courier", 12), undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Create the menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # Add File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Bindings for keyboard shortcuts
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-n>", self.new_file)

        # Bind drag and drop using TkinterDnD2
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.drop_file)

        # Initialize the file path variable
        self.file_path = None

    def new_file(self, event=None):
        """Create a new file by clearing the text area."""
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("KaX Notepad - New File")

    def open_file(self, event=None):
        """Open an existing file and display its content."""
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.root.title(f"KaX Notepad - {os.path.basename(file_path)}")

    def save_file(self, event=None):
        """Save the current content to a file."""
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("KaX Notepad", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self, event=None):
        """Save the content to a new file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                 initialdir=os.path.join("assets", "Interfaces", "notepad", "saved_notes"))
        if file_path:
            self.file_path = file_path
            self.save_file()

    def drop_file(self, event):
        """Handle the drop event to load a file into the text area."""
        file_path = event.data.strip('{}')  # Remove surrounding {} if they exist
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.file_path = file_path
            self.root.title(f"KaX Notepad - {os.path.basename(file_path)}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Using TkinterDnD.Tk directly as the root window
    notepad = KaXNotepad(root)
    root.mainloop()
