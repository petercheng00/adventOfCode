#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Point
{
  int x;
  int y;
  auto operator<=>(const Point&) const = default;
};

struct Fold
{
  char axis;
  int value;
};

std::vector<Point> doFold(const Fold& fold, const std::vector<Point>& in_points)
{
  std::vector<Point> out_points;
  out_points.reserve(in_points.size());
  for (const auto& pt : in_points)
  {
    if (fold.axis == 'x' && pt.x > fold.value)
    {
      Point new_pt{fold.value - (pt.x - fold.value), pt.y};
      if (std::find(out_points.begin(), out_points.end(), new_pt) ==
          out_points.end())
      {
        out_points.push_back(new_pt);
      }
    }
    else if (fold.axis == 'y' && pt.y > fold.value)
    {
      Point new_pt{pt.x, fold.value - (pt.y - fold.value)};
      if (std::find(out_points.begin(), out_points.end(), new_pt) ==
          out_points.end())
      {
        out_points.push_back(new_pt);
      }
    }
    else
    {
      if (std::find(out_points.begin(), out_points.end(), pt) ==
          out_points.end())
      {
        out_points.push_back(pt);
      }
    }
  }

  return out_points;
}

void day1(const std::vector<Point>& points, const std::vector<Fold>& folds)
{
  std::cout << doFold(folds[0], points).size() << "\n";
}
void day2(const std::vector<Point>& in_points, const std::vector<Fold>& folds)
{
  std::vector<Point> points = in_points;
  for (const auto& fold : folds)
  {
    points = doFold(fold, points);
  }
  int min_x = points[0].x;
  int max_x = points[0].x;
  int min_y = points[0].y;
  int max_y = points[0].y;
  for (const auto [x, y] : points)
  {
    min_x = std::min(min_x, x);
    max_x = std::max(max_x, x);
    min_y = std::min(min_y, y);
    max_y = std::max(max_y, y);
  }
  for (int y = min_y; y <= max_y; ++y)
  {
    for (int x = min_x; x <= max_x; ++x)
    {
      if (std::find(points.begin(), points.end(), Point{x, y}) != points.end())
      {
        std::cout << "#";
      }
      else
      {
        std::cout << " ";
      }
    }
    std::cout << "\n";
  }
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<Point> points;
  std::vector<Fold> folds;
  for (std::string line; std::getline(ifstream, line);)
  {
    if (std::isdigit(line[0]))
    {
      int x, y;
      char comma;
      std::stringstream(line) >> x >> comma >> y;
      points.emplace_back(x, y);
    }
    else if (line[0] == 'f')
    {
      int equals_index = line.find("=");
      char axis = line[equals_index - 1];
      int value = std::stoi(line.substr(equals_index + 1));
      folds.emplace_back(axis, value);
    }
  }

  day1(points, folds);
  day2(points, folds);
}
