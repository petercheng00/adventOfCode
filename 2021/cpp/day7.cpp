#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

std::vector<int> loadInput(const std::vector<std::string>& input_lines)
{
  std::vector<int> positions;
  std::stringstream ss(input_lines[0]);
  int x;
  char comma;
  while (!ss.eof())
  {
    // Last comma doesn't exist, but that doesn't affect anything.
    ss >> x >> comma;
    positions.push_back(x);
  }
  return positions;
}

void day1(const std::vector<std::string>& input_lines)
{
  // Use the median.
  std::vector<int> positions = loadInput(input_lines);

  std::nth_element(positions.begin(), positions.begin() + positions.size() / 2,
                   positions.end());
  int median = positions[positions.size() / 2];

  int sum_distances = 0;
  for (int p : positions)
  {
    sum_distances += std::abs(p - median);
  }
  std::cout << sum_distances << "\n";
}

int getFuelUsage(const std::vector<int>& positions, int target)
{
  int fuel_usage = 0;
  for (int p : positions)
  {
    int distance = std::abs(p - target);
    fuel_usage += distance * (distance + 1) * 0.5;
  }
  return fuel_usage;
}

void day2(const std::vector<std::string>& input_lines)
{
  // Use nothing clever and just brute force.
  std::vector<int> positions = loadInput(input_lines);
  const auto [min_it, max_it] =
      std::minmax_element(positions.begin(), positions.end());
  int min_fuel_usage = std::numeric_limits<int>::max();
  for (int x = *min_it; x <= *max_it; ++x)
  {
    int fuel_usage = getFuelUsage(positions, x);
    min_fuel_usage = std::min(min_fuel_usage, fuel_usage);
  }
  std::cout << min_fuel_usage << "\n";
}

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
