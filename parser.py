# parser.py
"""
PLY-based parser for the SomeWMULife language.

It uses the lexer from lexer.py and builds an AST composed of ASTNode objects.

Usage:
    python -m parser examples/example1.sml
"""

import sys
import ply.yacc as yacc

from lexer import tokens, lexer
from ast_nodes import ASTNode, make_leaf, level_order_string

# -------------------------
# Grammar rules
# -------------------------

# Start symbol
start = "program"


def p_program(p):
    """program : PROGRAM IDENTIFIER SEMI decls compound_statement DOT"""
    # p[2] is the program identifier
    prog_id = make_leaf("Identifier", p[2])
    p[0] = ASTNode("Program", children=[prog_id, p[4], p[5]])


def p_decls_var(p):
    """decls : VAR decl_list"""
    p[0] = ASTNode("Decls", children=[p[2]])


def p_decls_empty(p):
    """decls : """
    p[0] = ASTNode("Decls")  # empty


def p_decl_list_single(p):
    """decl_list : identifier_list COLON type SEMI"""
    p[0] = ASTNode("DeclList", children=[
        ASTNode("Decl", children=[p[1], p[3]])
    ])


def p_decl_list_multi(p):
    """decl_list : decl_list identifier_list COLON type SEMI"""
    # append another Decl
    decl = ASTNode("Decl", children=[p[2], p[4]])
    p[1].children.append(decl)
    p[0] = p[1]


def p_identifier_list_single(p):
    """identifier_list : IDENTIFIER"""
    p[0] = ASTNode("IdentifierList", children=[make_leaf("Identifier", p[1])])


def p_identifier_list_multi(p):
    """identifier_list : identifier_list COMMA IDENTIFIER"""
    p[1].children.append(make_leaf("Identifier", p[3]))
    p[0] = p[1]


def p_type_standard(p):
    """type : standard_type"""
    p[0] = p[1]


def p_type_array(p):
    """type : array_type"""
    p[0] = p[1]


def p_standard_type(p):
    """standard_type : INTEGER
                     | FLOAT"""
    p[0] = ASTNode("StandardType", value=p[1])


def p_array_type(p):
    """array_type : ARRAY LBRACKET dim RBRACKET OF standard_type"""
    # ARRAY [ dim ] OF StandardType
    dim_node = p[3]
    std_type = p[6]
    p[0] = ASTNode("ArrayType", children=[dim_node, std_type])


def p_dim(p):
    """dim : INTNUM DOT DOT INTNUM"""
    p[0] = ASTNode("Dim", children=[
        make_leaf("IntConst", p[1]),
        make_leaf("IntConst", p[4]),
    ])


def p_compound_statement(p):
    """compound_statement : BEGIN statement_list END"""
    p[0] = ASTNode("CompoundStatement", children=[p[2]])


def p_statement_list_single(p):
    """statement_list : statement"""
    p[0] = ASTNode("StatementList", children=[p[1]])


def p_statement_list_multi(p):
    """statement_list : statement_list SEMI statement"""
    p[1].children.append(p[3])
    p[0] = p[1]


def p_statement(p):
    """statement : assignment
                 | if_statement
                 | while_statement
                 | io_statement
                 | compound_statement"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : variable ASSIGN expr"""
    p[0] = ASTNode("Assignment", children=[p[1], p[3]])


def p_if_statement_then_else(p):
    """if_statement : IF expr THEN statement ELSE statement"""
    p[0] = ASTNode("IfStatement", children=[p[2], p[4], p[6]])


def p_if_statement_then(p):
    """if_statement : IF expr THEN statement"""
    p[0] = ASTNode("IfStatement", children=[p[2], p[4]])


def p_while_statement(p):
    """while_statement : WHILE expr DO statement"""
    p[0] = ASTNode("WhileStatement", children=[p[2], p[4]])


