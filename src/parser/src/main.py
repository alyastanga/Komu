import sys
import json
from .lexer.lexer import Lexer
from .parser.parser import Parser
from .resolver.resolver import Resolver

def main(file_path):
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)

    # Lexer -- Read source code and produce tokens
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Parser -- Check syntax and build AST
    parser = Parser(tokens)
    ast_nodes = parser.parse()

    # RESOLVER -- Semantic analysis and variable resolution
    try:
        resolver = Resolver()
        resolver.resolve(ast_nodes)
        print("Resolver check passed.")
    except Exception as e:
        print(e) # Print resolver errors
        sys.exit(1)

    # JSON Output
    ast_json = [node.to_dict() for node in ast_nodes]

    project_root = sys.path[0] 
    output_path = f"{project_root}/build/ast_output.json"
    
    try:
        with open(output_path, 'w') as f:
            json.dump(ast_json, f, indent=4)
        print(f"AST successfully generated at {output_path}")
    except Exception as e:
        print(f"Error writing AST to JSON: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 -m src.parser.src.main <file_path.komu>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)