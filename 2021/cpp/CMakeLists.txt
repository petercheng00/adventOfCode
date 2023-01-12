cmake_minimum_required(VERSION 3.16.3)

project(AdventOfCode)

set(CMAKE_BUILD_TYPE "RelWithDebInfo")
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(day1 day1.cpp)
add_executable(day3 day3.cpp)
add_executable(day5 day5.cpp)
add_executable(day7 day7.cpp)
add_executable(day9 day9.cpp)
add_executable(day11 day11.cpp)
add_executable(day13 day13.cpp)
