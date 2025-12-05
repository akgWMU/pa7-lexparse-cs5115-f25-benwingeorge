# main.py
"""
Main entry point for PA7.

Usage:
    python main.py --lex examples/example1.sml
    python main.py --parse examples/example1.sml
"""

import sys
from typing import List, Tuple

from lexer import tokenize_file
from parser import parse_file
from ast_nodes import level_order_string


def print_token_list(tokens: List[Tuple[str, object]]) -> None:
    """
    Print tokens in a conceptual (TYPE, VALUE) style.

    You can tweak this to exactly match assignment examples,
    e.g. mapping PLY internal types to KEYWORD / IDENTIFIER / CONSTANT etc.
    """
    result = []
    for tok_type, tok_val in tokens:
        if tok_type in {"INTEGER", "FLOAT", "PROGRAM", "VAR", "BEGIN", "END",
                        "IF", "THEN", "ELSE", "WHILE", "DO", "READ", "WRITE",
                        "AND", "OR", "NOT", "ARRAY"}:
            category = "KEYWORD"
        elif tok_type in {"IDENTIFIER"}:
            category = "IDENTIFIER"
        elif tok_type in {"INTNUM", "FLOATNUM", "STRING"}:
            category = "CONSTANT"
        elif tok_type in {"PLUS", "MINUS", "TIMES", "DIVIDE"}:
            category = "ARITH-OP"
        elif tok_type in {"LT", "LE", "GT", "GE", "EQ", "NE"}:
            category = "LOGIC-OP"
        elif tok_type in {"LPAREN", "RPAREN", "LBRACKET", "RBRACKET",
                          "COMMA", "SEMI", "COLON", "DOT"}:
            category = "SEPARATOR"
        elif tok_type in {"ASSIGN"}:
            category = "ARITH-OP"  # or "ASSIGN" if you want a separate category
        else:
            category = tok_type  # fallback

        result.append((category, tok_val))

    print(result)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("--lex", "--parse"):
        print("Usage:")
        print("  python main.py --lex <source-file>")
        print("  python main.py --parse <source-file>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if mode == "--lex":
        tokens = tokenize_file(filename)
        print_token_list(tokens)
    else:
        ast_root = parse_file(filename)
        if ast_root is not None:
            # Required level-order traversal format
            print(level_order_string(ast_root))


if __name__ == "__main__":
    main()