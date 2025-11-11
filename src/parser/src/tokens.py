from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    ARITHMETIC_OPERATOR = auto()
    RELATIONAL_OPERATOR = auto()
    ASSIGNMENT_OPERATOR = auto()
    LOGICAL_OPERATOR = auto()
    BITWISE_OPERATOR = auto()
    UNARY_OPERATOR = auto()
    KEYWORD = auto()
    WHITESPACE = auto()
    COMMENT = auto()
    SEMICOLON = auto()
    LPAREN = auto()  
    RPAREN = auto()  
    LBRACE = auto()  
    RBRACE = auto()
    COMMA = auto()
    BOOLEAN = auto()
    DOT = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f'Token({self.type}, {self.value}, line {self.line})'