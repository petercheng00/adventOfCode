#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

void day1(const std::vector<std::vector<int>>& heightmap)
{
  int rows = int(heightmap.size());
  int cols = int(heightmap[0].size());
  int risk_level = 0;
  for (int row = 0; row < rows; ++row)
  {
    for (int col = 0; col < cols; ++col)
    {
      int height = heightmap[row][col];
      if ((row == 0 || height < heightmap[row - 1][col]) &&
          (col == 0 || height < heightmap[row][col - 1]) &&
          (row == rows - 1 || height < heightmap[row + 1][col]) &&
          (col == cols - 1 || height < heightmap[row][col + 1]))
      {
        risk_level += (1 + height);
      }
    }
  }
  std::cout << risk_level << "\n";
}

int getBasinSize(const std::vector<std::vector<int>>& heightmap,
                 std::vector<std::vector<uint8_t>>& visited, int start_row,
                 int start_col)
{
  const int rows = heightmap.size();
  const int cols = heightmap[0].size();

  int size = 0;
  std::queue<std::pair<int, int>> to_explore;
  to_explore.push(std::make_pair(start_row, start_col));
  visited[start_row][start_col] = true;

  while (!to_explore.empty())
  {
    auto [row, col] = to_explore.front();
    to_explore.pop();
    size += 1;

    if (row > 0 && !visited[row - 1][col] && heightmap[row - 1][col] != 9)
    {
      to_explore.push(std::make_pair(row - 1, col));
      visited[row - 1][col] = true;
    }
    if (row < rows - 1 && !visited[row + 1][col] &&
        heightmap[row + 1][col] != 9)
    {
      to_explore.push(std::make_pair(row + 1, col));
      visited[row + 1][col] = true;
    }
    if (col > 0 && !visited[row][col - 1] && heightmap[row][col - 1] != 9)
    {
      to_explore.push(std::make_pair(row, col - 1));
      visited[row][col - 1] = true;
    }
    if (col < cols - 1 && !visited[row][col + 1] &&
        heightmap[row][col + 1] != 9)
    {
      to_explore.push(std::make_pair(row, col + 1));
      visited[row][col + 1] = true;
    }
  }

  return size;
}
void day2(const std::vector<std::vector<int>>& heightmap)
{
  // Based on problem constraints, seems like this is just find connected
  // components separated by 9s.
  // Track which spots have been processed.
  std::vector<std::vector<uint8_t>> visited(heightmap.size());
  for (int row = 0; row < int(heightmap.size()); ++row)
  {
    visited[row] = std::vector<uint8_t>(heightmap[row].size(), false);
  }

  std::vector<int> basin_sizes;
  for (int row = 0; row < int(heightmap.size()); ++row)
  {
    for (int col = 0; col < int(heightmap[row].size()); ++col)
    {
      if (heightmap[row][col] == 9 || visited[row][col])
      {
        continue;
      }
      basin_sizes.push_back(getBasinSize(heightmap, visited, row, col));
    }
  }
  std::nth_element(basin_sizes.begin(), basin_sizes.begin() + 2,
                   basin_sizes.end(), std::greater());
  std::cout << basin_sizes[0] * basin_sizes[1] * basin_sizes[2] << "\n";
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<std::vector<int>> heightmap;
  std::string line;
  while (std::getline(ifstream, line))
  {
    std::vector<int> heightrow(line.size());
    for (int i = 0; i < int(line.size()); ++i)
    {
      heightrow[i] = line[i] - '0';
    }
    heightmap.push_back(heightrow);
  }

  day1(heightmap);
  day2(heightmap);
}
