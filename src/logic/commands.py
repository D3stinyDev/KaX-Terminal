from customtkinter import CTkTextbox, CTkEntry
import os
import psutil
import random
from datetime import datetime
import time

class CommandHandler:
    def __init__(self, terminal):
        self.terminal = terminal
        self.commands_list = {
            "clear": "Clear the terminal display",
            "exit, quit": "Close the terminal",
            "help, h, hlp, hl, hel, helpme": "Show this help message",
            "notepad": "Open the notepad interface",
            "ballgame, ball, game": "Start the ball simulation game",
        }

    def execute_command(self, command):
        cmd = command.lower().strip()
        if cmd in ["clear"]:
            self.terminal.clear_display()
        elif cmd in ["exit", "quit"]:
            self.terminal.quit()
        elif cmd in ["help", "h", "hlp", "hl", "hel", "helpme"]:
            self.show_help()
        elif cmd == "notepad":
            self.open_notepad()
        elif cmd in ["ballgame", "ball", "game"]:
            self.open_ball_game()
        else:
            self.terminal.display_message(f"Command '{command}' not found.")

    def show_help(self):
        help_text = "KaX Terminal Help:\n"
        for cmd, desc in self.commands_list.items():
            help_text += f"  {cmd:<25} - {desc}\n"
        self.terminal.display_message(help_text)

    def open_notepad(self):
        os.system(f'python "{os.path.join(self.terminal.base_dir, "assets/Interfaces/notepad/notepad.py")}"')

    def open_ball_game(self):
        import os
        game_path = os.path.abspath(
            os.path.join(self.terminal.base_dir, "..", "assets", "Interfaces", "ballSimulationGame", "ballPhysGame.py")
        )
        if os.path.exists(game_path):
            os.system(f'python "{game_path}"')
        else:
            self.terminal.display_error("Ball simulation game not found.")