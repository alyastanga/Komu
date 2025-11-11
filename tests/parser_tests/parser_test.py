import sys
import os

test_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(test_file_path)))
sys.path.insert(0, project_root)

from src.parser.src.lexer.lexer import Lexer
from src.parser.src.parser.parser import Parser


def test_simple_variable_declaration():
    """
    Tests parsing a simple 'var x = 5;'
    """
    code = "var x = 5;"
    
    # 1. Run the lexer
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # 2. Run the parser 
    parser = Parser(tokens)
    ast_nodes = parser.parse()
    
    # 3. Write assertions to check the AST
    assert len(ast_nodes) == 1
    
    var_node = ast_nodes[0]
    assert var_node.identifier.name == "x"
    assert var_node.value.value == '5'