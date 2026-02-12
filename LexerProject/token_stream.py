from .tokens import Token
from .tokens import Token as _TokenClass  #util para type hints dos metodos de uma classe

class TokenStream:
    def __init__(self, lexer):
        self.tokens = lexer.tokenize()
        self.pos = 0

    def peek(self, n=0):
        idx = self.pos + n
        if idx < 0:
            return Token("EOF", "", -1, -1)
        if idx >= len(self.tokens):
            return Token("EOF", "", -1, -1)
        return self.tokens[idx]

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def match(self, tipo):
        if self.peek().tipo == tipo:
            self.next()
            return True
        return False

    def expect(self, tipo):
        tok = self.next()
        if tok.tipo != tipo:
            raise Exception(f"ParseError: esperado {tipo} mas veio {tok.tipo} em linha {tok.linha}, coluna {tok.coluna}")
        return tok

    def save(self):
        return self.pos

    def restore(self, pos):
        self.pos = pos