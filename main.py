import tkinter as tk
from tkinter import scrolledtext
import json
import os
from PIL import Image, ImageTk
import psutil
import random
from datetime import datetime
import time
import importlib.util
import sys

class KaXTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("KaX Terminal")

        # Initialize command history and history index
        self.command_history = []
        self.history_index = -1

        # Determine the base directory where the script is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Create a frame for the terminal area
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load and resize the logo
        self.logo_path = os.path.join(self.base_dir, "assets", "KaX_Terminal_BlackBG_WhiteTxt.png")
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

        # Bind CTRL + R to a function
        self.root.bind("<Control-r>", self.refresh_terminal)

        # Load modules after terminal has been fully initialized
        self.load_modules()

    def load_modules(self):
        modules_dir = os.path.join(self.base_dir, "config", "modules")
        if not os.path.exists(modules_dir):
            return  # If no modules directory exists, do nothing

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py"):  # Load only Python files
                module_path = os.path.join(modules_dir, filename)
                module_name = filename[:-3]  # Strip the .py extension

                # Dynamically load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Check if the module has a `modify_terminal` function and call it
                if hasattr(module, "modify_terminal"):
                    try:
                        module.modify_terminal(self)
                    except Exception as e:
                        self.terminal_display.configure(state='normal')
                        self.terminal_display.insert(tk.END, f"Error while loading module '{module_name}': {e}\n")
                        self.terminal_display.configure(state='disabled')

    def refresh_terminal(self, event):
        # Implement the action to be performed on CTRL + R
        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(tk.END, "\nRefreshing...\n")
        self.terminal_display.configure(state='disabled')
        self.terminal_display.see(tk.END)

    def load_and_resize_logo(self):
        image = Image.open(self.logo_path)
        image = image.resize((100, 50), Image.Resampling.LANCZOS)  # Adjust size as needed
        self.logo_image = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(self.frame, image=self.logo_image, bg="black")
        self.logo_label.pack(side=tk.LEFT, padx=10, pady=10)

    def execute_command(self, event):
        command = self.command_entry.get().strip()

        # Store the command in history if it's not empty and not a duplicate of the last command
        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
            self.history_index = len(self.command_history)  # Reset history index to end

        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(tk.END, f"\n$ {command}\n")
        
        if command == "cls" or command == "clear":
            self.terminal_display.delete(1.0, tk.END)
        elif command.startswith("echo "):
            self.terminal_display.insert(tk.END, command[5:] + "\n")
        elif command == "exit":
            self.root.quit()
        elif command == "version":
            self.terminal_display.insert(tk.END, "KaX Terminal Version 1.3.0\n")
        elif command == "crashTerminal":
            self.crash_terminal()
        elif command == "showTimestamp" or command == "showTms":
            self.show_timestamp()
        elif command.startswith("setColor "):
            self.set_color(command)
        elif command.startswith("countdown "):
            self.countdown(command)
        elif command == "resources":
            self.show_resources()
        elif command == "ballPhysicsGame":
            self.open_ball_physics_game()
        elif command == "notepad" or command == "ntpd":
            self.open_notepad()
        else:
            self.terminal_display.insert(tk.END, f"Command '{command}' not found.\n")
        
        # Auto-scroll to the end
        self.terminal_display.see(tk.END)

        self.terminal_display.configure(state='disabled')
        self.command_entry.delete(0, tk.END)

    def crash_terminal(self):
        self.terminal_display.insert(tk.END, "Simulating terminal crash... Just kidding! 😄\n")
        fun_messages = [
            "Blue Screen of Death Incoming!",
            "Segmentation fault. Core dumped. Or not.",
            "Oops, something went wrong... oh wait, just kidding!",
            "Exploding in 3... 2... 1... 💥"
        ]
        self.terminal_display.insert(tk.END, random.choice(fun_messages) + "\n")

    def show_timestamp(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.terminal_display.insert(tk.END, f"Current Timestamp: {timestamp}\n")

    def set_color(self, command):
        parts = command.split()
        if len(parts) == 3:
            bg_color = parts[1]
            fg_color = parts[2]
            self.terminal_display.configure(bg=bg_color, fg=fg_color)
            self.command_entry.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
            self.terminal_display.insert(tk.END, f"Terminal colors updated. Background: {bg_color}, Text: {fg_color}\n")
        else:
            self.terminal_display.insert(tk.END, "Usage: setColor <bg_color> <fg_color>\nExample: setColor black green\n")

    def countdown(self, command):
        try:
            # Extract time value and unit (s, m, h)
            parts = command.split()
            if len(parts) != 2:
                self.terminal_display.insert(tk.END, "Usage: countdown <time>\nExamples: countdown 20s, countdown 1m, countdown 1h\n")
                return

            time_value = int(parts[1][:-1])
            time_unit = parts[1][-1]

            # Convert to seconds based on the unit
            if time_unit == 's':
                total_seconds = time_value
            elif time_unit == 'm':
                total_seconds = time_value * 60
            elif time_unit == 'h':
                total_seconds = time_value * 3600
            else:
                self.terminal_display.insert(tk.END, "Invalid time unit. Use 's' for seconds, 'm' for minutes, or 'h' for hours.\n")
                return

            # Start the countdown
            while total_seconds > 0:
                mins, secs = divmod(total_seconds, 60)
                time_format = f'{mins:02}:{secs:02}'
                self.terminal_display.insert(tk.END, f"\rCountdown: {time_format}\n")
                self.terminal_display.update()
                time.sleep(1)
                total_seconds -= 1

            self.terminal_display.insert(tk.END, "Time's up!\n")
        except Exception as e:
            self.terminal_display.insert(tk.END, f"Error during countdown: {e}\n")

    def open_notepad(self):
        os.system(f'python "{os.path.join(self.base_dir, "assets/Interfaces/notepad/notepad.py")}"')

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

    def open_ball_physics_game(self):
        os.system(f'python "{os.path.join(self.base_dir, "assets/Interfaces/ballSimulationGame/ballPhysGame.py")}"')

if __name__ == "__main__":
    root = tk.Tk()
    terminal = KaXTerminal(root)
    root.mainloop()
