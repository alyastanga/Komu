#include <stdexcept>
#include <iostream>
#include "interpreter.hpp"
#include <variant>

/**
 * @brief Evaluates an expression node and returns its integer value.
 */

KomuValue Interpreter::evaluate_binary_expression(const json& expr) {
    std::string type = expr.at("type");
    int line = static_cast<int>(expr.at("line"));
    if(type == "UnaryOp"){
        std::string op = expr.at("operator").get<std::string>();
        json operand_expr = expr.at("node");
    
        KomuValue op_value = evaluate_binary_expression(operand_expr);
        double num_value = std::get<double>(op_value.value);

        if(op == "-"){
            return KomuValue(-num_value);
        } else if (op == "~"){
            return KomuValue(static_cast<double>(~static_cast<int>(num_value)));
        } else if(op == "+"){
            return KomuValue(+num_value);
        }

        if(operand_expr.at("type") != "Identifier"){
            throw std::runtime_error("Error: Unary operator '" + op + "' can only be applied to variables at line: " + std::to_string(line) + ".");
        }

        std::string var_name = operand_expr.at("name");
        if(variables.count(var_name)){
            KomuValue curr_kv = variables.at(var_name);
            double origValue = std::get<double>(curr_kv.value);
            if(op == "++"){
                variables[var_name] = KomuValue(origValue + 1);
                return KomuValue(origValue + 1);
            } else if(op == "--"){
                variables[var_name] = KomuValue(origValue - 1);
                return KomuValue(origValue - 1);
            }

        }
         else {
            throw std::runtime_error("Error: Unknown unary operator '" + op + "'at line: " + std::to_string(line) + ".");
        }
    }
    else if(type == "PostfixUnaryOp"){
        std::string op = expr.at("operator");
        json operand_expr = expr.at("node");
        std::string var_name = operand_expr.at("name");
        if(variables.count(var_name)){
            KomuValue curr_kv = variables.at(var_name);
            double origValue = std::get<double>(curr_kv.value);
            if(op == "++"){
                variables[var_name] = KomuValue(origValue + 1);
                return KomuValue(origValue);
            } else if(op == "--"){
                variables[var_name] = KomuValue(origValue - 1);
                return KomuValue(origValue);
            }
        }
         else {
            throw std::runtime_error("Error: Unknown postfix unary operator '" + op + "'at line: " + std::to_string(line) + ".");
        }
    }
    else if(type == "Number"){
        return KomuValue(expr.at("value").get<double>());
    }else if(type == "MissionCall"){
        execute_mission_call(expr);
        return last_return_value;
    }
    else if(type == "Identifier"){
        std::string var_name = expr.at("name");
        if(variables.count(var_name)) {
            return variables.at(var_name);
        } else{
            throw std::runtime_error("Error: Undefined variable '" + var_name + "' at line: " + std::to_string(line) + ".");
        }
        
    }else if(type == "String"){
        return KomuValue(expr.at("value").get<std::string>());
    }

   else if(type == "BinaryOp"){
        std::string op = expr.at("operator").get<std::string>();
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");
        
        KomuValue left_kv = evaluate_binary_expression(left_expr);
        KomuValue right_kv = evaluate_binary_expression(right_expr);
        
        if(std::holds_alternative<double>(left_kv.value) && std::holds_alternative<double>(right_kv.value)){
            double left_value = std::get<double>(left_kv.value);
            double right_value = std::get<double>(right_kv.value);

            // Handle all numeric operators
            if(op == "+"){
                return KomuValue(left_value + right_value);
            } else if(op == "-"){
                return KomuValue(left_value - right_value);
            } else if(op == "*"){
                return KomuValue(left_value * right_value);
            } else if(op == "/"){
                if (right_value == 0) {
                    throw std::runtime_error("Error: Division by zero, at line: " + std::to_string(line) + ".");
                }
                return KomuValue(left_value / right_value);
            } else {
                throw std::runtime_error("Error: Unknown binary operator '" + op + "' for numbers.");
            }
        }
        
        else if(std::holds_alternative<std::string>(left_kv.value) && std::holds_alternative<std::string>(right_kv.value)){
            std::string left_str = std::get<std::string>(left_kv.value);
            std::string right_str = std::get<std::string>(right_kv.value);

            if(op == "+"){
                return KomuValue(left_str + right_str);
            } else {
                throw std::runtime_error("Error: Operator '" + op + "' cannot be applied to strings.");
            }
        }
        else {
            throw std::runtime_error("Error: Type mismatch for operator '" + op + "'. Cannot mix numbers, strings, or booleans. at line: " + std::to_string(line) + ".");
        }
    }else{
        throw std::runtime_error("Error: Cannot evaluate unhandled expression type '" + type + "' at line: " + std::to_string(line) + ".");
    }
    return KomuValue();
}

