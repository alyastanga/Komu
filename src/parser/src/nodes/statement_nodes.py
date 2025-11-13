"""Statement Nodes for the AST."""
from .literal_nodes import IdentifierNode

class VarAssignNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value
        self.line = identifier.line

    def __repr__(self):
        return f'VarAssignNode({self.identifier}, {self.value})'
    
    def to_dict(self):
        return{
            "line": self.line,
            "type" : "Var",
            "identifier": self.identifier.name,
            "value": self.value.to_dict()
        }
    
class AssignNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value
        self.line = identifier.line
    
    def __repr__(self):
        return f'AssignNode({self.identifier}, {self.value})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "Assign",
            "identifier": self.identifier.name,
            "value": self.value.to_dict()
        }
    
class MissionNode:
    def __init__(self, identifier, parameter = None, body = None):
        self.identifier = identifier
        self.value = identifier.name
        self.line = identifier.line
        self.parameter = parameter
        self.body = body

    def __repr__(self):
        if self.parameter:
            return f'MissionNode({self.identifier}, {self.parameter}, {self.body})'
        else:
            return f'MissionNode({self.identifier})'
    
    def to_dict(self):
        if self.parameter:
            return {
                "line": self.line,
                "type": "Mission",
                "identifier": self.identifier.name,
                "parameter": [param.to_dict() for param in self.parameter],
                "body": [stmt.to_dict() for stmt in self.body]
                
            }
        else: 
            return {
                "line": self.line,
                "type": "Mission",
                "identifier": self.identifier.name,
                "body": [stmt.to_dict() for stmt in self.body]
            }


class MissionCallNode:
    def __init__(self, identifier, argument):
        self.identifier = identifier
        self.value = identifier.name
        self.line = identifier.line
        self.argument = argument

    def __repr__(self):
        if self.argument:
            return f'MissionCallNode({self.identifier}, {self.argument})'
        else:
            return f'MissionCallNode({self.identifier})'
    
    def to_dict(self):
        if self.argument:
            return {
                "line": self.line,
                "type": "MissionCall",
                "identifier": self.value,
                "argument": [arg.to_dict() for arg in self.argument]
            }
        else: 
            return {
                "line": self.line,
                "type": "MissionCall",
                "identifier": self.value
            }


class ConditionalNode:
    def __init__(self, if_condition, if_body, else_if_condition = None, else_body = None):
        self.if_condition = if_condition
        self.if_body = if_body
        self.else_if_condition = else_if_condition if else_if_condition is not None else []
        self.else_body = else_body

    def __repr__(self):
        if self.else_if_condition and self.else_body:
            return f'Conditional Node({self.if_condition}, {self.if_body}, {self.else_if_condition}, {self.else_body})'
        elif self.else_if_condition:
            return f'Conditional Node({self.if_condition}, {self.if_body}, {self.else_if_condition})'
        elif self.else_body:
            return f'Conditional Node({self.if_condition}, {self.if_body}, {self.else_body})'
        else: 
            return f'Conditional Node({self.if_condition}, {self.if_body})'
    
    def to_dict(self):
        if self.else_if_condition and self.else_body:
            return {
                "line": self.if_condition.line,
                "type": "Conditional",
                "if": {
                    "condition": self.if_condition.to_dict(),
                    "body": [stmt.to_dict() for stmt in self.if_body]
                },
                "else_if": [
                    {
                        "condition": cond.to_dict(),
                        "body": [stmt.to_dict() for stmt in body]
                    } for cond, body in self.else_if_condition
                ],
                "else": [stmt.to_dict() for stmt in self.else_body]
            }
        elif self.else_if_condition:
            return {
                "line": self.if_condition.line,
                "type": "Conditional",
                "if": {
                    "condition": self.if_condition.to_dict(),
                    "body": [stmt.to_dict() for stmt in self.if_body]
                },
                "else_if": [
                    {
                        "condition": cond.to_dict(),
                        "body": [stmt.to_dict() for stmt in body]
                    } for cond, body in self.else_if_condition
                ]
            }
        elif self.else_body:
            return {
                "line": self.if_condition.line,
                "type": "Conditional",
                "if": {
                    "condition": self.if_condition.to_dict(),
                    "body": [stmt.to_dict() for stmt in self.if_body]
                },
                "else": [stmt.to_dict() for stmt in self.else_body]
            }
        else:
            return {

                "line": self.if_condition.line,
                "type": "Conditional",
                "if": {
                    "condition": self.if_condition.to_dict(),
                    "body": [stmt.to_dict() for stmt in self.if_body]
                }
            }
        
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.line = condition.line

    def __repr__(self):
        return f'WhileNode({self.condition}, {self.body})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "While",
            "condition": self.condition.to_dict(),
            "body": [stmt.to_dict() for stmt in self.body]
        }
    
class ReturnNode:
    def __init__(self, value):
        self.value = value
        self.line = value.line

    def __repr__(self):
        return f'ReturnNode({self.value})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "Return",
            "value": self.value.to_dict()
        }
    
