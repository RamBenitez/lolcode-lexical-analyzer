# main lexical analysis algorithm reads code line by line and matches regex patterns
import re
from lexer.token_types import TOKEN_SPECIFICATION
from utils.file_reader import readLines

class Token:
    # single token with its type, lexeme, value, and line number.
    def __init__(self, type, lexeme, value=None, line=0):
        self.type = type
        self.lexeme = lexeme
        self.value = value
        self.line = line
    
    def __repr__(self):
        if self.value is not None:
            return f"{self.type}, '{self.lexeme}', {self.value})"
        return f"{self.type}, '{self.lexeme}')"

class LexicalAnalyzer:
    # tokenizes LOLCODE by matching regex patterns
    def __init__(self):
        # compile all token patterns from TOKEN_SPECIFICATION
        self.token_patterns = [(t, re.compile(p)) for t, p in TOKEN_SPECIFICATION]
    
    def tokenize(self, lines):
        # reads each line and identifies tokens using pattern matching
        # returns a tuple of tokens and errors
        tokens, errors = [], []
        
        for line_num, line in enumerate(lines, start=1):
            pos = 0
            
            while pos < len(line):
                best, best_type = None, None
                
                # try each pattern and keep the longest match
                for token_type, pattern in self.token_patterns:
                    m = pattern.match(line, pos)
                    if m and (best is None or len(m.group(0)) > len(best.group(0))):
                        best, best_type = m, token_type
                
                if best:
                    lexeme = best.group(0)
                    if best_type != 'WHITESPACE':
                        tokens.append(self._make(best_type, lexeme, line_num))
                    pos = best.end()
                else:
                    errors.append(f"Error at line {line_num}, pos {pos}: '{line[pos]}'")
                    pos += 1
        
        return tokens, errors
    
    def nameType (self, token_type):
        if token_type in ("HAI", "KTHXBYE"):
            return "Code Delimiter"
        elif token_type == "WAZZUP":
            return "Variable List Delimiter"
        elif token_type == "BUHBYE":
            return "Variable List Terminator"
        elif token_type == "I HAS A":
            return "Variable Declaration"
        elif token_type == "IDENTIFIER":
            return "Variable Identifier"
        elif token_type == "ITZ":
            return "Variable Assignment (following I HAS A)"
        elif token_type == "NUMBR Literal":
            return "Integer Literal"
        elif token_type == "NUMBAR Literal":
            return "Float Literal"
        elif token_type == "YARN Literal":
            return "String Literal"
        elif token_type == "TROOF Literal":
            return "Boolean Value (True/False)"
        elif token_type in ("SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF"):
            return "Arithmetic Operator"
        elif token_type in ("BIGGR OF", "SMALLR OF"):
            return "Comparison Operator"
        elif token_type == "VISIBLE":
            return "Output Keyword"
        elif token_type == "AN":
            return "Conjunction"
        elif token_type == "BTW":
            return "Comment Keyword"
        elif token_type == '"':
            return "String Delimiter"
        else:
            # fallback for any unclassified tokens
            return token_type
    
    def _make(self, token_type, lexeme, line):
        # creates a token and converts literals to their actual values
        value = None
        
        if token_type == 'NUMBR Literal':
            value = int(lexeme)
        elif token_type == 'NUMBAR Literal':
            value = float(lexeme)
        elif token_type == 'YARN Literal':
            value = lexeme[1:-1]  # remove quotes
        elif token_type == 'TROOF Literal':
            value = (lexeme == 'WIN')

        types = self.nameType(token_type)
        return Token(types, lexeme, value, line)