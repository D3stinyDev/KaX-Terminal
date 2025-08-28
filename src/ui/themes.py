import customtkinter as ctk

class ThemeManager:
    def apply_theme(self, root):
        ctk.set_appearance_mode("dark")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("dark-blue")  # Options: "blue", "dark-blue", "green"

theme_manager = ThemeManager()