from .ast_base_nodes import DataTypeNode

class NumberNode(DataTypeNode):
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Number"
        data["value"] = float(self.value) if '.' in self.value else int(self.value)
        return data
    
        
class StringNode(DataTypeNode):
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "String"
        return data

class BooleanNode(DataTypeNode):
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Boolean"
        data["value"] = True if self.value == 'true' else False
        return data

class IdentifierNode:
    def __init__(self, token):
        self.token = token  # <-- Renamed from self.Token
        self.name = token.value
        self.line = token.line

    def __repr__(self):
        return f'IdentifierNode({self.name})'
    
    def to_dict(self):
        return {
            "line": self.line,
            "type": "Identifier",
            "name": self.name
        }