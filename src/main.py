# main program to test the LOLCODE Lexical Analyzer

from lexer.tokenizer import LexicalAnalyzer
from utils.file_reader import readLines
from parser.parser import Parser
from interpreter.interpreter import Interpreter


def main():
    file_path = "../tests/testcase.lol"
    
    try:
        # Lexical Analysis
        lines = readLines(file_path)
        analyzer = LexicalAnalyzer()
        tokens, errors = analyzer.tokenize(lines)
        
        if errors:
            print("Lexical Errors:")
            for error in errors:
                print(f"  {error}")
            return
        
        # Display Tokens
        print("=" * 60)
        print("TOKENS")
        print("=" * 60)
        print(f"Token Count: {len(tokens)}\n")
        print(f"{'Lexeme':<20} {'Classification':<30}")
        print("-" * 60)
        for token in tokens:
            print(f"{token.lexeme:<20} {analyzer.nameType(token.type):<30}")
        print()
    
        # Syntax Analysis
        token_dicts = [{'type': t.type, 'value': t.lexeme} for t in tokens]
        parser = Parser(token_dicts)
        ast = parser.parse()
        
        # Display Parse Tree
        print("=" * 60)
        print("PARSE TREE")
        print("=" * 60)
        print(ast)
        
        # Semantic Analysis & Execution
        interpreter = Interpreter(ast, parser.symbol_table)
        output = interpreter.execute()
        
        # Display Symbol Table (after execution with actual values)
        print("=" * 60)
        print("SYMBOL TABLE")
        print("=" * 60)
        print(f"{'Identifier':<20} {'Value':<30}")
        print("-" * 60)
        for var, value in parser.symbol_table.symbols.items():
            print(f"{var:<20} {str(value):<30}")
        print()
        
        # Display Execution Output
        print("=" * 60)
        print("EXECUTION OUTPUT")
        print("=" * 60)
        for line in output:
            print(line)

    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()