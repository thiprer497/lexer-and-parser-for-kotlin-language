# helpers pequenos (is_hex, is_bin ...) # wrapper TokenStream com peek()/next()/expect()
def eh_hex(ch: str) -> bool:
    return ch.isdigit() or ch.lower() in 'abcdef'

def eh_bin(ch: str) -> bool:
    return ch in '01'

def eh_sufixo_inteiro(ch: str) -> bool:
    return ch.lower() in ('u', 'l')

def eh_sufixo_float(ch: str) -> bool:
    return ch.lower() == 'f'

def eh_separador(ch: str) -> bool:
    return ch == '_'