# PA7 – Lexical Analyzer and Parser for SomeWMULife
**Course:** CS 5115 – Fall 2025  
**Student:** Benwin George  

---

## 1. Introduction

Briefly describe the goal of this assignment:
- Implement a lexical analyzer using PLY.
- Implement a parser that builds an AST for SomeWMULife programs.
- Produce a level-order traversal of the parse tree.

---

## 2. Design Choices

### 2.1 Lexer Design
- How you handled:
  - Keywords vs identifiers
  - Integers, floats, scientific notation
  - String constants
  - Comments `{ ... }`
- Any assumptions or simplifications.

### 2.2 Parser & Grammar Design
- How you translated the BNF grammar into PLY rules.
- Any left-recursion / ambiguity considerations.
- Structure of your AST nodes (what `kind` and `value` represent).

### 2.3 AST Representation
- Structure of `ASTNode`.
- Encoding of different constructs:
  - Program, declarations, assignments, if/while, expressions, I/O, arrays.

---

## 3. Implementation Details

### 3.1 File Overview
- `lexer.py` – lexical analyzer
- `parser.py` – parser and AST builder
- `ast_nodes.py` – AST structure and traversal
- `main.py` – driver program
- Any helper files or scripts

### 3.2 Error Handling
- Illegal characters in the lexer
- Syntax errors in the parser (`p_error` function)
- How errors are reported to the user

---

## 4. Testing

### 4.1 Test Inputs
List the sample SomeWMULife programs you used (e.g., `example1.sml`) and what they are intended to test.

### 4.2 Sample Output – Tokens
Show an example token list for a short program and explain.

### 4.3 Sample Output – Parse Tree
Show the level-order traversal output for at least one input program.

---

## 5. Limitations and Possible Extensions

- Any known limitations (e.g., partial support for floats, arrays, or comments).
- Ideas for future work (type checking, code generation, etc.).

---

## 6. Conclusion

Short summary of what you learned and what the tool can do.