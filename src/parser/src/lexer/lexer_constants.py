from ..tokens import TokenType

"""Lexer Constants Module"""

KEYWORDS = {'if', 'else if', 'else' ,'while', 'return', 'var', 'mission'}     
ARITHMETIC_OPERATORS = {'+', '-', '*', '/', '%'}
ASSIGNMENT_OPERATOR = {'='}
RELATIONAL_OPERATORS = {'==', '!=', '<', '>', '<=', '>='}
UNARY_OPERATORS = {'-', '+'}
LOGICAL_OPERATORS = {'&&', '||', '!'}
BITWISE_OPERATORS = {'&', '|', '^', '~'}
BOOLEAN_LITERALS = {'true', 'false'}
SINGLE_CHAR_TOKENS = {
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
    }
