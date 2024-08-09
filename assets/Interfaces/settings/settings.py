import tkinter as tk
from tkinter import colorchooser, messagebox
import json
import os

class SettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")

        # Ensure the settings directory exists
        os.makedirs("KaX Terminal/assets/Interfaces/settings/consoleSettings", exist_ok=True)

        # Initialize settings
        self.settings_file = "KaX Terminal/assets/Interfaces/settings/consoleSettings/save.json"
        self.settings = {
            "background_color": "black",
            "text_color": "green",
            "shortcuts_enabled": {
                "reload": True
            }
        }
        self.load_settings()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Create color selection labels and buttons
        tk.Label(self.root, text="Background Color:").grid(row=0, column=0, padx=10, pady=10)
        self.bg_color_button = tk.Button(self.root, text=self.settings["background_color"], command=self.choose_bg_color)
        self.bg_color_button.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Text Color:").grid(row=1, column=0, padx=10, pady=10)
        self.text_color_button = tk.Button(self.root, text=self.settings["text_color"], command=self.choose_text_color)
        self.text_color_button.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Shortcuts Enabled:").grid(row=2, column=0, padx=10, pady=10)
        self.shortcut_reload_var = tk.BooleanVar(value=self.settings["shortcuts_enabled"].get("reload", True))
        self.shortcut_reload_check = tk.Checkbutton(self.root, text="Reload", variable=self.shortcut_reload_var)
        self.shortcut_reload_check.grid(row=2, column=1, padx=10, pady=10)

        # Create Save and Load buttons
        tk.Button(self.root, text="Save Settings", command=self.save_settings).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Load Settings", command=self.load_settings).grid(row=3, column=1, padx=10, pady=10)

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.settings["background_color"] = color
            self.bg_color_button.config(text=color)
    
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.settings["text_color"] = color
            self.text_color_button.config(text=color)

    def save_settings(self):
        self.settings["shortcuts_enabled"]["reload"] = self.shortcut_reload_var.get()
        try:
            with open(self.settings_file, 'w') as file:
                json.dump(self.settings, file, indent=4)
            messagebox.showinfo("Settings", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    self.settings = json.load(file)
                    self.bg_color_button.config(text=self.settings.get("background_color", "black"))
                    self.text_color_button.config(text=self.settings.get("text_color", "green"))
                    self.shortcut_reload_var.set(self.settings.get("shortcuts_enabled", {}).get("reload", True))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsGUI(root)
    root.mainloop()
