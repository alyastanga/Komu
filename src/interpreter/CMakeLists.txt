add_library(komu_lib 
    src/interpreter.cpp
)

target_include_directories(komu_lib
    PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party
)

add_executable(komu 
    src/main.cpp
)

target_link_libraries(komu 
    PRIVATE komu_lib
)
