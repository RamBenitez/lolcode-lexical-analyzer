# interpreter_screen.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InterpreterScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter") #window title
        self.root.geometry("1200x800") #Size
        self.root.configure(bg="#145da0") 

        # menu bar
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=0) #create file dropdown menu
        file_menu.add_command(label="Open File", command=self.open_file)# open file
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=file_menu) #attach file menu to menu bar
        self.root.config(menu=menu)

        # main window
        main_pane = tk.PanedWindow(
            self.root, 
            orient=tk.HORIZONTAL, 
            sashrelief=tk.RAISED, 
            sashwidth=4
        )
        main_pane.pack(
            fill=tk.BOTH, 
            expand=True, 
            padx=10, 
            pady=10
        )
        # editor
        editor_frame = tk.Frame(main_pane, bg="#8cbcff")
        main_pane.add(editor_frame, stretch="always")

        editor_label = tk.Label(
            editor_frame,
            text="LOLCode Editor",
            font=("Arial", 13, "bold"),
            bg="#8cbcff",
            fg="#0D47A1"
        )
        editor_label.pack(pady=5)

        #editor text size
        self.editor = tk.Text(
            editor_frame,
            height=25,
            width=80,
            wrap="word",
            bg="#FFFFFF",
            fg="#000000",
            font=("Consolas", 11)
        )
        self.editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # tables
        tables_frame = tk.Frame(main_pane, bg="#E3F2FD")
        main_pane.add(tables_frame, stretch="always")

        #token table styling
        token_label = tk.Label(
            tables_frame,
            text="Tokens",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        token_label.pack(pady=(10, 5))
        # token table titles and columns
        self.token_table = ttk.Treeview(
            tables_frame,
            columns=("Lexeme", "Type"),
            show="headings",
            height=12
        )
        self.token_table.heading("Lexeme", text="Lexeme")
        self.token_table.heading("Type", text="Type")
        self.token_table.column("Lexeme", width=150, anchor="center")
        self.token_table.column("Type", width=120, anchor="center")
        self.token_table.pack(padx=20, pady=5, fill=tk.BOTH)

        # symbol table
        symbol_label = tk.Label(
            tables_frame,
            text="Symbol Table",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        symbol_label.pack(pady=(15, 5))

        self.symbol_table = ttk.Treeview(
            tables_frame,
            columns=("Variable", "Value"),
            show="headings",
            height=10
        )
        self.symbol_table.heading("Variable", text="Variable")
        self.symbol_table.heading("Value", text="Value")
        self.symbol_table.column("Variable", width=150, anchor="center")
        self.symbol_table.column("Value", width=120, anchor="center")
        self.symbol_table.pack(padx=20, pady=5, fill=tk.BOTH)

        # run execution button
        self.run_button = ttk.Button(
            self.root,
            text="Run / Execute Code",
            command=self.run_code
        )
        self.run_button.pack(pady=10, ipadx=10, ipady=5)

        # Console output
        console_frame = tk.Frame(root, bg="#E3F2FD")
        console_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        console_label = tk.Label(
            console_frame,
            text="Console Output",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        console_label.pack()

        self.console = tk.Text(
            console_frame,
            height=10,
            width=130,
            bg="#212121",
            fg="#00FF00",
            insertbackground="white",
            font=("Consolas", 11)
        )
        self.console.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # input
        input_frame = tk.Frame(root, bg="#E3F2FD")
        input_frame.pack(pady=(0, 20))

        input_label = tk.Label(
            input_frame,
            text="Program Input:",
            font=("Arial", 10, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        input_label.pack(side="left", padx=5)

        self.input_entry = tk.Entry(input_frame, width=60)
        self.input_entry.pack(side="left", padx=5)

        submit_input = ttk.Button(input_frame, text="Submit", command=self.submit_input)
        submit_input.pack(side="left", padx=5)

    # file handling
    def open_file(self):
        #open the dialog box for the lolcode files
        file_path = filedialog.askopenfilename(filetypes=[("LOLCode Files", "*.lol")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
            self.editor.delete("1.0", tk.END) #clear the editor content
            self.editor.insert("1.0", code)
            self.console.insert(tk.END, f"Loaded file: {file_path}\n")

    def save_file(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".lol",
            filetypes=[("LOLCode Files", "*.lol"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                code = self.editor.get("1.0", tk.END)
                file.write(code)
            self.console.insert(tk.END, f"Saved file: {file_path}\n")

    # execution
    def run_code(self):
        code = self.editor.get("1.0", tk.END).strip()

        if not code: #if editor is empty
            messagebox.showwarning("No Code", "Please write or load LOLCode to execute.")
            return
        self.console.insert(tk.END, "\n Running LOLCode...\n")

        # in progrss, backend execution
        self.console.insert(tk.END, " Execution completed.\n")

    # table update helper
    def update_tokens(self, tokens):
        #clear old tokens
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        #insert new tokens
        for lexeme, tok_type in tokens:
            self.token_table.insert("", "end", values=(lexeme, tok_type))

    def update_symbols(self, symbols):
        #clear old symbols
        for item in self.symbol_table.get_children():
            self.symbol_table.delete(item)
        #inser symbols
        for var, val in symbols:
            self.symbol_table.insert("", "end", values=(var, val))

    def submit_input(self):
        user_input = self.input_entry.get().strip()
        if user_input:
            self.console.insert(tk.END, f"User Input: {user_input}\n")
            self.input_entry.delete(0, tk.END)
