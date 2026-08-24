from token_types import TokenType

# Operator sets used by the recursive descent evaluator.
ADD_OPS = {
    TokenType.PLUS, TokenType.MINUS, TokenType.EQUALS, TokenType.NOT_EQUALS,
    TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL
}
MUL_OPS = {TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0]
        self.variables = {}

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]

    def expect(self, ttype):
        if self.current_token.type != ttype:
            raise RuntimeError(f"Parse error: Expected {ttype} but got {self.current_token.type} at line {self.current_token.line}")
        self.advance()

    def parse_and_execute(self):
        while self.current_token.type != TokenType.EOF:
            self.statement()

    def statement(self):
        ttype = self.current_token.type
        if ttype == TokenType.LET:
            self.advance()                                   # consume 'let'
            name = self.current_token.value
            self.advance()                                   # consume variable name
            self.expect(TokenType.ASSIGN)
            self.variables[name] = self.evaluate_math_and_logic()
            self.expect(TokenType.SEMICOLON)
        elif ttype == TokenType.PRINT:
            self.advance()                                   # consume 'print'
            value = self.evaluate_math_and_logic()
            print(int(value) if isinstance(value, float) and value.is_integer() else value)
            self.expect(TokenType.SEMICOLON)
        elif ttype == TokenType.IF:
            self.parse_if()
        else:
            raise RuntimeError(f"Unexpected token: {ttype} at line {self.current_token.line}")

    def parse_if(self):
        self.advance()                                       # consume 'if'
        self.expect(TokenType.LPAREN)
        result = self.evaluate_math_and_logic()
        condition = isinstance(result, float) and result != 0.0
        self.expect(TokenType.RPAREN)

        if condition:
            self.execute_block()
            if self.current_token.type == TokenType.ELSE:
                self.advance()
                self.skip_block()
        else:
            self.skip_block()
            if self.current_token.type == TokenType.ELSE:
                self.advance()
                self.execute_block()

    def execute_block(self):
        self.expect(TokenType.LBRACE)
        while self.current_token.type != TokenType.RBRACE:
            self.statement()
        self.expect(TokenType.RBRACE)

    def skip_block(self):
        self.expect(TokenType.LBRACE)
        depth = 1
        while depth > 0:
            if self.current_token.type == TokenType.LBRACE: depth += 1
            elif self.current_token.type == TokenType.RBRACE: depth -= 1
            self.advance()

    def evaluate_math_and_logic(self):
        left = self.evaluate_multiplication_and_division()
        while self.current_token.type in ADD_OPS:
            op = self.current_token.type
            self.advance()
            left = self.eval(left, op, self.evaluate_multiplication_and_division())
        return left

    def evaluate_multiplication_and_division(self):
        left = self.evaluate_single_value()
        while self.current_token.type in MUL_OPS:
            op = self.current_token.type
            self.advance()
            left = self.eval(left, op, self.evaluate_single_value())
        return left

    def evaluate_single_value(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.advance()
            return float(token.value)
        if token.type == TokenType.STRING:
            self.advance()
            return token.value
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            if token.value not in self.variables:
                raise RuntimeError(f"Undefined variable: {token.value} at line {token.line}")
            return self.variables[token.value]
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.evaluate_math_and_logic()
            self.expect(TokenType.RPAREN)
            return result
        raise RuntimeError(f"Parse error at token: {token.type} at line {token.line}")

    def eval(self, left, op, right):
        # String concatenation
        if op == TokenType.PLUS and (isinstance(left, str) or isinstance(right, str)):
            return str(left) + str(right)

        # String comparison
        if isinstance(left, str) and isinstance(right, str):
            if op == TokenType.EQUALS:     return 1.0 if left == right else 0.0
            if op == TokenType.NOT_EQUALS: return 1.0 if left != right else 0.0
            raise RuntimeError(f"Unsupported string comparison: {op}")

        # Numeric operations
        if isinstance(left, float) and isinstance(right, float):
            if op == TokenType.PLUS:           return left + right
            if op == TokenType.MINUS:          return left - right
            if op == TokenType.MULTIPLY:       return left * right
            if op == TokenType.DIVIDE:
                if right == 0: raise RuntimeError("Division by zero")
                return left / right
            if op == TokenType.MODULO:         return left % right
            if op == TokenType.EQUALS:         return 1.0 if left == right else 0.0
            if op == TokenType.NOT_EQUALS:     return 1.0 if left != right else 0.0
            if op == TokenType.LESS:           return 1.0 if left < right else 0.0
            if op == TokenType.LESS_EQUAL:     return 1.0 if left <= right else 0.0
            if op == TokenType.GREATER:        return 1.0 if left > right else 0.0
            if op == TokenType.GREATER_EQUAL:  return 1.0 if left >= right else 0.0

        raise RuntimeError(f"Type error: cannot use {op} with {type(left).__name__} and {type(right).__name__}")
