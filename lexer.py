# lexer.py
"""
PLY-based lexical analyzer for the SomeWMULife language.

Usage (quick test):
    python -m lexer examples/example1.sml
"""

import sys
import ply.lex as lex

# Reserved keywords (uppercase, case-sensitive)
reserved = {
    "AND": "AND",
    "ARRAY": "ARRAY",
    "BEGIN": "BEGIN",
    "DO": "DO",
    "ELSE": "ELSE",
    "END": "END",
    "FLOAT": "FLOAT",
    "IF": "IF",
    "INTEGER": "INTEGER",
    "NOT": "NOT",
    "OR": "OR",
    "PROGRAM": "PROGRAM",
    "READ": "READ",
    "THEN": "THEN",
    "VAR": "VAR",
    "WHILE": "WHILE",
    "WRITE": "WRITE",
}

# Token names
tokens = [
    # identifiers and constants
    "IDENTIFIER",
    "INTNUM",
    "FLOATNUM",
    "STRING",

    # operators
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
    "ASSIGN",

    # delimiters / separators
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "SEMI",
    "COLON",
    "DOT",

    # (Optional) comment token – by default we *skip* comments in parser usage.
    # "COMMENT",
] + list(reserved.values())


# Simple one-character tokens / operators
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'

t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_COMMA    = r','
t_SEMI     = r';'
t_COLON    = r':'
t_DOT      = r'\.'

# Relational operators and assignment
t_LE       = r'<='
t_GE       = r'>='
t_NE       = r'<>'
t_LT       = r'<'
t_GT       = r'>'
t_EQ       = r'='
t_ASSIGN   = r':='


# Ignored characters (spaces, tabs, newlines are handled in t_newline)
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# String constants: 'abc' (letters only, per spec)
def t_STRING(t):
    r"'[A-Za-z]*'"
    # strip surrounding quotes
    t.value = t.value[1:-1]
    return t


# Float and int constants:
# We implement a simple but usable version that handles:
#   123
#   123.45
#   123E+10
#   123.45E-10
def t_FLOATNUM(t):
    r'\d+(\.\d+)?([Ee][\+\-]?\d+)?'
    # We will treat any token with a dot or exponent as FLOATNUM
    text = t.value
    if '.' in text or 'E' in text.upper():
        t.value = float(text)
        return t
    else:
        # If it's pure digits, let INTNUM rule handle it,
        # so we tell PLY this wasn't actually a FLOATNUM.
        # (Alternatively, we could define INTNUM first and handle all here.)
        t.type = "INTNUM"
        t.value = int(text)
        return t


# Identifiers vs Keywords
def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9]*'
    upper_text = t.value.upper()
    if upper_text in reserved:
        t.type = reserved[upper_text]
        # Keep original spelling or store upper_text if you prefer
        t.value = upper_text
    return t


# Comments { ... }
# NOTE: by default we SKIP comments entirely.
def t_comment(t):
    r'\{[^}]*\}'
    # If you need COMMENT tokens for Part 1 output,
    # change this to set t.type = "COMMENT" and return t.
    # For parsing, we simply ignore them.
    pass


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def tokenize_file(filename: str):
    with open(filename, "r") as f:
        data = f.read()
    lexer.input(data)

    tokens_list = []
    for tok in lexer:
        tokens_list.append((tok.type, tok.value))
    return tokens_list


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m lexer <source-file>")
        sys.exit(1)

    toks = tokenize_file(sys.argv[1])
    for t in toks:
        print(t)