def p_io_statement_read(p):
    """io_statement : READ LPAREN variable RPAREN"""
    p[0] = ASTNode("Read", children=[p[3]])


def p_io_statement_write_expr(p):
    """io_statement : WRITE LPAREN expr RPAREN"""
    p[0] = ASTNode("WriteExpr", children=[p[3]])


def p_io_statement_write_string(p):
    """io_statement : WRITE LPAREN STRING RPAREN"""
    p[0] = ASTNode("WriteString", children=[make_leaf("StringConst", p[3])])


def p_variable_simple(p):
    """variable : IDENTIFIER"""
    p[0] = ASTNode("Variable", children=[make_leaf("Identifier", p[1])])


def p_variable_array(p):
    """variable : IDENTIFIER LBRACKET expr RBRACKET"""
    p[0] = ASTNode("ArrayAccess", children=[
        make_leaf("Identifier", p[1]),
        p[3],
    ])


# ---- Expressions ----
# Expr: logical ops between rel_expr
def p_expr_bin_logop(p):
    """expr : expr logop rel_expr"""
    p[0] = ASTNode("BinOp", value=p[2], children=[p[1], p[3]])


def p_expr_rel_expr(p):
    """expr : rel_expr"""
    p[0] = p[1]


def p_logop(p):
    """logop : OR
             | AND"""
    p[0] = p[1]


def p_rel_expr_relop(p):
    """rel_expr : rel_expr relop add_expr"""
    p[0] = ASTNode("RelOp", value=p[2], children=[p[1], p[3]])


def p_rel_expr_add_expr(p):
    """rel_expr : add_expr"""
    p[0] = p[1]


def p_relop(p):
    """relop : LT
             | LE
             | GT
             | GE
             | EQ
             | NE"""
    p[0] = p[1]


def p_add_expr_addop(p):
    """add_expr : add_expr addop mul_expr"""
    p[0] = ASTNode("BinOp", value=p[2], children=[p[1], p[3]])


def p_add_expr_mul_expr(p):
    """add_expr : mul_expr"""
    p[0] = p[1]


def p_addop(p):
    """addop : PLUS
             | MINUS"""
    p[0] = p[1]


def p_mul_expr_mulop(p):
    """mul_expr : mul_expr mulop factor"""
    p[0] = ASTNode("BinOp", value=p[2], children=[p[1], p[3]])


def p_mul_expr_factor(p):
    """mul_expr : factor"""
    p[0] = p[1]


def p_mulop(p):
    """mulop : TIMES
             | DIVIDE"""
    p[0] = p[1]


def p_factor_variable(p):
    """factor : variable"""
    p[0] = p[1]


def p_factor_constant(p):
    """factor : constant"""
    p[0] = p[1]


def p_factor_not(p):
    """factor : NOT factor"""
    p[0] = ASTNode("UnaryOp", value="NOT", children=[p[2]])


def p_factor_paren(p):
    """factor : LPAREN expr RPAREN"""
    p[0] = p[2]


def p_constant_int(p):
    """constant : INTNUM"""
    p[0] = make_leaf("IntConst", p[1])


def p_constant_float(p):
    """constant : FLOATNUM"""
    p[0] = make_leaf("FloatConst", p[1])


# -------------------------
# Error rule
# -------------------------

def p_error(p):
    if p is None:
        print("Syntax error: unexpected end of input")
    else:
        print(f"Syntax error at token '{p.value}' (type={p.type}) line={p.lineno}")
    # You can choose to raise an exception to stop parsing:
    # raise SyntaxError("Parsing failed")


# Build the parser
parser = yacc.yacc()


def parse_file(filename: str) -> ASTNode:
    with open(filename, "r") as f:
        data = f.read()
    return parser.parse(data, lexer=lexer)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m parser <source-file>")
        sys.exit(1)

    ast_root = parse_file(sys.argv[1])
    if ast_root is not None:
        print(level_order_string(ast_root))