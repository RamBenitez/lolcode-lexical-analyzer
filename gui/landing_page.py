import tkinter as tk
from tkinter import ttk
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

        #Style for the button
        style = ttk.Style()
        style.configure(
            "Blue.TButton",
            font=("Helvetica", 16, "bold"),
            padding=15,
            background="#0078D7",  # blue
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor="none"
        )
        #for hover effect
        style.map(
            "Blue.TButton",
            background=[("active", "#005A9E")],  # darker blue when hovered
            foreground=[("active", "white")]
        )
        #start button
        self.start_button = ttk.Button(
            root,
            text="Start",
            style="Blue.TButton",
            command=self.on_start_click
        )
        self.start_button.pack(pady=50, ipadx=20, ipady=10)

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
