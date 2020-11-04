# specify the required C++ version necessary for the project to be compiled
cmake_minimum_required(VERSION 3.10)

# set project name
project(solver VERSION 1.0)

# set the C++ version standard for the program
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# project configuration
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS_DEBUG_INIT "-Wall")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

# add the executeable(s) (".cpp" files)
add_executable(solver src/main.cpp src/State.cpp src/Position.cpp src/SokobanSolver.cpp)