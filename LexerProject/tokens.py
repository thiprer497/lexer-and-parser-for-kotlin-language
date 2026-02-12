 # Token dataclass + TokenType enum
from dataclasses import dataclass

@dataclass
class Token:
    tipo: str
    lexema: str
    linha: int
    coluna: int

    def __repr__(self):
        return f"Token({self.tipo}, '{self.lexema}', linha = {self.linha}, coluna = {self.coluna})"