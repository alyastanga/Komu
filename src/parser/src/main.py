from .lexer.lexer import Lexer
from .parser.parser import Parser
from .nodes import *
import json
import os
import sys

def read_komu_file(file_path):
    if not file_path.endswith('.komu'):
        print("Error: Input file must have a .komu extension.")
        sys.exit(1)
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
    with open(file_path, 'r') as f:
        return f.read()



def run_frontend(input_text):
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    # print("Tokens:", tokens)


    parser = Parser(tokens)
    ast_nodes = parser.parse()
    # print(f"Parser Output (AST): \n {ast_nodes}")

    # print("MISSSION NODE", MissionNode)

    list_of_dicts = [node.to_dict() for node in ast_nodes]
    # print(f"AST as list of dicts:\n {list_of_dicts}")
    output_filename = "build/ast_output.json"

    with open(output_filename, 'w') as f:
        json.dump(list_of_dicts, f, indent=4)
    
    # print(f"AST written to {output_filename}")

    return output_filename

if __name__ == "__main__":
    source_code = read_komu_file("examples/test.komu")
    # print(source_code)
    run_frontend(source_code)