import tkinter as tk
from PIL import Image, ImageTk
import os
from interpreter_screen import InterpreterScreen

class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter - Landing Page")
        self.root.geometry("1200x800")
        self.root.configure(bg="#8cbcff")

        logo_path = os.path.join("assets", "logo1.png")
        img = Image.open(logo_path)
        img = img.resize((700, 450), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)

        logo_label = tk.Label(
            root,
            image=self.logo_img,
            bg="#8cbcff"
        )
        logo_label.pack(pady=40)

        #start button - using standard tk.Button for better cross-platform appearance
        self.start_button = tk.Button(
            root,
            text="Start",
            font=("Helvetica", 16, "bold"),
            bg="#0078D7",  # blue background
            fg="white",  # white text
            activebackground="#005A9E",  # darker blue when clicked
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            command=self.on_start_click
        )
        self.start_button.pack(pady=50, ipadx=40, ipady=15)

    def on_start_click(self):
        #starting when  clicked
        self.start_button.config(text="Starting...")
        self.root.after(1000, self.open_main_screen) 

    def open_main_screen(self):
        """Destroy landing page and open main interpreter screen"""
        self.root.destroy()  # Close landing page
        new_root = tk.Tk()   # Create new window
        InterpreterScreen(new_root)  # Initialize interpreter GUI
        new_root.mainloop()