KomuValue Interpreter::evaluate_relational_expression(const json& expr){
    std::string type = expr.at("type");
    std::string str_var_value;
    if(type == "UnaryOp"){
        std::string op = expr.at("operator").get<std::string>();
        json operand_expr = expr.at("node");
        if(op == "!"){
            KomuValue operand_value = evaluate_relational_expression(operand_expr);
            return KomuValue(!std::get<bool>(operand_value.value));
        }else{
            return evaluate_binary_expression(expr);
        }
    } else if(type == "Boolean"){

        return KomuValue(expr.at("value").get<bool>());

    }else if(type == "Identifier"){
        std::string var_name = expr.at("name");
        if(variables.count(var_name)) {
            return variables.at(var_name);
        } 
        else{
            std::cerr << "Error: Undefined boolean variable " << var_name << std::endl;
            return KomuValue();
        }
        
    }
    else if(type == "RelationalOp"){
        std::string op = expr.at("operator").get<std::string>();
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");

        KomuValue left_kv = evaluate_binary_expression(left_expr);
        KomuValue right_kv = evaluate_binary_expression(right_expr);

        if (std::holds_alternative<double>(left_kv.value) && std::holds_alternative<double>(right_kv.value)) {
            double left_value = std::get<double>(left_kv.value);
            double right_value = std::get<double>(right_kv.value);
            
            if (op == "==") { return KomuValue(left_value == right_value); }
            if (op == "!=") { return KomuValue(left_value != right_value); }
            if (op == "<")  { return KomuValue(left_value < right_value); }
            if (op == "<=") { return KomuValue(left_value <= right_value); }
            if (op == ">")  { return KomuValue(left_value > right_value); }
            if (op == ">=") { return KomuValue(left_value >= right_value); }
            throw std::runtime_error("Error: Unknown relational operator '" + op + "' for numbers.");
        }

        else if (std::holds_alternative<std::string>(left_kv.value) && std::holds_alternative<std::string>(right_kv.value)) {
            std::string left_str = std::get<std::string>(left_kv.value);
            std::string right_str = std::get<std::string>(right_kv.value);

            if (op == "==") { return KomuValue(left_str == right_str); }
            if (op == "!=") { return KomuValue(left_str != right_str); }
            throw std::runtime_error("Error: Operator '" + op + "' cannot be applied to strings.");
        }
        
        else if (std::holds_alternative<bool>(left_kv.value) && std::holds_alternative<bool>(right_kv.value)) {
            bool left_bool = std::get<bool>(left_kv.value);
            bool right_bool = std::get<bool>(right_kv.value);

            if (op == "==") { return KomuValue(left_bool == right_bool); }
            if (op == "!=") { return KomuValue(left_bool != right_bool); }
            throw std::runtime_error("Error: Operator '" + op + "' cannot be applied to booleans.");
        }

        else {
            if (op == "==") { return KomuValue(false); }
            if (op == "!=") { return KomuValue(true); }
            throw std::runtime_error("Error: Type mismatch for relational operator '" + op + "'.");
        }
    }else{
        return evaluate_binary_expression(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled boolean expression type " + type + ".");
}

KomuValue Interpreter::evaluate_bitwise_and(const json& expr){
    std::string type = expr.at("type");
    if(type == "BitwiseOp" && expr.at("operator").get<std::string>() == "&"){
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");
        
        KomuValue left_kv = evaluate_bitwise_and(left_expr);
        KomuValue right_kv = evaluate_bitwise_and(right_expr);

        double left_value = std::get<double>(left_kv.value);
        double right_value = std::get<double>(right_kv.value);

        int left_int = static_cast<int>(left_value);
        int right_int = static_cast<int>(right_value);

       
        return KomuValue(static_cast<double>(left_int & right_int));

    } else{
        return evaluate_relational_expression(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled bitwise expression type '" + type + "'.");
}

KomuValue Interpreter::evaluate_bitwise_xor(const json& expr){
    std::string type = expr.at("type");
    if(type == "BitwiseOp" && expr.at("operator").get<std::string>() == "^"){
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");
        
        KomuValue left_kv = evaluate_bitwise_xor(left_expr);
        KomuValue right_kv = evaluate_bitwise_xor(right_expr);

        double left_value = std::get<double>(left_kv.value);
        double right_value = std::get<double>(right_kv.value);

        int left_int = static_cast<int>(left_value);
        int right_int = static_cast<int>(right_value);

       
        return KomuValue(static_cast<double>(left_int ^ right_int));

    } else{
        return evaluate_bitwise_and(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled bitwise expression type '" + type + "'.");
}

KomuValue Interpreter::evaluate_bitwise_or(const json& expr){
    std::string type = expr.at("type");
    if(type == "BitwiseOp" && expr.at("operator").get<std::string>() == "|"){
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");
        
        KomuValue left_kv = evaluate_bitwise_or(left_expr);
        KomuValue right_kv = evaluate_bitwise_or(right_expr);

        double left_value = std::get<double>(left_kv.value);
        double right_value = std::get<double>(right_kv.value);

        int left_int = static_cast<int>(left_value);
        int right_int = static_cast<int>(right_value);

       
        return KomuValue(static_cast<double>(left_int | right_int));

    } else{
        return evaluate_bitwise_xor(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled bitwise expression type '" + type + "'.");
}

KomuValue Interpreter::evaluate_logical_and(const json& expr){
    std::string type = expr.at("type");
    if(type == "LogicalOp" && expr.at("operator").get<std::string>() == "&&"){
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");

        KomuValue left_kv = evaluate_logical_and(left_expr);
        KomuValue right_kv = evaluate_logical_and(right_expr);
        
        bool left_value = std::get<bool>(left_kv.value);
        bool right_value = std::get<bool>(right_kv.value);
       
        return KomuValue(left_value && right_value);

    } else{
        return evaluate_bitwise_or(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled bitwise expression type '" + type + "'.");
}

KomuValue Interpreter::evaluate_logical_or(const json& expr){
    std::string type = expr.at("type");
    double line = expr.at("line");
    if(type == "LogicalOp" && expr.at("operator").get<std::string>() == "||"){
        json left_expr = expr.at("left");
        json right_expr = expr.at("right");
        
        KomuValue left_kv = evaluate_logical_or(left_expr);
        KomuValue right_kv = evaluate_logical_or(right_expr);
        
        bool left_value = std::get<bool>(left_kv.value);
        bool right_value = std::get<bool>(right_kv.value);
       
        return KomuValue(left_value || right_value);

    } else{
        return evaluate_logical_and(expr);
    }

    throw std::runtime_error("Error: Cannot evaluate unhandled bitwise expression type " + type + " at line: " + std::to_string(line) + ".");
}

void Interpreter::print_value(const KomuValue& kv){
    if(std::holds_alternative<double>(kv.value)){
        std::cout << std::get<double>(kv.value);
    } else if(std::holds_alternative<std::string>(kv.value)){
        std::string arg_value = std::get<std::string>(kv.value);
        std::string processed_str;

            for(size_t i = 0; i < arg_value.length(); ++i){
                if(arg_value[i] == '\\' && i + 1 < arg_value.length()){
                    char next_char = arg_value[i + 1];
                    if(next_char == 'n'){
                        processed_str += '\n';
                        ++i;
                    } else if(next_char == 't'){
                        processed_str += '\t';
                        ++i;
                    } else{
                        processed_str += arg_value[i];
                    }
                } else{
                    processed_str += arg_value[i];
                }
            }
            std::cout << processed_str;

    } else if(std::holds_alternative<bool>(kv.value)){
        std::cout << (std::get<bool>(kv.value) ? "true" : "false");
    } else{
        std::cout << "nil";
    }
}
void Interpreter::print(const json& args){
    for (const auto& arg_node : args){
        try{
            KomuValue result = evaluate_logical_or(arg_node);
            print_value(result);
        }catch(const std::runtime_error& e){
            std::cerr << "Runtime Error during print: " << e.what() << std::endl;
        }   
    }
}

/**
* @brief Handles execution of mission identifiers.
*/

void Interpreter::execute_mission(const json& node) {
    std::string mission_name = node.at("identifier");

    KomuMission mission;
    mission.name = mission_name;
    mission.body = node.at("body"); 

    if (node.contains("parameter")) {
        json param_list = node.at("parameter");
        for (const auto& param_node : param_list) {
            if (param_node.at("type") == "Identifier") {
                mission.parameters.push_back(param_node.at("name"));
            } 
            else {
                throw std::runtime_error("Error: Function parameters must be identifiers.");
            }
        }
    }
    missions[mission_name] = mission;
    
    std::cout << "Defined Mission: " << mission_name << std::endl;
}

void Interpreter::execute_return_statement(const json& node) {
    json value_node = node.at("value");
    KomuValue return_value = evaluate_logical_or(value_node);
    throw ReturnException(return_value);
}



/**
 * @brief Handles execution missions
 */

void Interpreter::execute_mission_call(const json& node) {
    std::string mission_name = node.at("identifier");

    if (mission_name == "log") {
        if (node.contains("argument")) {
            print(node.at("argument"));
        }
        return;
    } else if (mission_name == "logln") {
        if (node.contains("argument")) {
            print(node.at("argument"));
        }
        std::cout << std::endl;
        return;
    } else if (mission_name == "input") {
        std::string user_input;
        std::getline(std::cin, user_input);
        last_return_value = KomuValue(user_input); 
        return;
    }

    if (missions.count(mission_name) == 0) {
        throw std::runtime_error("Error: Calling undefined mission '" + mission_name + "'.");
    }
    KomuMission mission = missions.at(mission_name);
    json arg_list;
    if (node.contains("argument")) {
        arg_list = node.at("argument");
    }

    if (arg_list.size() != mission.parameters.size()) {
        throw std::runtime_error("Error: Mission '" + mission_name + "' expected " + 
                                 std::to_string(mission.parameters.size()) + 
                                 " arguments, but got " + std::to_string(arg_list.size()) + ".");
    }

    std::map<std::string, KomuValue> old_variables = variables;
    variables.clear(); 

    for (size_t i = 0; i < mission.parameters.size(); ++i) {
        std::string param_name = mission.parameters[i];
        json arg_node = arg_list[i];
        
        std::map<std::string, KomuValue> local_scope_temp = variables;
        variables = old_variables; 
        KomuValue arg_value = evaluate_logical_or(arg_node);
        variables = local_scope_temp; 

        variables[param_name] = arg_value;
    }

    try {
        for (const auto& stmt : mission.body) {
            execute_statement(stmt);
        }
    } catch (const ReturnException& e) {
        last_return_value = e.returnValue;
    } catch (const std::runtime_error& e) {
        variables = old_variables;
        throw e;
    }
    variables = old_variables;
}


/** 
* @brief Handles variable declaration and assignment.
*/

void Interpreter::execute_var_declaration(const json& node){
    std::string var_name = node.at("identifier");           
    json value_node = node.at("value");
    std::string value_type = value_node.at("type");
    try{
        KomuValue value = evaluate_logical_or(value_node);
        variables[var_name] = value;
        // std::cout << "Declared Variable: " << var_name << " = ";
        // print_value(value);
        // std::cout << std::endl;
    }catch(std::runtime_error& e){
        std::cerr << "Runtime Error during variable declaration: " << e.what() << std::endl;
    }
    
    
}


void Interpreter::execute_conditional(const json& node){
    json if_node = node.at("if");
    json if_condition = if_node.at("condition");
    KomuValue condition_kv = evaluate_logical_or(if_condition);
    bool condition_result = std::get<bool>(condition_kv.value);
    if(condition_result){
        json then_block = if_node.at("body");
        for(const auto& stmt : then_block){
            execute_statement(stmt);
        }
    } else if(node.contains("else_if")){
        json else_if_block = node.at("else_if");
        for(const auto& stmt : else_if_block){
            json condition = stmt.at("condition");
            KomuValue else_if_kv = evaluate_logical_or(condition);
            bool else_if_result = std::get<bool>(else_if_kv.value);
            if(else_if_result){
                json body = stmt.at("body");
                for(const auto& inner_stmt : body){
                    execute_statement(inner_stmt);
                }
                break;
            }
        }
    }else if(node.contains("else")){
        json else_block = node.at("else");
        for(const auto& stmt : else_block){
            execute_statement(stmt);
        }
    }
}

void Interpreter::execute_while_loop(const json& node){
    json condition_node = node.at("condition");
    json body_node = node.at("body");
    while(std::get<bool>(evaluate_logical_or(condition_node).value)){
        for(const auto& stmt : body_node){
            execute_statement(stmt);
        }
    }
}

/**
* @brief Executes a given statement node.
*/

void Interpreter::execute_statement(const json& stmt){
    std::string stmt_type = stmt.at("type");
    if(stmt_type == "Var"){
        execute_var_declaration(stmt);
    }
    else if(stmt_type == "Mission"){
        execute_mission(stmt);
    }else if(stmt_type == "MissionCall"){
        execute_mission_call(stmt);
    }else if(stmt_type == "Conditional"){
        execute_conditional(stmt);
    } else if(stmt_type == "While"){
        execute_while_loop(stmt);
    }else if(stmt_type == "Return"){
        execute_return_statement(stmt);
    }else{
        try{
            evaluate_logical_or(stmt);
        }catch(std::runtime_error& e){
            std::cerr << "Runtime Error during statement execution: " << e.what() << std::endl;
        }
    }
}

/**
 * @brief Interprets the entire AST represented in JSON format.
 */

void Interpreter::interpret(const json& ast_data){
    std::cout << "Starting AST Interpreter..." << std::endl;
    try{
        for(const auto& node : ast_data){
            execute_statement(node);
        }
    }
    catch(const std::runtime_error& e){
        std::cerr << "Runtime Error: " << e.what() << std::endl;
    }
//    std::cout << "End of Program\n Summary:" << std::endl;
    
//     std::cout << "Variables:" << std::endl;
//     for(const auto& pair : variables){
//         std::cout << "\t" << pair.first << " = ";
//         print_value(pair.second); 
//         std::cout << std::endl;
//     }

//     std::cout << "Missions:" << std::endl;
//     for(const auto& pair : missions){
//         std::cout << "\t" << pair.first << " (" << pair.second.parameters.size() << " params)" << std::endl;
//     }

}