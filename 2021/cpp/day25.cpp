#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int doEastMoves(std::vector<std::string>& map)
{
  int rows = map.size();
  int cols = map[0].size();

  std::vector<std::string> next_map(map);
  int num_moves = 0;
  for (int row = 0; row < rows; ++row)
  {
    for (int col = 0; col < cols; ++col)
    {
      if (map[row][col] == '>')
      {
        int dst_col = (col + 1) % cols;
        if (map[row][dst_col] == '.')
        {
          next_map[row][col] = '.';
          next_map[row][dst_col] = '>';
          ++num_moves;
        }
      }
    }
  }

  std::swap(map, next_map);
  return num_moves;
}

int doSouthMoves(std::vector<std::string>& map)
{
  int rows = map.size();
  int cols = map[0].size();

  std::vector<std::string> next_map(map);
  int num_moves = 0;
  for (int row = 0; row < rows; ++row)
  {
    for (int col = 0; col < cols; ++col)
    {
      if (map[row][col] == 'v')
      {
        int dst_row = (row + 1) % rows;
        if (map[dst_row][col] == '.')
        {
          next_map[row][col] = '.';
          next_map[dst_row][col] = 'v';
          ++num_moves;
        }
      }
    }
  }

  std::swap(map, next_map);
  return num_moves;
}

void day1(const std::vector<std::string>& orig_map)
{
  auto map = orig_map;

  for (int step = 1;; ++step)
  {
    int total_moves = 0;
    total_moves += doEastMoves(map);
    total_moves += doSouthMoves(map);
    if (total_moves == 0)
    {
      std::cout << step << "\n";
      return;
    }
  }
}

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
