# src/parser/symbol_table.py

# symboltable class is used to store and manage variables during parsing

class SymbolTable:
    def __init__(self):
        # initialize dictionayr to hold the values
        self.symbols = {}
    
    #declare variable in the table
    def declare(self, name, value):
        if name in self.symbols:
            raise Exception(f"Variable '{name}' already declared.")
        self.symbols[name] = value
    
    # retrive the value of the declared variale
    def lookup(self, name):
        #check if the variable exist
        if name not in self.symbols:
            raise Exception(f"Variable '{name}' not declared.")
        #return the value of the variable
        return self.symbols[name]
    
    #update the value of an existing variablee
    def update(self, name, value):
        #check if it exist
        if name not in self.symbols:
            raise Exception(f"Variable '{name}' not declared.")
        self.symbols[name] = value
    
    #string representation of the table
    def __repr__(self):
        return f"SymbolTable({self.symbols})"
