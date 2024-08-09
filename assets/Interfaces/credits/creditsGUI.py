import tkinter as tk

class CreditsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Credits")

        # Set the window size and prevent resizing
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        # Create a frame for the content
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Add a label to display the credits
        self.credits_label = tk.Label(
            self.frame, 
            text="Founder - D3stinyDev:\n Discord: d3stinydev\n",  # Replace "Your Name" with the actual developer's name
            font=("Arial", 14),
            padx=20, pady=20
        )
        self.credits_label.pack()

        # Add a button to close the GUI
        self.close_button = tk.Button(
            self.frame, 
            text="Close", 
            command=self.root.quit
        )
        self.close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CreditsGUI(root)
    root.mainloop()
