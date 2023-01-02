#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void day1(const std::vector<std::string>& input_lines) {}

void day2(const std::vector<std::string>& input_lines) {}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<std::string> lines;
  std::string line;
  while (std::getline(ifstream, line))
  {
    lines.push_back(line);
  }

  day1(lines);
  day2(lines);
}
