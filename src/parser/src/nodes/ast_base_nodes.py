from ..tokens import Token

class DataTypeNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.line = token.line

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": self.__class__.__name__,
            "value": self.value
        }

class OperatorNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.line = operator_token.line

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left_node}, {self.operator_token}, {self.right_node})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": self.__class__.__name__,
            "operator": self.operator_token.value,
            "left": self.left_node.to_dict(),
            "right": self.right_node.to_dict()
        }