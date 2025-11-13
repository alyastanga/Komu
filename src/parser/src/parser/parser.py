from ..tokens import Token, TokenType
from .expression_parser import ExpressionParser
from .statement_parser import StatementParser

class Parser(ExpressionParser, StatementParser):
    """ Main Parser Class
    Combines expression and statement parsing to build the AST.
    Uses recursive descent parsing techniques.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0

        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = Token(TokenType.EOF, None)

    def peek(self):
        """Peeks at the next token without advancing the current position."""
        peek_idx = self.token_idx + 1
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        else:
            return Token(TokenType.EOF, None)    
    
    def advance(self):
        """Advances to the next token in the token list."""
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = Token(TokenType.EOF, None)
    
    def expect(self, token_type):
        """expects the current token to be of a specific type and advances."""
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        
        else:
            raise Exception(f'Expected token type {token_type}, got {self.current_token.type} at line {self.current_token.line}')
    
    def parse(self):
        """Parses the entire token list into an AST."""
        statements = []

        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            statements.append(statement)

        return statements
