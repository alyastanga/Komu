cmake_minimum_required(VERSION 3.20)

project(komu)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

enable_testing()

add_subdirectory(src/interpreter)

add_subdirectory(tests)