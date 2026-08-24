class TokenType:
    # Keywords
    LET = "LET"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"

    ASSIGN = "ASSIGN"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    EOF = "EOF"

class Token:
    def __init__(self, type: str, value: str, line: int):
        self.type = type
        self.value = value
        self.line = line
