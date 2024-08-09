import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import json
import os
import psutil

class KaXTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("KaX Terminal")

        # Initialize command history, history index, and aliases
        self.command_history = []
        self.history_index = -1
        self.aliases = {}

        # Create a frame for the terminal area
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load and resize the logo
        self.logo_path = "KaX Terminal/assets/KaX_Terminal_BlackBG_WhiteTxt.png"
        self.load_and_resize_logo()

        # Create a scrolled text widget for the terminal display
        self.terminal_display = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, bg="black", fg="green", insertbackground="white", font=("Courier", 12))
        self.terminal_display.pack(fill=tk.BOTH, expand=True)
        self.terminal_display.insert(tk.END, "Welcome to KaX Terminal\n")
        self.terminal_display.configure(state='disabled')  # Make the text widget read-only
        self.terminal_display.vbar.config(width=0)

        # Create an entry widget for the command input
        self.command_entry = tk.Entry(self.frame, bg="black", fg="green", insertbackground="white", font=("Courier", 12))
        self.command_entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Up>", self.previous_command)
        self.command_entry.bind("<Down>", self.next_command)

    def load_and_resize_logo(self):
        image = Image.open(self.logo_path)
        image = image.resize((100, 50), Image.Resampling.LANCZOS)  # Adjust size as needed
        self.logo_image = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(self.frame, image=self.logo_image, bg="black")
        self.logo_label.pack(side=tk.LEFT, padx=10, pady=10)

    def execute_command(self, event):
        command = self.command_entry.get().strip()

        # Check if the command is an alias
        if command in self.aliases:
            command = self.aliases[command]

        # Store the command in history if it's not empty and not a duplicate of the last command
        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
            self.history_index = len(self.command_history)  # Reset history index to end

        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(tk.END, f"\n$ {command}\n")
        
        if command == "cls" or command == "clear":
            self.terminal_display.delete(1.0, tk.END)
            print("Cleared the text on screen")
        elif command.startswith("echo "):
            self.terminal_display.insert(tk.END, command[5:] + "\n")
            print("Echo successful")
        elif command == "exit":
            self.root.quit()
            print("Program was closed with exit command")
        elif command == "version":
            self.terminal_display.insert(tk.END, "KaX Terminal Version 1.0\n")
            print("Displayed the KaX Terminal version")
        elif command.startswith("document-create") or command.startswith("doc-create"):
            self.handle_document_create(command)
            print("Created a document")
        elif command == "document-clear" or command == "doc-clear":
            self.handle_document_clear()
            print("Cleared all locally stored documents")
        elif command == "document-read" or command == "doc-read":
            self.handle_document_read()
            print("Displayed all local stored documents")
        elif command == "reload":
            self.restart_application(None)
            print("Reload command initiated, starting the messagebox")
        elif command == "settings":
            self.open_settings()
            print("Opened settings GUI")
        elif command == "credits":
            self.open_credits()
            print("Opened credits GUI")
        elif command == "resources":
            self.show_resources()
            print("Displayed system resource usage")
        elif command.startswith("alias "):
            self.set_alias(command)
            print("Alias set successfully")
        else:
            self.terminal_display.insert(tk.END, f"Command '{command}' not found.\n")
        
        # Auto-scroll to the end
        self.terminal_display.see(tk.END)

        self.terminal_display.configure(state='disabled')
        self.command_entry.delete(0, tk.END)

    def previous_command(self, event):
        if self.command_history:
            if self.history_index == -1:  # Start from the most recent command if index is -1
                self.history_index = len(self.command_history) - 1
            else:
                self.history_index = max(0, self.history_index - 1)  # Move to the previous command
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])

    def next_command(self, event):
        if self.command_history:
            if self.history_index == -1:
                return  # Do nothing if no command has been selected yet
            else:
                self.history_index = min(len(self.command_history) - 1, self.history_index + 1)  # Move to the next command
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])

    def show_resources(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(tk.END, f"CPU Usage: {cpu_usage}%\n")
        self.terminal_display.insert(tk.END, f"Memory Usage: {memory_info.percent}%\n")
        self.terminal_display.configure(state='disabled')

    def set_alias(self, command):
        parts = command.split(maxsplit=2)
        if len(parts) < 3:
            self.terminal_display.insert(tk.END, "Usage: alias <name> <command>\n")
            return
        alias_name, alias_command = parts[1], parts[2]
        self.aliases[alias_name] = alias_command
        self.terminal_display.insert(tk.END, f"Alias '{alias_name}' set for command '{alias_command}'\n")

    def handle_document_create(self, command):
        parts = command.split()
        title = ""
        description = ""
        message = ""
        for i in range(1, len(parts)):
            if parts[i] == "-title" and i + 1 < len(parts):
                title = parts[i + 1]
            elif parts[i] == "-description" and i + 1 < len(parts):
                description = parts[i + 1]
            elif parts[i] == "-message" and i + 1 < len(parts):
                message = parts[i + 1]
        
        document = {
            "title": title,
            "description": description,
            "message": message.replace('\\n', '\n').replace('/n', '\n')
        }

        self.save_document(document)

        self.terminal_display.insert(tk.END, f"Document created: {json.dumps(document, indent=2)}\n")

    def save_document(self, document):
        file_path = "KaX Terminal/database/documents.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    data = json.load(file)
            else:
                data = []
        except json.JSONDecodeError:
            data = []

        data.append(document)

        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def handle_document_clear(self):
        self.terminal_display.insert(tk.END, "Are you sure you want to clear all documents? Type 'yes' to confirm: ")

        def on_confirm(event):
            response = self.command_entry.get().strip().lower()
            self.terminal_display.configure(state='normal')
            self.terminal_display.insert(tk.END, f"\n$ {response}\n")
            if response == "yes":
                file_path = "KaX Terminal/database/documents.json"
                with open(file_path, "w") as file:
                    json.dump([], file)
                self.terminal_display.insert(tk.END, "All documents have been cleared.\n")
            else:
                self.terminal_display.insert(tk.END, "Document clear command cancelled.\n")
            
            self.command_entry.unbind("<Return>")
            self.command_entry.bind("<Return>", self.execute_command)
            self.command_entry.delete(0, tk.END)
            self.terminal_display.configure(state='disabled')

        self.command_entry.unbind("<Return>")
        self.command_entry.bind("<Return>", on_confirm)

    def handle_document_read(self):
        file_path = "KaX Terminal/database/documents.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    data = json.load(file)
                    if data:
                        self.terminal_display.insert(tk.END, f"Documents:\n{json.dumps(data, indent=2)}\n")
                    else:
                        self.terminal_display.insert(tk.END, "No documents found.\n")
            else:
                self.terminal_display.insert(tk.END, "No documents found.\n")
        except json.JSONDecodeError:
            self.terminal_display.insert(tk.END, "Error reading documents.\n")

    def restart_application(self, event):
        self.root.quit()
        os.system(f'python "{os.path.join("KaX Terminal", "assets", "messagebox", "restartMessageBox.py")}"')

    def open_settings(self):
        os.system(f'python "{os.path.join("KaX Terminal/assets/Interfaces/settings/settings.py")}"')

    def open_credits(self):
        os.system(f'python "{os.path.join("KaX Terminal", "assets", "Interfaces", "credits", "creditsGUI.py")}"')

if __name__ == "__main__":
    root = tk.Tk()
    terminal = KaXTerminal(root)
    root.mainloop()
