# Exceções léxicas (LexError, UnclosedString, ...)
class LexError(Exception):
    pass

class UnclosedComment(LexError):
    pass

class UnclosedString(LexError):
    pass

class InvalidCharLiteral(LexError):
    pass