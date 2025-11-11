#ifndef KOMU_INTERPRETER_HPP
#define KOMU_INTERPRETER_HPP

#include <string>
#include <map>
#include <vector>
#include "json.hpp"
#include "KomuValue.hpp"

using json = nlohmann::json;

class ReturnException : public std::exception {
public:
    KomuValue returnValue;

    // Constructor: This takes the return value as a parameter
    ReturnException(const KomuValue& value) : returnValue(value) {}

    const char* what() const noexcept override {
        return "A 'return' statement was executed.";
    }
};

struct KomuMission{
    std::string name;
    std::vector<std::string> parameters;
    json body;
};

class Interpreter {
    public:
        Interpreter() = default;
        void interpret(const json& ast_data);
    
    private:
        std::map<std::string, KomuValue> variables;
        std::map<std::string, KomuMission> missions;

        
        void execute_statement(const json& stmt);
        void execute_var_declaration(const json& node);
        void execute_mission(const json& node);
        void print_value(const KomuValue& kv);
        void print(const json& args);
        void execute_mission_call(const json& node);
        void execute_conditional(const json& node);
        void execute_while_loop(const json& node);
        void execute_return_statement(const json& node);

        KomuValue last_return_value;

        KomuValue evaluate_binary_expression(const json& expr);
        KomuValue evaluate_relational_expression(const json& expr);

        KomuValue evaluate_bitwise_and(const json& expr);
        KomuValue evaluate_bitwise_or(const json& expr);
        KomuValue evaluate_bitwise_xor(const json& expr);

        KomuValue evaluate_logical_and(const json& expr);
        KomuValue evaluate_logical_or(const json& expr);






};

#endif // KOMU_INTERPRETER_HPP
