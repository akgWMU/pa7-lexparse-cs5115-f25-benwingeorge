# PA7 – SomeWMULife Lexical Analyzer & Parser

This project implements the **lexical analysis** and **parsing** phases of the SomeWMULife language using **PLY** (Python Lex & Yacc).  
It generates tokens, builds an Abstract Syntax Tree (AST), and outputs a **level‑order traversal** of the tree.

---

## 📁 Project Structure

```
PA7/
│
├── lexer.py          # Lexical analyzer (tokens, regex rules)
├── parser.py         # Parser + AST builder
├── ast_nodes.py      # AST Node class + level-order traversal
├── main.py           # CLI driver (--lex / --parse)
│
├── examples/         # Test programs
│   ├── example1.sml
│   ├── if_example.sml
│   └── array_example.sml
│
├── report/
│   └── PA7_Report.md
│
└── requirements.txt  # Dependencies (PLY)
```

---

## ⚙️ Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🔹 1. Lexical Analysis

```bash
python main.py --lex examples/example1.sml
```

Produces a token list such as:

```
[('KEYWORD', 'PROGRAM'), ('IDENTIFIER', 'example'), ('SEPARATOR', ';'), ...]
```

---

### 🔹 2. Parsing + AST Traversal

```bash
python main.py --parse examples/example1.sml
```

Example output:

```
Program

Identifier(example) # Decls # CompoundStatement

DeclList # StatementList

Decl # Read # Read # WhileStatement
...
```

Each line is a level; nodes in the same level are separated by `#`.

---

## 🧠 Features

### ✔ Lexer
- Distinguishes keywords vs identifiers  
- Supports int, float, scientific notation  
- String constants `'letters'`  
- Comments `{ ... }` skipped  
- Category mapping: KEYWORD, IDENTIFIER, CONSTANT, ARITH-OP, LOGIC-OP, SEPARATOR

### ✔ Parser
Implements full SomeWMULife grammar:
- Program + declarations
- IF / THEN / ELSE
- WHILE loops  
- READ / WRITE  
- Arrays: `ARRAY [low .. high] OF type`
- Expression grammar with correct precedence  

### ✔ AST
- Each rule produces an `ASTNode(kind, value, children)`
- Supports `BinOp`, `RelOp`, `UnaryOp`, `ArrayAccess`, etc.
- BFS traversal for final output

---

## 🧪 Test Programs

| File | Features Tested |
|------|-----------------|
| `example1.sml` | WHILE, OR, READ/WRITE, relational ops |
| `if_example.sml` | Nested IF/ELSE, comparisons, strings |
| `array_example.sml` | Arrays, indexing, Dim, WHILE, arithmetic |

---

## ⚠️ Limitations

- One intentional shift/reduce conflict (dangling else)  
- No semantic analysis or type checking  
- String literals limited to `[A-Za-z]*` per spec  

---

## 📚 Future Work

- Add symbol table + type checking  
- Add interpreter or code generator  
- Improve error recovery  
- Extend string literal capabilities  

---

## 🎉 Conclusion

This project demonstrates a complete PLY-based compiler front-end for SomeWMULife.  
It tokenizes the source, builds the AST, and prints a structured traversal suitable for additional compiler phases such as type checking and code generation.
