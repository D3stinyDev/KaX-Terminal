# KaX Terminal Enhanced

## Overview
**KaX Terminal Enhanced** is a modern, extensible terminal application built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) and Tkinter. It features a polished graphical interface, modular command system, dynamic module loading, and interactive utilities like a notepad and a customizable ball physics simulation game.

---

## Features

- **Modern UI**: CustomTkinter-powered sidebar, theming, and custom widgets.
- **Command Execution**: Modular command handler with aliases and error handling.
- **Command History**: Navigate previous/next commands with arrow keys.
- **Dynamic Modules**: Easily add new features and interfaces.
- **Custom Widgets**: Enhanced entry and display widgets for better usability.
- **Theming**: Switch between dark, light, and custom color themes.
- **Logo & Branding**: Custom logo and branding in the UI.
- **Integrated Utilities**:
  - **Notepad**: Simple text editor interface.
  - **Ball Physics Game**: Highly customizable physics simulation with sidebar settings.
- **Settings & Customization**:
  - Ball radius, color, outline, opacity, initial velocity, gravity, bounce factor, simulation speed, circle size, circle outline, background color, random color, pause/resume.
- **Error Handling**: Friendly error messages and robust input validation.
- **Extensible Structure**: Add new commands, modules, and interfaces with ease.

---

## Project Structure

```
KaX-Terminal-Enhanced
├── src
│   ├── main.py                # Main application entry point
│   ├── ui
│   │   ├── custom_widgets.py   # Custom widget classes
│   │   └── themes.py           # Theme definitions and manager
│   ├── logic
│   │   ├── commands.py         # Command handler and implementations
│   │   └── history.py          # Command history management
│   └── utils
│       └── helpers.py          # Utility functions
├── assets
│   ├── KaX_Terminal_BlackBG_WhiteTxt.png  # Logo image
│   └── Interfaces
│       ├── notepad
│       │   └── notepad.py      # Notepad interface
│       └── ballSimulationGame
│           └── ballPhysGame.py  # Ball physics simulation game
├── config
│   └── modules
│       └── sample_module.py     # Example module
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   ```
2. **Navigate to the project directory:**
   ```sh
   cd KaX-Terminal-Enhanced
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the application:**
   ```sh
   python src/main.py
   ```
2. **Terminal Commands:**
   - `clear`, `cls` — Clear the terminal display.
   - `exit`, `quit` — Close the terminal.
   - `help`, `h`, `hlp`, `hl`, `hel`, `helpme` — Show help and available commands.
   - `notepad` — Open the notepad interface.
   - `ballgame`, `ball`, `game`, `ballPhysicsGame` — Launch the ball physics simulation game.
   - `echo <message>` — Display a message.
   - `version` — Show terminal version.
   - `resources` — Display system resource usage.
   - *Add your own commands via `src/logic/commands.py`!*

---

## Ball Physics Game

**Launch via terminal command:**  
`ballgame` or `ballPhysicsGame`

**Features:**
- Place balls with left-click inside the circle.
- Drag balls with right mouse button.
- Balls bounce and collide with each other.
- Sidebar settings:
  - Ball radius, color, outline, opacity
  - Initial velocity (X/Y)
  - Gravity, bounce factor
  - Simulation speed
  - Circle size, outline thickness
  - Background color
  - Random color toggle
  - Pause/resume simulation

---

## Customization

- **Themes:**  
  Change appearance mode and color theme in `src/ui/themes.py`.
- **Add Commands:**  
  Extend `src/logic/commands.py` for new commands.
- **Add Modules/Interfaces:**  
  Place new modules in `assets/Interfaces/` and load them dynamically.
- **UI Widgets:**  
  Customize or extend widgets in `src/ui/custom_widgets.py`.

---

## Documentation

### Adding a New Command

1. Open `src/logic/commands.py`.
2. Add your command to the `commands_list` dictionary.
3. Implement its logic in `execute_command`.

### Extending the Ball Physics Game

- Add new settings to the sidebar in `ballPhysGame.py`.
- Use sliders, entries, checkboxes, and buttons for user input.
- Update ball or simulation logic as needed.

### Error Handling

- Use `display_error` and `display_message` methods in `main.py` for user feedback.

---

## Credits

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)