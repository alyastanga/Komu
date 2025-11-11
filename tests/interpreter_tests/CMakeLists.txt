add_executable(interpreter_tests
    interpreter_tests.cpp
)

target_link_libraries(interpreter_tests PRIVATE
    komu_lib    
    gtest_main  
)

add_test(
    NAME CppInterpreterTests
    COMMAND interpreter_tests
)