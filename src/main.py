# main program to test the LOLCODE Lexical Analyzer

from lexer.tokenizer import LexicalAnalyzer
from utils.file_reader import readLines


def main():
    file_path = "../tests/testcase.lol"
    
    try:
        # read the file and tokenize
        lines = readLines(file_path)
        analyzer = LexicalAnalyzer()
        tokens, errors = analyzer.tokenize(lines)
        
        # display results
        print(f"Total Tokens: {len(tokens)}")
        print(f"Total Errors: {len(errors)}\n")
        
        # print tokens in a table
        print(f"{'LINE':<6} {'TYPE':<20} {'LEXEME':<15} {'VALUE'}")
        print("-" * 60)
        
        for token in tokens:
            value = token.value if token.value is not None else ""
            print(f"{token.line:<6} {token.type:<20} {token.lexeme:<15} {value}")
        
        if errors:
            print("\nErrors found:")
            for error in errors:
                print(f"  {error}")
        
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
