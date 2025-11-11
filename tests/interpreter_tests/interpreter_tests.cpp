#include "interpreter.hpp"
#include "json.hpp"
#include "gtest/gtest.h"

using json = nlohmann::json;

class InterpreterTest : public ::testing::Test
{
  protected:
    void SetUp() override { interpreter = Interpreter(); }

    Interpreter interpreter;
};

TEST_F(InterpreterTest, HandlesEmptyAST)
{
    json empty_ast = json::array();
    ASSERT_NO_THROW(interpreter.interpret(empty_ast));
}

TEST_F(InterpreterTest, HandlesSimpleArithmetic)
{
    json arithmetic_ast = R"(
    [
        {
            "line": 1,
            "type": "Var",
            "identifier": "x",
            "value": {
                "line": 1,
                "type": "BinaryOp",
                "operator": "+",
                "left": {
                    "line": 1,
                    "type": "BinaryOp",
                    "operator": "*",
                    "left": {
                        "line": 1,
                        "type": "Number",
                        "value": 5
                    },
                    "right": {
                        "line": 1,
                        "type": "Number",
                        "value": 2
                    }
                },
                "right": {
                    "line": 1,
                    "type": "Number",
                    "value": 2
                }
            }
        }
    ]
    )"_json;

    interpreter.interpret(arithmetic_ast);
    ASSERT_TRUE(true);
}

TEST_F(InterpreterTest, HandlesVariableAssignment)
{
    // ...
}

TEST_F(InterpreterTest, HandlesConditionalIf)
{
    // ...
}
