from ..tokens import Token, TokenType
from ..lexer.lexer_constants import RELATIONAL_OPERATORS
from ..nodes.literal_nodes import (NumberNode, StringNode, BooleanNode, IdentifierNode)
from ..nodes.expression_nodes import (BinaryOpNode, RelationalOpNode, LogicalOpNode, BitwiseOpNode, 
                                      UnaryOpNode, PostfixUnaryOpNode)
from ..nodes.statement_nodes import MissionCallNode

class ExpressionParser:
    """
    Handles parsing all expressions using a precedence ladder.
    This class is intended to be inherited by the main Parser.
    """
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left_node = self.parse_logical_and()
        while (self.current_token.type == TokenType.LOGICAL_OPERATOR and
                                          self.current_token.value == '||'):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_logical_and()
            new_logicalOp = LogicalOpNode(left_node, operator_token, right_node)
            left_node = new_logicalOp
        return left_node 

    def parse_logical_and(self):
        left_node = self.parse_bitwise_or()
        while (self.current_token.type == TokenType.LOGICAL_OPERATOR and
                                            self.current_token.value == '&&'):
                operator_token = self.current_token            
                self.advance()
                right_node = self.parse_bitwise_or()
                new_logicalOp = LogicalOpNode(left_node, operator_token, right_node)
                left_node = new_logicalOp
        return left_node 

    def parse_bitwise_or(self):
        left_node = self.parse_bitwise_xor()
        while (self.current_token.type == TokenType.BITWISE_OPERATOR and
                                          self.current_token.value  == '|'):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_bitwise_xor()
            new_bitwiseOp = BitwiseOpNode(left_node, operator_token, right_node)
            left_node = new_bitwiseOp
        return left_node 

    def parse_bitwise_xor(self):
        left_node = self.parse_bitwise_and()
        while (self.current_token.type == TokenType.BITWISE_OPERATOR and
                                            self.current_token.value == '^'):
                operator_token = self.current_token            
                self.advance()
                right_node = self.parse_bitwise_and()
                new_bitwiseOp = BitwiseOpNode(left_node, operator_token, right_node)
                left_node = new_bitwiseOp
        return left_node 
    
    def parse_bitwise_and(self):
        left_node = self.parse_comparison()
        while (self.current_token.type == TokenType.BITWISE_OPERATOR and 
                                          self.current_token.value == '&'):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_comparison()
            new_bitwiseOp = BitwiseOpNode(left_node, operator_token, right_node)
            left_node = new_bitwiseOp
        return left_node 
     
    def parse_comparison(self):
        left_node = self.parse_term()
        while (self.current_token.type == TokenType.RELATIONAL_OPERATOR and 
                                          self.current_token.value in RELATIONAL_OPERATORS):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_term()
            new_relationalOp = RelationalOpNode(left_node, operator_token, right_node)
            left_node = new_relationalOp
        return left_node
    
    def parse_term(self):
        left_node = self.parse_factor()
        while (self.current_token.type == TokenType.ARITHMETIC_OPERATOR and 
                                          self.current_token.value in {'+', '-'}):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_factor()
            new_binaryOp = BinaryOpNode(left_node, operator_token, right_node)
            left_node = new_binaryOp
        return left_node
    
    def parse_factor(self):
        left_node = self.parse_primary()
        while (self.current_token.type == TokenType.ARITHMETIC_OPERATOR and 
                                          self.current_token.value in {'*', '/'}):
            operator_token = self.current_token            
            self.advance()
            right_node = self.parse_primary()
            new_binaryOp = BinaryOpNode(left_node, operator_token, right_node)
            left_node = new_binaryOp
        return left_node
    
    def parse_primary(self):
        token = self.current_token
        if token.type == TokenType.ARITHMETIC_OPERATOR and token.value == '-':
            self.advance()
            negation_node = self.parse_primary()
            return UnaryOpNode(token, negation_node)
        elif token.type == TokenType.LOGICAL_OPERATOR and token.value == '!':
            self.advance()
            not_node = self.parse_primary()
            return UnaryOpNode(token, not_node)
        elif token.type == TokenType.BITWISE_OPERATOR and token.value == '~':
            self.advance()
            bitwise_not_node = self.parse_primary()
            return UnaryOpNode(token, bitwise_not_node)
        elif token.type == TokenType.ARITHMETIC_OPERATOR and token.value == '+':
            self.advance()
            plus_node = self.parse_primary()
            return UnaryOpNode(token, plus_node)
        elif token.type == TokenType.UNARY_OPERATOR and token.value == '++':  
            self.advance()
            increment_node = self.parse_primary()
            return UnaryOpNode(token, increment_node)
        elif token.type == TokenType.UNARY_OPERATOR and token.value == '--':
            self.advance()
            decrement_node = self.parse_primary()
            return UnaryOpNode(token, decrement_node)
        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token)
        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token)
        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return BooleanNode(token)
        elif token.type == TokenType.IDENTIFIER:
            next_token = self.peek()
            self.advance()
            if next_token.type == TokenType.LPAREN:                
                identifier_token = token
                args = self.parameters() 
                return MissionCallNode(IdentifierNode(identifier_token), args)
            if(next_token.type == TokenType.UNARY_OPERATOR and 
               next_token.value in {'++', '--'}):
                identifier_token = token
                operator_token = next_token
                self.advance()
                return PostfixUnaryOpNode(IdentifierNode(identifier_token), operator_token)
            else: 
                return IdentifierNode(token)
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr_node = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr_node
        else:
            raise Exception(f"Syntax Error: Unexpected token {token.type}", token.line)