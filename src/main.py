# main program to test the LOLCODE Lexical Analyzer

from lexer.tokenizer import LexicalAnalyzer
from utils.file_reader import readLines
from parser.parser import Parser 


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
            display_type = analyzer.nameType(token.type)
            print(f"{token.line:<6} {display_type:<40} {token.lexeme:<20}")
        
        if errors:
            print("\nErrors found:")
            for error in errors:
                print(f"  {error}")
    
        #parser function - parse the tokens and prints the Abstract Syntax Tree
        try:
            token_dicts = [{'type': t.type, 'value': t.lexeme} for t in tokens]
            parser = Parser(token_dicts)
            ast = parser.parse()
            
            print("\nAbstract Syntax Tree")
            print(ast) 

        except SyntaxError as e:
            print(f"Error: {e}")

    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
