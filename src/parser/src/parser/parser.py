from ..tokens import Token, TokenType
from .expression_parser import ExpressionParser
from .statement_parser import StatementParser

class Parser(ExpressionParser, StatementParser):
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0

        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = Token(TokenType.EOF, None)

    def peek(self):
        peek_idx = self.token_idx + 1
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        else:
            return Token(TokenType.EOF, None)    
    
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = Token(TokenType.EOF, None)
    
    def expect(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        
        else:
            raise Exception(f'Expected token type {token_type}, got {self.current_token.type} at line {self.current_token.line}')
    
    def parse(self):
        statements = []

        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            statements.append(statement)

        return statements
