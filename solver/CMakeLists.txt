# Specify the required C++ version necessary for the project to be compiled.
cmake_minimum_required(VERSION 3.10)

# set project name
project(project VERSION 1.0)

# Set the C++ version standard for the program
set(CMAKE_CXX_STANDARD 17)
# Make the C++ standard set above oblicatory
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(GCC_COVERATE_LINK_FLAGS "-lrt")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERATE_LINK_FLAGS}")
# add the executeable(s) (".cpp" files)
add_executable(project src/main.cpp src/State.cpp src/Position.cpp src/SokobanSolver.cpp)


target_link_libraries( project ${OpenCV_LIBS} )

