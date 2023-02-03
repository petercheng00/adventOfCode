cmake_minimum_required(VERSION 3.16.3)

project(AdventOfCode)

set(CMAKE_BUILD_TYPE "RelWithDebInfo")
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Eigen3 3.4 REQUIRED NO_MODULE)

add_executable(day1 day1.cpp)
add_executable(day3 day3.cpp)
add_executable(day5 day5.cpp)
add_executable(day7 day7.cpp)
add_executable(day9 day9.cpp)
add_executable(day11 day11.cpp)
add_executable(day13 day13.cpp)
add_executable(day15 day15.cpp)
add_executable(day17 day17.cpp)
add_executable(day19 day19.cpp)
target_link_libraries(day19 Eigen3::Eigen)
add_executable(day21 day21.cpp)
add_executable(day23 day23.cpp)
