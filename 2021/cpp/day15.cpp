#include <fstream>
#include <iostream>
#include <string>
#include <tuple>
#include <vector>

struct RowCol
{
  int row;
  int col;
};

const std::vector<RowCol> NEIGHBORS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

std::tuple<int, int, int> get_min_unvisted_distance(
    const std::vector<std::vector<int>>& distances,
    const std::vector<std::vector<uint8_t>>& visited)
{
  int min_row = -1;
  int min_col = -1;
  int min_distance = std::numeric_limits<int>::max();
  for (int row = 0; row < int(distances.size()); ++row)
  {
    for (int col = 0; col < int(distances[row].size()); ++col)
    {
      if (!visited[row][col] && distances[row][col] < min_distance)
      {
        min_row = row;
        min_col = col;
        min_distance = distances[row][col];
      }
    }
  }
  return std::make_tuple(min_row, min_col, min_distance);
}

void day1(const std::vector<std::vector<int>>& risks)
{
  // This is just dijkstra's.
  const int rows = risks.size();
  const int cols = risks[0].size();
  RowCol start{0, 0};
  RowCol end{rows - 1, cols - 1};

  std::vector<std::vector<uint8_t>> visited(rows,
                                            std::vector<uint8_t>(cols, false));
  std::vector<std::vector<int>> distances(
      rows, std::vector<int>(cols, std::numeric_limits<int>::max()));
  distances[start.row][start.col] = 0;

  while (true)
  {
    auto [row, col, distance] = get_min_unvisted_distance(distances, visited);
    if (row == end.row && col == end.col)
    {
      std::cout << distance << "\n";
      return;
    }
    visited[row][col] = true;
    for (const auto& offset : NEIGHBORS)
    {
      int row2 = row + offset.row;
      int col2 = col + offset.col;
      if (row2 < 0 || row2 >= rows || col2 < 0 || col2 >= cols)
      {
        continue;
      }
      if (visited[row2][col2])
      {
        continue;
      }
      distances[row2][col2] =
          std::min(distances[row2][col2], distance + risks[row2][col2]);
    }
  }
}
void day2(const std::vector<std::vector<int>>& risks)
{
  // Let's just try running day1 with a way bigger map?
  const int rows = risks.size();
  const int cols = risks[0].size();
  const int scale = 5;
  const int big_rows = scale * rows;
  const int big_cols = scale * cols;
  std::vector<std::vector<int>> big_risks(big_rows, std::vector<int>(big_cols));
  for (int row_copy = 0; row_copy < scale; ++row_copy)
  {
    int start_row = row_copy * rows;
    for (int col_copy = 0; col_copy < scale; ++col_copy)
    {
      int start_col = col_copy * cols;
      for (int row = 0; row < rows; ++row)
      {
        for (int col = 0; col < cols; ++col)
        {
          int value = risks[row][col] + row_copy + col_copy;
          value = ((value - 1) % 9) + 1;
          big_risks[start_row + row][start_col + col] = value;
        }
      }
    }
  }
  day1(big_risks);
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<std::vector<int>> risks;
  std::string line;
  while (std::getline(ifstream, line))
  {
    std::vector<int> risk_row(line.size());
    for (int i = 0; i < int(line.size()); ++i)
    {
      risk_row[i] = line[i] - '0';
    }
    risks.push_back(risk_row);
  }

  day1(risks);
  day2(risks);
}
