# Impact Analysis: Treating Quotation Marks as Separate Tokens

## Current Behavior
`"noot noot"` → 1 token
- Type: YARN Literal
- Lexeme: "noot noot"
- Value: noot noot (quotes stripped)

## Proposed Behavior
`"noot noot"` → 3 tokens
- Token 1: Type: ", Lexeme: "
- Token 2: Type: STRING_CONTENT, Lexeme: noot noot
- Token 3: Type: ", Lexeme: "

---

## CHANGES REQUIRED

### 1. TOKEN_SPECIFICATION (token_types.py)
**Change Level: SMALL**

BEFORE:
```python
('YARN Literal', r'"[^"]*"'),
```

AFTER:
```python
('"', r'"'),  # Must be BEFORE IDENTIFIER to match first
('STRING_CONTENT', r'[^"\s]+'),  # Content between quotes (simplified)
# OR keep YARN Literal but add quote token
```

**Issue**: Order matters! The quote pattern must come before other patterns.

---

### 2. TOKENIZER (tokenizer.py)
**Change Level: MEDIUM**

Changes needed in `_make()` method:

BEFORE:
```python
elif token_type == 'YARN Literal':
    value = lexeme[1:-1]  # Remove quotes
```

AFTER:
If keeping YARN Literal + adding quotes:
```python
elif token_type == 'YARN Literal':
    value = lexeme[1:-1]  # Remove quotes (still works)
elif token_type == '"':
    value = None  # Quote has no value
```

OR if splitting completely:
```python
elif token_type == 'STRING_CONTENT':
    value = lexeme  # No quote removal needed
elif token_type == '"':
    value = None
```

**Issue**: Need to handle state - are we inside or outside a string?

---

### 3. PARSER (parser.py) 
**Change Level: LARGE** ⚠️

Current `parse_literal()`:
```python
elif token['type'] == 'YARN Literal':
    yarn_value = self.match('YARN Literal')['value']
    return Node('literal_yarn', value=yarn_value[1:-1])
```

NEW parse method needed:
```python
elif token['type'] == '"':
    return self.parse_string_literal()

def parse_string_literal(self):
    self.match('"')  # Opening quote
    content_parts = []
    
    # Collect all content until closing quote
    while self.current_token() and self.current_token()['type'] != '"':
        if self.current_token()['type'] == 'STRING_CONTENT':
            content_parts.append(self.current_token()['value'])
            self.advance()
        elif self.current_token()['type'] == 'IDENTIFIER':
            # Inside quotes, identifiers are just strings
            content_parts.append(self.current_token()['value'])
            self.advance()
        else:
            break
    
    self.match('"')  # Closing quote
    content = ' '.join(content_parts)
    return Node('literal_yarn', value=content)
```

**Issues**:
- Much more complex string parsing
- Need to handle spaces, special chars inside strings
- What if quote is missing? Error handling gets harder
- Multi-word strings become multiple tokens to reassemble

---

### 4. TOKENIZER STATE MACHINE
**Change Level: LARGE** ⚠️

Current tokenizer is **stateless** - each character position is independent.

With separate quotes, you need **state tracking**:
```python
def tokenize(self, lines):
    tokens, errors = [], []
    inside_string = False  # NEW STATE
    
    for line_num, line in enumerate(lines, start=1):
        pos = 0
        
        while pos < len(line):
            if line[pos] == '"':
                # Toggle string state
                inside_string = not inside_string
                tokens.append(Token('"', '"', None, line_num))
                pos += 1
            elif inside_string:
                # Collect string content
                content = ""
                while pos < len(line) and line[pos] != '"':
                    content += line[pos]
                    pos += 1
                if content:
                    tokens.append(Token('STRING_CONTENT', content, content, line_num))
            else:
                # Normal tokenization
                ...
```

**Issues**:
- Complete rewrite of tokenization logic
- Harder to maintain
- More bugs possible
- String can't span multiple lines (current LOLCODE)

---

## SUMMARY OF CHANGES

| Component | Complexity | Lines Changed | Risk |
|-----------|-----------|---------------|------|
| token_types.py | LOW | ~5 lines | LOW |
| tokenizer.py | HIGH | ~50-100 lines | HIGH |
| parser.py | MEDIUM | ~20-30 lines | MEDIUM |
| GUI | NONE | 0 lines | NONE |
| Tests | HIGH | Need new tests | MEDIUM |

**Total Effort**: 2-4 hours of work
**Bug Risk**: HIGH (string handling is error-prone)
**Benefit**: Mostly cosmetic (shows quotes separately in token table)

---

## RECOMMENDATION

❌ **NOT RECOMMENDED** unless you have a specific requirement

**Reasons**:
1. Current implementation works correctly
2. Matches standard LOLCODE tokenization
3. Parser already handles YARN Literals properly
4. Separating quotes adds complexity for minimal benefit
5. More potential for bugs (unclosed strings, special chars, etc.)

**When it WOULD make sense**:
- If your language spec explicitly requires it
- If you need to support escape sequences (\n, \", etc.)
- If you need different string types (single vs double quotes)
- If strings can contain embedded expressions

---

## ALTERNATIVE: Keep current + show differently in GUI

If you just want the GUI to DISPLAY quotes separately, you could:

```python
# In GUI, when displaying tokens:
for token in tokens:
    if token.type == 'YARN Literal':
        # Show as 3 rows in the table
        self.token_table.insert("", "end", values=('"', "String Delimiter"))
        self.token_table.insert("", "end", values=(token.value, "String Content"))
        self.token_table.insert("", "end", values=('"', "String Delimiter"))
    else:
        display_type = analyzer.nameType(token.type)
        self.token_table.insert("", "end", values=(token.lexeme, display_type))
```

This gives you the visual separation without changing the tokenizer or parser!
