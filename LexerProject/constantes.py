 # OPERADORES, SIMBOLOS, KEYWORDS
# mapeamento lexema -> token-type
OPERADORES = {
    # atribuição
    "=": "OP_ASSIGN",

    # aritméticos
    "+": "OP_PLUS",
    "-": "OP_MINUS",
    "*": "OP_MUL",
    "/": "OP_DIV",
    "%": "OP_MOD",

    # comparação
    "===": "OP_EQ_STRICT",
    "!==": "OP_NEQ_STRICT",
    "==": "OP_EQ",
    "!=": "OP_NEQ",
    "<=": "OP_LE",
    ">=": "OP_GE",
    "<": "OP_LT",
    ">": "OP_GT",

    # lógicos
    "&&": "OP_AND",
    "||": "OP_OR",
    "!": "OP_NOT",

    # incremento / atribuição
    "++": "OP_INC",
    "--": "OP_DEC",
    "+=": "OP_PLUS_ASSIGN",
    "-=": "OP_MINUS_ASSIGN",
    "*=": "OP_MUL_ASSIGN",
    "/=": "OP_DIV_ASSIGN",

    # setas / ranges
    "->": "OP_ARROW",
    "..<": "OP_RANGE_UNTIL",
    "..": "OP_RANGE",

    # null-safety
    "?.": "OP_SAFE_CALL",
    "?:": "OP_ELVIS",
    "!!": "OP_NOT_NULL",

    # outros
    "::": "OP_REF",
}

# simbolos simples
SIMBOLOS = {
    '(': "LPAREN",
    ')': "RPAREN",
    '{': "LBRACE",
    '}': "RBRACE",
    '[': "LBRACKET",
    ']': "RBRACKET",
    ',': "COMMA",
    ';': "SEMICOLON",
    ':': "COLON",
    '.': "DOT",
    '@': "AT",
    '?': "QUESTION",
}

# lista de palavras-chave (mantive seus conjuntos originais)
MODIFIER_KEYWORDS = {
    "abstract", "actual", "annotation", "companion", "const", "crossinline",
    "data", "enum", "expect", "external", "final", "infix", "inline", "inner",
    "internal", "lateinit", "noinline", "open", "operator", "out", "override",
    "private", "protected", "public", "reified", "sealed", "suspend", "tailrec",
    "vararg"
}

SOFT_KEYWORDS = {
    "by", "catch", "constructor", "delegate", "dynamic", "field", "file",
    "finally", "get", "import", "init", "param", "property", "receiver", "set",
    "setparam", "value", "where"
}

HARD_KEYWORDS = {
    "as", "as?", "break", "class", "continue", "do", "else", "false", "for", "fun",
    "if", "in", "!in", "interface", "is", "!is", "null", "object", "package",
    "return", "super", "this", "throw", "true", "try", "typealias", "typeof", "val",
    "var", "when", "while"
}

# cria um mapa lexema -> token_type (strings)
KEYWORDS = {}

# hard keywords: prefix KW_
for kw in HARD_KEYWORDS:
    # normaliza lexema para nome de token: transforma chars problemáticos
    token_name = "KW_" + kw.upper().replace('?', '_Q').replace('!', 'NOT_').replace('-', '_').replace('.', '_').replace('<', '_LT_').replace('>', '_GT_')
    KEYWORDS[kw] = token_name

# soft keywords: prefix SK_
for kw in SOFT_KEYWORDS:
    token_name = "SK_" + kw.upper().replace('?', '_Q').replace('!', 'NOT_').replace('-', '_')
    KEYWORDS[kw] = token_name

# modifier keywords: prefix MOD_
for kw in MODIFIER_KEYWORDS:
    token_name = "MOD_" + kw.upper().replace('-', '_')
    KEYWORDS[kw] = token_name