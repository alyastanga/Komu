from .ast_base_nodes import OperatorNode

class BinaryOpNode(OperatorNode):
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "BinaryOp"
        return data
    
class RelationalOpNode(OperatorNode):  
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "RelationalOp"
        return data
    
class LogicalOpNode(OperatorNode):    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "LogicalOp"
        return data

class BitwiseOpNode(OperatorNode):   
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "BitwiseOp"
        return data
    
class UnaryOpNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        self.line = operator_token.line

    def __repr__(self):
        return f'UnaryOpNode({self.operator_token}, {self.node})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "UnaryOp",
            "operator": self.operator_token.value,
            "node": self.node.to_dict()
        }

class PostfixUnaryOpNode:
    def __init__(self, node, operator_token):
        self.node = node
        self.operator_token = operator_token
        self.line = operator_token.line

    def __repr__(self):
        return f'PostFixUnaryOpNode({self.node}, {self.operator_token})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "PostfixUnaryOp",
            "operator": self.operator_token.value,
            "node": self.node.to_dict()
        }