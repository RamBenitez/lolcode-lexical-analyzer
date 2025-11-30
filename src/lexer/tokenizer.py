# main lexical analysis algorithm reads code line by line and matches regex patterns
import re
from .token_types import TOKEN_SPECIFICATION 
from utils.file_reader import readLines

class Token:
    def __init__(self, type, lexeme, value=None, line=0):
        self.type = type
        self.lexeme = lexeme
        self.value = value
        self.line = line
    
    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, '{self.lexeme}', {self.value})"
        return f"Token({self.type}, '{self.lexeme}')"

class LexicalAnalyzer:
    # tokenizes LOLCODE by matching regex patterns
    def __init__(self):
        # compile all token patterns from TOKEN_SPECIFICATION
        self.token_patterns = [(t, re.compile(p)) for t, p in TOKEN_SPECIFICATION]
    
    def tokenize(self, lines):
        # reads each line and identifies tokens using pattern matching
        # returns a tuple of tokens and errors
        tokens, errors = [], []
        
        multi_line_comment = False

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            # Check for OBTW - must be on its own line (possibly with trailing comment)
            if stripped.startswith('OBTW'):
                # OBTW can have trailing content (treated as comment), but cannot have statements before it
                # Check if OBTW is at beginning of stripped line
                after_obtw = stripped[4:].strip()
                # If there's anything after OBTW that's not a comment, that's still allowed per spec
                # "OBTW and TLDR must have their own lines (which may include some comments but not other statements)"
                multi_line_comment = True
                continue
            
            # Check for TLDR - must be on its own line
            if stripped.startswith('TLDR'):
                if not multi_line_comment:
                    errors.append(f"Error at line {line_num}: TLDR without matching OBTW")
                    continue
                # Check if there's content after TLDR that would be a statement
                after_tldr = stripped[4:].strip()
                if after_tldr and not after_tldr.startswith('BTW'):
                    errors.append(f"Error at line {line_num}: TLDR must be on its own line")
                    continue
                multi_line_comment = False
                continue 
                
            # Skip lines inside multi-line comments
            if multi_line_comment:
                continue
            
            # Check if OBTW or TLDR appears in the middle of a line (not allowed)
            if 'OBTW' in line and not stripped.startswith('OBTW'):
                errors.append(f"Error at line {line_num}: OBTW must be at the start of its own line")
                continue
            if 'TLDR' in line and not stripped.startswith('TLDR'):
                errors.append(f"Error at line {line_num}: TLDR must be at the start of its own line") 

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
                    
                    # If we encounter BTW, it's a single-line comment - skip rest of line
                    if best_type == 'BTW':
                        break  # Stop processing this line
                    
                    if best_type != 'WHITESPACE':
                        tokens.append(self._make(best_type, lexeme, line_num))
                    pos = best.end()
                else:
                    errors.append(f"Error at line {line_num}, pos {pos}: '{line[pos]}'")
                    pos += 1
            
            #Allows parser to recognize linebreaks 
            tokens.append(Token(type='LINEBREAK', lexeme='\\n', value=None, line=line_num))
            
        return tokens, errors
    
    def nameType(self, token_type):
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
            return "Variable Assignment"
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
        elif token_type == "LINEBREAK":
            return "Linebreak"
        elif token_type in ("O RLY?", "YA RLY", "NO WAI", "OIC"):
            return "If-Then Statement"
        else:
            # Fallback for any unclassified tokens
            return token_type
    
    def _make(self, token_type, lexeme, line):
        # creates a token and converts literals to their actual values
        value = None
        
        if token_type == 'NUMBR Literal':
            value = int(lexeme)
        elif token_type == 'NUMBAR Literal':
            value = float(lexeme)
        elif token_type == 'YARN Literal':
            value = lexeme[1:-1]  # Remove quotes
        elif token_type == 'TROOF Literal':
            value = (lexeme == 'WIN')
        elif token_type == 'IDENTIFIER':
            value = lexeme  # Store identifier name as value
        elif token_type == 'TYPE Literal':
            value = lexeme  # Store type name as value

        return Token(token_type, lexeme, value, line)