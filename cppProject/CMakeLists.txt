cmake_minimum_required(VERSION 4.1)
project(cppProject)

set(CMAKE_CXX_STANDARD 14)

include_directories(src/domain)

add_executable(cppProject
        src/domain/DirectedGraph.cpp
        src/domain/DirectedGraph.h
        src/main.cpp)
