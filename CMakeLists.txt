cmake_minimum_required(VERSION 3.1...3.5)
project(ice-puzzle CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE Release)
add_executable(
    main 
    ./main.cpp 
    ./modules/MazeGenerator/MazeGenerator.cpp 
    ./modules/MazeSolver/MazeSolver.cpp 
    ./modules/Vec2/Vec2.cpp
)