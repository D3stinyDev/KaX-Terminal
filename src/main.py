import customtkinter as ctk
import os
import sys
import importlib.util
from logic.commands import CommandHandler
from logic.history import CommandHistory
from ui.themes import theme_manager
from utils.helpers import log_message, format_output, handle_error
from PIL import Image, ImageTk
from ui.custom_widgets import CustomEntry, CustomTextbox

class KaXTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("KaX Terminal Enhanced")
        self.root.geometry("800x600")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Initialize command history
        self.command_history = CommandHistory()

        # Apply theme
        theme_manager.apply_theme(self.root)

        # Create terminal display
        self.terminal_display = CustomTextbox(self.root, bg_color="black", text_color="green", font=("Courier", 12))
        self.terminal_display.pack(fill=ctk.BOTH, expand=True)
        self.terminal_display.insert(ctk.END, "Welcome to KaX Terminal Enhanced\n")
        self.terminal_display.configure(state='disabled')

        # Create command entry
        self.command_entry = CustomEntry(self.root, bg_color="black", text_color="green", font=("Courier", 12))
        self.command_entry.pack(fill=ctk.X, side=ctk.BOTTOM)
        self.command_entry.bind("<Return>", self.process_command)
        self.command_entry.bind("<Up>", self.show_previous_command)
        self.command_entry.bind("<Down>", self.show_next_command)

        # Load logo
        self.logo_label = load_logo(self.root)
        self.logo_label.pack(side=ctk.LEFT, padx=10, pady=10)

        # Load modules
        self.load_modules()

        # Initialize command handler
        self.command_handler = CommandHandler(self)

    def load_modules(self):
        modules_dir = os.path.join(os.path.dirname(__file__), "..", "config", "modules")
        if not os.path.exists(modules_dir):
            return

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py"):
                module_path = os.path.join(modules_dir, filename)
                module_name = filename[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                if hasattr(module, "modify_terminal"):
                    try:
                        module.modify_terminal(self)
                    except Exception as e:
                        self.display_error(f"Error loading module '{module_name}': {e}")

    def process_command(self, event):
        command = self.command_entry.get().strip()
        self.command_history.add_command(command)

        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(ctk.END, f"\n$ {command}\n")
        
        self.command_handler.execute_command(command)

        self.terminal_display.configure(state='disabled')
        self.command_entry.delete(0, ctk.END)

    def display_error(self, message):
        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(ctk.END, f"Error: {message}\n")
        self.terminal_display.configure(state='disabled')

    def display_message(self, message):
        self.terminal_display.configure(state='normal')
        self.terminal_display.insert(ctk.END, f"{message}\n")
        self.terminal_display.configure(state='disabled')

    def show_previous_command(self, event):
        prev = self.command_history.get_previous_command()
        if prev is not None:
            self.command_entry.delete(0, ctk.END)
            self.command_entry.insert(0, prev)

    def show_next_command(self, event):
        next_cmd = self.command_history.get_next_command()
        if next_cmd is not None:
            self.command_entry.delete(0, ctk.END)
            self.command_entry.insert(0, next_cmd)

    def clear_display(self):
        self.terminal_display.configure(state='normal')
        self.terminal_display.delete("1.0", ctk.END)
        self.terminal_display.configure(state='disabled')

    def quit(self):
        self.root.quit()

def load_logo(root):
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "KaX_Terminal_BlackBG_WhiteTxt.png")
    try:
        if os.path.exists(logo_path):
            image = Image.open(logo_path)
            image = image.resize((64, 64))  # Resize as needed
            photo = ImageTk.PhotoImage(image)
            label = ctk.CTkLabel(root, image=photo, text="")
            label.image = photo  # Keep a reference!
            return label
    except Exception as e:
        print(f"Logo load error: {e}")
    # Fallback if image is missing or invalid
    label = ctk.CTkLabel(root, text="KaX Terminal", font=("Courier", 16, "bold"))
    return label

if __name__ == "__main__":
    root = ctk.CTk()
    terminal = KaXTerminal(root)
    root.mainloop()

    # Path to the ball physics game module
    ball_game_module_path = os.path.join(terminal.base_dir, "assets/Interfaces/ballSimulationGame/ballPhysGame.py")