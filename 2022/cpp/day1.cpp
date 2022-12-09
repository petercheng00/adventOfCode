#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

int day1(const std::string& input_filename)
{
  std::ifstream ifstream(input_filename);
  int max_calories = 0;
  int current_calories = 0;
  std::string line;
  while (std::getline(ifstream, line))
  {
    if (line == "")
    {
      max_calories = std::max(max_calories, current_calories);
      current_calories = 0;
      continue;
    }
    current_calories += std::stoi(line);
  }
  max_calories = std::max(max_calories, current_calories);
  return max_calories;
}

int day2(const std::string& input_filename)
{
  std::ifstream ifstream(input_filename);
  std::vector<int> calories(1);
  std::string line;
  while (std::getline(ifstream, line))
  {
    if (line == "")
    {
      calories.push_back(0);
      continue;
    }
    calories.back() += std::stoi(line);
  }
  std::sort(calories.begin(), calories.end(), std::greater<int>());
  return std::accumulate(calories.begin(), calories.begin() + 3, 0);
}

int main(int argc, char* argv[])
{
  assert(argc == 2);
  std::cout << day1(argv[1]) << "\n";
  std::cout << day2(argv[1]) << "\n";
}
