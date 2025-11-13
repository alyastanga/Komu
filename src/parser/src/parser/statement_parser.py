# This file needs the statement and literal nodes
from ..tokens import TokenType
from ..nodes.literal_nodes import IdentifierNode
from ..nodes.statement_nodes import (VarAssignNode, MissionNode, ConditionalNode,
                                     WhileNode, ReturnNode, AssignNode)

class StatementParser:
    """
    Handles parsing all statements.
    This class is intended to be inherited by the main Parser.
    """
    def parse_statement(self):
        """Parses a single statement based on the current token."""
        if self.current_token.type == TokenType.KEYWORD:
            if self.current_token.value == 'var':
                return self.parse_var_declaration()
            elif self.current_token.value == 'mission':
                return self.parse_mission_statement()
            elif self.current_token.value == 'if':
                return self.parse_conditional()
            elif self.current_token.value == 'while':
                return self.parse_while_loop()
            elif self.current_token.value == 'return':
                return self.parse_return_statement()

            
        elif self.current_token.type == TokenType.IDENTIFIER:
            next_token = self.peek()
            if next_token.type == TokenType.ASSIGNMENT_OPERATOR:
                return self.parse_var_reassignment()
            else:
                return self.parse_expression_statement()
        elif self.current_token.type == TokenType.UNARY_OPERATOR:
            return self.parse_expression_statement()
            
        raise Exception(f"Syntax Error: Unexpected Keyword {self.current_token}")
    
    def parse_expression_statement(self):
        """Parses an expression followed by a semicolon as a statement."""
        expr_node = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return expr_node

    def parse_mission_statement(self):
        """Parses a mission (function) declaration statement."""
        self.expect(TokenType.KEYWORD)   
        identifier = self.expect(TokenType.IDENTIFIER) 
        if self.current_token.type == TokenType.LPAREN:
            params = self.parameters()
        else:
            params = [] 
        
        body = self.parse_block()

        return MissionNode(IdentifierNode(identifier), params, body)

    def parse_var_declaration(self):
        """Parses a variable declaration statement."""
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'var':
            self.expect(TokenType.KEYWORD) 
        identifier = self.expect(TokenType.IDENTIFIER)  
        self.expect(TokenType.ASSIGNMENT_OPERATOR)
        token_node = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        return VarAssignNode(IdentifierNode(identifier), token_node)
    
    def parameters(self):
        """Parses a list of parameters for missions (functions)."""
        params = []
        self.expect(TokenType.LPAREN)
        
        if self.current_token.type == TokenType.RPAREN:
            self.advance()
            return params
        
        params.append(self.parse_expression())

        while self.current_token.type == TokenType.COMMA:
            self.advance()  
            params.append(self.parse_expression())

        self.expect(TokenType.RPAREN)
        return params
    
    def parse_block(self):
        """Parses a block of statements enclosed in braces."""
        statements = []
        self.expect(TokenType.LBRACE)

        while self.current_token.type != TokenType.RBRACE:
            statement = self.parse_statement()
            statements.append(statement)

        self.expect(TokenType.RBRACE)
        return statements

    def parse_conditional(self):
        """Parses an if-else conditional statement."""
        self.expect(TokenType.KEYWORD)  
        self.expect(TokenType.LPAREN)    
        if_condition = self.parse_expression()  
        self.expect(TokenType.RPAREN)    
        if_body = self.parse_block()

        else_if_nodes = []   
        else_body = None

        while self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
            self.advance()
            if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'if':
                self.advance()  
                self.expect(TokenType.LPAREN)  
                else_if_condition = self.parse_expression()  
                self.expect(TokenType.RPAREN)  
                else_if_body = self.parse_block()  
                else_if_nodes.append((else_if_condition, else_if_body))
            else: 
                else_body = self.parse_block()
                break    

        return ConditionalNode(if_condition, if_body, else_if_nodes, else_body)
    
    def parse_while_loop(self):
        """Parses a while loop statement."""
        self.expect(TokenType.KEYWORD)
        self.expect(TokenType.LPAREN)
        loop_condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        loop_body = self.parse_block()

        return WhileNode(loop_condition, loop_body)
    
    def parse_var_reassignment(self):
        """Parses a variable reassignment statement."""
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGNMENT_OPERATOR)
        value = self.parse_expression_statement()


        return AssignNode(IdentifierNode(identifier), value)
    
    def parse_return_statement(self):
        """Parses a return statement."""
        self.expect(TokenType.KEYWORD)  
        return_value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        return ReturnNode(return_value)