import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def show_messagebox():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    result = messagebox.askyesno("KaX Terminal", "The program has been closed, if you want to restart it press 'yes'. If you want to close the program press 'no'.")

    if result:  # User pressed "Yes"
        python_file_path = "main.py"  # Replace with your Python file path
        if os.path.exists(python_file_path):
            subprocess.Popen(['python', python_file_path])
        else:
            messagebox.showerror("Error", f"File not found: {python_file_path}")

    root.destroy()  # Destroy the root window

if __name__ == "__main__":
    show_messagebox()
