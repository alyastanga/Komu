#include "interpreter.hpp"
#include "json.hpp"
#include <iostream>
#include <fstream>

using json = nlohmann::json;

int main(){
    std::cout << "Komu Interpreter" << std::endl;

    std::ifstream ast_file("ast_output.json");
    if (!ast_file.is_open()) {
        std::cerr << "Error: Could not open ast.json!" << std::endl;
        return 1; 
    }

    json ast_data;
    try {
        ast_data = json::parse(ast_file);
    } catch (json::parse_error& e) {
        std::cerr << "Error: Failed to parse JSON: " << e.what() << std::endl;
        return 1; 
    }

    Interpreter komu_interpreter;
    komu_interpreter.interpret(ast_data);

    return 0; 
}
