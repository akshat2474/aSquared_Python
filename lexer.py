from token_types import TokenType, Token

KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE
}

SIMPLE_SYMBOLS = {
    '+': TokenType.PLUS,      '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,  '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,    ';': TokenType.SEMICOLON,
}

class Lexer:
    def __init__(self, source: str):
        self.input = source
        self.position = 0
        self.line = 1
        self.current_char = self.input[0] if self.input else '\0'

    def advance(self):
        self.position += 1
        if self.position >= len(self.input):
            self.current_char = '\0'
        else:
            self.current_char = self.input[self.position]
            if self.current_char == '\n':
                self.line += 1

    def peek(self) -> str:
        next_pos = self.position + 1
        return self.input[next_pos] if next_pos < len(self.input) else '\0'

    def create_token(self, ttype: TokenType, value: str) -> Token:
        return Token(type=ttype, value=value, line=self.line)

    def skip_whitespace(self):
        while self.current_char != '\0' and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '\0' and self.current_char != '\n':
            self.advance()

    def read_number(self) -> Token:
        start_pos = self.position
        while self.current_char.isdigit() or self.current_char == '.':
            self.advance()
        val_str = self.input[start_pos:self.position]
        return self.create_token(TokenType.NUMBER, val_str)

    def read_identifier(self) -> Token:
        start_pos = self.position
        while self.current_char.isalnum() or self.current_char == '_':
            self.advance()
        val_str = self.input[start_pos:self.position]
        ttype = KEYWORDS.get(val_str, TokenType.IDENTIFIER)
        return self.create_token(ttype, val_str)

    def read_string(self) -> Token:
        self.advance() # consume opening quote
        start_pos = self.position
        while self.current_char != '\0' and self.current_char != '"':
            if self.current_char == '\\' and self.peek() == '"':
                self.advance()
                self.advance()
                continue
            self.advance()
        val_str = self.input[start_pos:self.position].replace('\\"', '"')
        self.advance() # consume closing quote
        return self.create_token(TokenType.STRING, val_str)

    def read_symbol(self) -> Token:
        c = self.current_char

        # Single-character symbols: resolved via the module-level lookup table
        if c in SIMPLE_SYMBOLS:
            self.advance()
            return self.create_token(SIMPLE_SYMBOLS[c], c)

        # Double-character symbols: need to peek() at the next character
        if c == '=':
            if self.peek() == '=':
                self.advance(); self.advance()
                return self.create_token(TokenType.EQUALS, "==")
            self.advance()
            return self.create_token(TokenType.ASSIGN, "=")
        if c == '!':
            if self.peek() == '=':
                self.advance(); self.advance()
                return self.create_token(TokenType.NOT_EQUALS, "!=")
        if c == '<':
            if self.peek() == '=':
                self.advance(); self.advance()
                return self.create_token(TokenType.LESS_EQUAL, "<=")
            self.advance()
            return self.create_token(TokenType.LESS, "<")
        if c == '>':
            if self.peek() == '=':
                self.advance(); self.advance()
                return self.create_token(TokenType.GREATER_EQUAL, ">=")
            self.advance()
            return self.create_token(TokenType.GREATER, ">")

        raise RuntimeError(f"Unexpected character: {c} at line {self.line}")

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.current_char != '\0':
            if self.current_char == '#':
                self.skip_comment()
                continue
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.read_identifier())
                continue
            if self.current_char == '"':
                tokens.append(self.read_string())
                continue
            
            tokens.append(self.read_symbol())
            
        tokens.append(self.create_token(TokenType.EOF, ""))
        return tokens
