from ..tokens import Token, TokenType
from .lexer_constants import KEYWORDS, ARITHMETIC_OPERATORS, LOGICAL_OPERATORS, SINGLE_CHAR_TOKENS

class Lexer:
    """ This class is responsible for converting the input source code into tokens. """
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.line = 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
        else:
            self.current_char = None

    def advance(self):
        """Advances the 'cursor' to the next character in the input text."""
        if self.current_char == '\n':
            self.line += 1
        self.position += 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        """Peeks at the next character without advancing the current position."""
        peek_pos = self.position + 1
        if peek_pos < len(self.input_text):
            return self.input_text[peek_pos]
        else:
            return None

    def get_number(self):
        """Extracts a number (integer or float) from the input text."""
        result = ''
        
        if self.current_char == '.':
            result = '0.'
            self.advance() 
        else:
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            if self.current_char == '.':
                result += self.current_char 
                self.advance() 
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
        return Token(TokenType.NUMBER, result , self.line)

    def get_string(self):
        """Extracts a string literal from the input text."""
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char is None:
            raise Exception(f'Unterminated string literal at line {self.line}')
        self.advance() 
        return Token(TokenType.STRING, result , self.line)
    
    def get_boolean(self, value):
        """Extracts a boolean literal from the input text."""
        return Token(TokenType.BOOLEAN, value , self.line)
    
    def get_identifier_or_keyword(self):
        """Extracts an identifier or keyword from the input text."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result in KEYWORDS:
            return Token(TokenType.KEYWORD, result , self.line)
        return Token(TokenType.IDENTIFIER, result , self.line)
    
    def _check_keyword(self, keyword, token_type):
        """Checks if the current position matches a specific keyword."""
        keyword_len = len(keyword)

        if self.input_text[self.position : self.position + keyword_len] == keyword:
            
            boundary_idx = self.position + keyword_len
            
            if boundary_idx >= len(self.input_text):
                for _ in range(keyword_len): self.advance()
                return Token(token_type, keyword, self.line)

            boundary_char = self.input_text[boundary_idx]
            if boundary_char.isalnum() or boundary_char == '_':
                return self.get_identifier_or_keyword() 
            
            for _ in range(keyword_len): self.advance()
            return Token(token_type, keyword, self.line)

        return self.get_identifier_or_keyword()
    
    def get_next_token(self):
        """Main method to get the next token from the input text."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            if (self.current_char.isdigit() or 
                    (self.current_char == '.' and 
                    self.peek() is not None and self.peek().isdigit())): 
                return self.get_number()
            
            if self.current_char == '"':
                self.advance()
                return self.get_string()
            
            if self.current_char == 't':
                return self._check_keyword('true', TokenType.BOOLEAN)
            
            if self.current_char == 'f':
                return self._check_keyword('false', TokenType.BOOLEAN) 
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier_or_keyword()
            
            if self.current_char in {'+', '-'}:
                char = self.current_char
                next_char = self.peek()
                if  next_char == char:
                    char += next_char
                    self.advance()
                    self.advance()
                    return Token(TokenType.UNARY_OPERATOR, char , self.line)

            if self.current_char in ARITHMETIC_OPERATORS:
                char = self.current_char
                self.advance()
                return Token(TokenType.ARITHMETIC_OPERATOR, char , self.line)
            
            if self.current_char in {'=', '!', '<', '>'}:
                char = self.current_char
                next_char = self.peek()
                if next_char == '=':
                    char += next_char
                    self.advance()
                    self.advance()
                    return Token(TokenType.RELATIONAL_OPERATOR, char , self.line)
                elif char in {'<', '>'}:
                    self.advance()
                    return Token(TokenType.RELATIONAL_OPERATOR, char , self.line)
                elif char == '!':
                    self.advance()
                    return Token(TokenType.LOGICAL_OPERATOR, char , self.line)                
                else: 
                    if char == '=':
                        self.advance()
                        return Token(TokenType.ASSIGNMENT_OPERATOR, char , self.line)
            
            if self.current_char in {'&', '|', '^', '~'}:
                char = self.current_char
                next_char = self.peek()
                if next_char is not None and char + next_char in LOGICAL_OPERATORS:
                    char += next_char
                    self.advance()
                    self.advance()
                    return Token(TokenType.LOGICAL_OPERATOR, char , self.line)
                else:
                    self.advance()
                    return Token(TokenType.BITWISE_OPERATOR, char , self.line)
            
            if self.current_char in SINGLE_CHAR_TOKENS:
                token_type = SINGLE_CHAR_TOKENS[self.current_char]
                char = self.current_char
                self.advance()
                return Token(token_type, char , self.line)
    
            raise Exception(f'Unknown character: {self.current_char} at line {self.line}')
        
        return Token(TokenType.EOF, None , self.line)
    
    def tokenize(self):
        """Tokenizes the entire input text into a list of tokens."""
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens
        
        