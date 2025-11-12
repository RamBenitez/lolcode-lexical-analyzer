# interpreter_screen.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os

# Add the src directory to the path so we can import the lexer and parser
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer.tokenizer import LexicalAnalyzer
from parser.parser import Parser
from parser.symbol_table import SymbolTable
from interpreter.interpreter import Interpreter

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

        # Main container with grid layout
        main_container = tk.Frame(self.root, bg="#145da0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_rowconfigure(0, weight=3)  # Top section (editor + tables)
        main_container.grid_rowconfigure(1, weight=0)  # Button
        main_container.grid_rowconfigure(2, weight=1)  # Console
        main_container.grid_rowconfigure(3, weight=0)  # Input
        main_container.grid_columnconfigure(0, weight=1)

        # Top section with PanedWindow for editor and tables
        top_pane = tk.PanedWindow(
            main_container, 
            orient=tk.HORIZONTAL, 
            sashrelief=tk.RAISED, 
            sashwidth=4,
            bg="#145da0"
        )
        top_pane.grid(row=0, column=0, sticky="nsew")

        # Editor section
        editor_frame = tk.Frame(top_pane, bg="#8cbcff", width=500)
        top_pane.add(editor_frame, minsize=300, stretch="always")

        editor_label = tk.Label(
            editor_frame,
            text="LOLCode Editor",
            font=("Arial", 13, "bold"),
            bg="#8cbcff",
            fg="#0D47A1"
        )
        editor_label.pack(pady=5)

        # Editor text
        self.editor = tk.Text(
            editor_frame,
            wrap="word",
            bg="#FFFFFF",
            fg="#000000",
            font=("Consolas", 11)
        )
        self.editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Tables section
        tables_frame = tk.Frame(top_pane, bg="#E3F2FD", width=400)
        top_pane.add(tables_frame, minsize=300, stretch="always")

        # Token table section
        token_label = tk.Label(
            tables_frame,
            text="Tokens",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        token_label.pack(pady=(5, 2))
        
        # Frame for token table with scrollbar
        token_frame = tk.Frame(tables_frame, bg="#E3F2FD")
        token_frame.pack(padx=10, pady=2, fill=tk.BOTH, expand=True)
        
        # token table
        self.token_table = ttk.Treeview(
            token_frame,
            columns=("Lexeme", "Type"),
            show="headings",
            height=10
        )
        self.token_table.heading("Lexeme", text="Lexeme")
        self.token_table.heading("Type", text="Type")
        self.token_table.column("Lexeme", width=120, anchor="w")
        self.token_table.column("Type", width=180, anchor="w")
        
        # Add scrollbar to token table
        token_scrollbar = ttk.Scrollbar(token_frame, orient="vertical", command=self.token_table.yview)
        self.token_table.configure(yscrollcommand=token_scrollbar.set)
        
        self.token_table.pack(side="left", fill=tk.BOTH, expand=True)
        token_scrollbar.pack(side="right", fill="y")

        # Symbol table section
        symbol_label = tk.Label(
            tables_frame,
            text="Symbol Table",
            font=("Arial", 11, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        )
        symbol_label.pack(pady=(10, 2))

        # Frame for symbol table with scrollbar
        symbol_frame = tk.Frame(tables_frame, bg="#E3F2FD")
        symbol_frame.pack(padx=10, pady=2, fill=tk.BOTH, expand=True)

        self.symbol_table = ttk.Treeview(
            symbol_frame,
            columns=("Variable", "Value"),
            show="headings",
            height=8
        )
        self.symbol_table.heading("Variable", text="Variable")
        self.symbol_table.heading("Value", text="Value")
        self.symbol_table.column("Variable", width=120, anchor="w")
        self.symbol_table.column("Value", width=180, anchor="w")
        
        # Add scrollbar to symbol table
        symbol_scrollbar = ttk.Scrollbar(symbol_frame, orient="vertical", command=self.symbol_table.yview)
        self.symbol_table.configure(yscrollcommand=symbol_scrollbar.set)
        
        self.symbol_table.pack(side="left", fill=tk.BOTH, expand=True)
        symbol_scrollbar.pack(side="right", fill="y")

        # Run button
        self.run_button = ttk.Button(
            main_container,
            text="Run / Execute Code",
            command=self.run_code
        )
        self.run_button.grid(row=1, column=0, pady=5, ipadx=10, ipady=5)

        # Console output
        console_frame = tk.Frame(main_container, bg="#E3F2FD")
        console_frame.grid(row=2, column=0, sticky="nsew", pady=5)

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
            height=8,
            bg="#212121",
            fg="#00FF00",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.console.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Input section
        input_frame = tk.Frame(main_container, bg="#E3F2FD")
        input_frame.grid(row=3, column=0, pady=(0, 5))

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
        
        self.console.delete("1.0", tk.END)  # Clear console
        self.console.insert(tk.END, "Running LOLCode...\n")
        
        try:
            # Tokenize the code
            lines = code.split('\n')
            analyzer = LexicalAnalyzer()
            tokens, errors = analyzer.tokenize(lines)
            
            # Display tokens in the token table
            token_data = []
            for token in tokens:
                display_type = analyzer.nameType(token.type)
                token_data.append((token.lexeme, display_type))
            self.update_tokens(token_data)
            
            # Display any lexical errors
            if errors:
                self.console.insert(tk.END, "\nLexical Errors:\n", "error")
                for error in errors:
                    self.console.insert(tk.END, f"  {error}\n", "error")
                return
            
            # Try to parse
            try:
                token_dicts = [{'type': t.type, 'value': t.lexeme} for t in tokens]
                parser = Parser(token_dicts)
                ast = parser.parse()
                
                self.console.insert(tk.END, "Parsing successful!\n", "success")
                
            except SyntaxError as e:
                self.console.insert(tk.END, f"\nSyntax Error: {str(e)}\n", "error")
                return
            except Exception as e:
                self.console.insert(tk.END, f"\nParser Error: {str(e)}\n", "error")
                return
            
            # Execute the code with the interpreter
            try:
                interpreter = Interpreter(ast, parser.symbol_table)
                output = interpreter.execute()
                
                # Display program output in console
                if output:
                    self.console.insert(tk.END, "\nProgram Output:\n", "success")
                    for line in output:
                        self.console.insert(tk.END, f"{line}\n")
                
                # Display symbol table with actual runtime values
                symbol_data = []
                for var_name, var_value in interpreter.symbol_table.symbols.items():
                    # Convert value to displayable string
                    if var_value is None:
                        display_value = "NOOB"
                    elif isinstance(var_value, bool):
                        display_value = "WIN" if var_value else "FAIL"
                    elif isinstance(var_value, float):
                        display_value = f"{var_value:.2f}"
                    else:
                        display_value = str(var_value)
                    
                    symbol_data.append((var_name, display_value))
                
                self.update_symbols(symbol_data)
                
                self.console.insert(tk.END, f"\nExecution completed successfully!\n", "success")
                
            except Exception as e:
                self.console.insert(tk.END, f"\nRuntime Error: {str(e)}\n", "error")
                import traceback
                error_details = traceback.format_exc()
                self.console.insert(tk.END, f"{error_details}\n", "error")
                
        except Exception as e:
            self.console.insert(tk.END, f"\nError during execution: {e}\n", "error")
            messagebox.showerror("Execution Error", str(e))
        
        # Configure text tags for colored output
        self.console.tag_config("error", foreground="#FF5555")
        self.console.tag_config("success", foreground="#00FF00")

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
