import sys
import os

# Add the "src" directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from parser.symbol_table import SymbolTable


def test_symbol_table():
    table = SymbolTable()
    
    # Declare variables
    table.declare("num", 17)
    table.declare("name", "seventeen")
    table.declare("flag", True)
    
    # Update variable
    table.assign("num", 20)
    
    # Retrieve variable
    print("num =", table.get("num"))
    print("name =", table.get("name"))
    print("flag =", table.get("flag"))
    
    # Print full table
    print(table)

if __name__ == "__main__":
    test_symbol_table()
