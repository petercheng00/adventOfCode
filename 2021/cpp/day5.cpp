#include <boost/functional/hash.hpp>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

struct Point
{
  int x;
  int y;
};

struct Line
{
  Point p1;
  Point p2;
};

bool isVertical(const Line& l) { return l.p1.x == l.p2.x; }

bool isHorizontal(const Line& l) { return l.p1.y == l.p2.y; }

std::vector<Line> load_lines(const std::vector<std::string>& input_lines)
{
  std::vector<Line> lines;
  lines.reserve(input_lines.size());
  for (const auto& line : input_lines)
  {
    std::stringstream ss(line);
    int x1, y1, x2, y2;
    char comma;
    std::string arrow;
    ss >> x1 >> comma >> y1 >> arrow >> x2 >> comma >> y2;
    lines.push_back({{x1, y1}, {x2, y2}});
  }
  return lines;
}

void day1(const std::vector<std::string>& input_lines)
{
  auto lines = load_lines(input_lines);
  std::unordered_map<std::pair<int, int>, int, boost::hash<std::pair<int, int>>>
      coverage_count;
  for (const auto& line : lines)
  {
    if (isVertical(line))
    {
      for (int y = std::min(line.p1.y, line.p2.y);
           y <= std::max(line.p1.y, line.p2.y); ++y)
      {
        coverage_count[std::make_pair(line.p1.x, y)] += 1;
      }
    }
    else if (isHorizontal(line))
    {
      for (int x = std::min(line.p1.x, line.p2.x);
           x <= std::max(line.p1.x, line.p2.x); ++x)
      {
        coverage_count[std::make_pair(x, line.p1.y)] += 1;
      }
    }
  }
  int num_overlapping_points = 0;
  for (const auto& cc_iter : coverage_count)
  {
    if (cc_iter.second > 1)
    {
      ++num_overlapping_points;
    }
  }
  std::cout << num_overlapping_points << "\n";
}

void day2(const std::vector<std::string>& input_lines)
{
  auto lines = load_lines(input_lines);
  std::unordered_map<std::pair<int, int>, int, boost::hash<std::pair<int, int>>>
      coverage_count;
  for (const auto& line : lines)
  {
    int x_step = line.p2.x - line.p1.x;
    x_step = (x_step != 0) ? x_step / std::abs(x_step) : 0;
    int y_step = line.p2.y - line.p1.y;
    y_step = (y_step != 0) ? y_step / std::abs(y_step) : 0;
    int x = line.p1.x;
    int y = line.p1.y;
    while (true)
    {
      coverage_count[std::make_pair(x, y)] += 1;
      x += x_step;
      y += y_step;
      if (x == line.p2.x && y == line.p2.y)
      {
        coverage_count[std::make_pair(x, y)] += 1;
        break;
      }
    }
  }
  int num_overlapping_points = 0;
  for (const auto& cc_iter : coverage_count)
  {
    if (cc_iter.second > 1)
    {
      ++num_overlapping_points;
    }
  }
  std::cout << num_overlapping_points << "\n";
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
