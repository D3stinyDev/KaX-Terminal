import customtkinter as ctk

def modify_terminal(terminal):
    terminal.terminal_display.configure(state='normal')
    terminal.terminal_display.insert(ctk.END, "Sample Module Loaded Successfully!\n")
    terminal.terminal_display.configure(state='disabled')

    # Example command registration
    terminal.command_registry["sample_command"] = sample_command

def sample_command(terminal):
    terminal.terminal_display.configure(state='normal')
    terminal.terminal_display.insert(ctk.END, "This is a response from the sample command!\n")
    terminal.terminal_display.configure(state='disabled')