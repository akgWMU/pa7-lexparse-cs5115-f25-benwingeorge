# PA7 – Lexical Analyzer and Parser for SomeWMULife
**Course:** CS 5115 – Fall 2025  
**Student:** Benwin George  

---

## 1. Introduction

The goal of this assignment was to build the front end of a tiny, Pascal-like language called **SomeWMULife**.  
Specifically, I implemented:

- A **lexical analyzer** using **PLY’s `lex`** module that scans a SomeWMULife source file and produces a stream of tokens.
- A **parser** using **PLY’s `yacc`** module that consumes those tokens, checks syntax according to the language grammar, and builds an **Abstract Syntax Tree (AST)**.
- A **level-order traversal** (BFS) of the resulting parse tree/AST, printed such that:
  - each level is printed on a separate line,
  - nodes in the same level are separated by `#`,
  - and levels are separated by blank lines.

This forms the foundation of a compiler: once the AST is available, later stages (type checking, code generation, optimization) can be layered on top.

---

## 2. Design Choices

### 2.1 Lexer Design

**Keywords vs identifiers**

- I used a `reserved` dictionary that maps keyword strings such as `"PROGRAM"`, `"VAR"`, `"INTEGER"`, `"FLOAT"`, `"IF"`, `"WHILE"`, `"BEGIN"`, `"END"`, `"READ"`, `"WRITE"`, etc., to their token names.
- The `t_IDENTIFIER` rule matches:
  ```python
  r'[A-Za-z][A-Za-z0-9]*'
  ```
  and then checks if the uppercased text is in `reserved`.  
  - If it is, the token type is set to the keyword (e.g., `PROGRAM`, `IF`, `INTEGER`).
  - Otherwise, the token type remains `IDENTIFIER`.

**Integers, floats, scientific notation**

- Numerical constants are handled with a single regex in `t_FLOATNUM` that covers:
  - integers like `0`, `123`
  - floats like `123.45`
  - scientific notation like `1E10`, `3.5e-2`
- Inside the rule, I determine whether to classify the token as `INTNUM` or `FLOATNUM`.

**String constants**

- Implemented via the regex `'[A-Za-z]*'`.
- Quotes are stripped before storing the token value.

**Comments `{ ... }`**

- Implemented with a single regex rule that ignores comments:
  ```python
  r'\{[^}]*\}'
  ```

### 2.2 Parser & Grammar Design

- Grammar directly follows the BNF from the SomeWMULife spec.
- `program` is the start symbol.
- Expressions are broken into precedence layers using `expr`, `rel_expr`, `add_expr`, `mul_expr`, and `factor`.
- A shift/reduce conflict appears due to the classic dangling ELSE ambiguity; this is expected and correctly resolved by shifting.

### 2.3 AST Representation

- `ASTNode(kind, value=None, children=[])` represents a generic tree node.
- `make_leaf(kind, value)` is used for identifiers and constants.
- Nodes represent constructs like:
  - `Program`, `Decls`, `DeclList`, `Assignment`, `IfStatement`, `WhileStatement`
  - `BinOp`, `RelOp`, `UnaryOp`
  - `ArrayType`, `ArrayAccess`
  - `Read`, `WriteExpr`, `WriteString`

---

## 3. Implementation Details

### 3.1 File Overview

- **lexer.py** – token rules, comment skipping, categorization of tokens.
- **parser.py** – grammar rules, AST construction, syntax error handling.
- **ast_nodes.py** – AST definitions and level‑order traversal function.
- **main.py** – driver supporting `--lex` and `--parse` modes.

### 3.2 Error Handling

- Invalid characters trigger `t_error`, printing a message and skipping the character.
- Syntax errors trigger `p_error`, printing the token and line number where parsing failed.

---

## 4. Testing

### 4.1 Test Inputs

Test programs:

- `example1.sml`  
  Tests declarations, WHILE loops, OR, relational operators, arithmetic expressions.
- `if_example.sml`  
  Tests nested IF/ELSE statements, comparison operators, string constants, comments.
- `array_example.sml`  
  Tests ARRAY declarations, Dim syntax, array accesses, relational and arithmetic expressions.

### 4.2 Sample Output – Tokens

Using:

```bash
python main.py --lex examples/example1.sml
```

Tokens appear correctly categorized as:
- `KEYWORD`, `IDENTIFIER`, `CONSTANT`, `ARITH-OP`, `LOGIC-OP`, `SEPARATOR`.

### 4.3 Sample Output – Parse Tree

Using:

```bash
python main.py --parse examples/example1.sml
```

Produces a multi‑level BFS traversal such as:

```
Program

Identifier(example) # Decls # CompoundStatement

DeclList # StatementList

Decl # Read # Read # WhileStatement

...
```

This confirms the parser builds a structurally correct AST.

---

## 5. Limitations and Possible Extensions

### Limitations

- No type checking or semantic analysis.
- String literals limited to alphabetic characters.
- Only minimal syntax error recovery.
- One expected shift/reduce conflict in IF‑ELSE grammar.

### Possible Extensions

- Add symbol tables and type checking.
- Add an interpreter or code generator.
- Improve error recovery.
- Extend string literal support.

---

## 6. Conclusion

This project successfully implements the **lexical** and **syntactic** phases of a compiler front‑end for SomeWMULife.  
The lexer tokenizes input programs, the parser constructs a complete AST according to the grammar, and the level‑order traversal demonstrates the structural correctness of the tree.

The assignment provided hands‑on experience with compiler construction concepts such as tokenization, grammar design, AST representation, and PLY-based parsing.

