#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int simulate_step(std::vector<std::vector<int>>& state)
{
  const int rows = state.size();
  const int cols = state[0].size();
  // First all values go up by 1.
  for (auto& row : state)
  {
    for (auto& x : row)
    {
      x += 1;
    }
  }

  // Repeatedly search for any flashes that need to occur, until stabilized.
  // Track which flashes have occurred already so we don't infinitely loop.
  std::vector<std::vector<uint8_t>> flashed(state.size());
  {
    for (int i = 0; i < state.size(); ++i)
    {
      flashed[i] = std::vector<uint8_t>(state[i].size(), false);
    }
  }

  int num_flashes = 0;
  while (true)
  {
    bool anything_flashed = false;
    for (int row = 0; row < rows; ++row)
    {
      for (int col = 0; col < cols; ++col)
      {
        if (state[row][col] > 9 && !flashed[row][col])
        {
          // This one flashes.
          ++num_flashes;
          anything_flashed = true;
          flashed[row][col] = true;

          // Update neighboring values.
          for (int row2 = row - 1; row2 <= row + 1; ++row2)
          {
            for (int col2 = col - 1; col2 <= col + 1; ++col2)
            {
              if (row2 >= 0 && row2 < rows && col2 >= 0 && col2 < cols)
              {
                ++state[row2][col2];
              }
            }
          }
        }
      }
    }

    if (!anything_flashed)
    {
      break;
    }
  }

  // Now anything that flashed goes back to zero.
  for (auto& row : state)
  {
    for (auto& x : row)
    {
      if (x > 9)
      {
        x = 0;
      }
    }
  }

  return num_flashes;
}

void day1(const std::vector<std::vector<int>>& energies)
{
  int num_flashes = 0;
  std::vector<std::vector<int>> state = energies;
  for (int i = 0; i < 100; ++i)
  {
    num_flashes += simulate_step(state);
  }
  std::cout << num_flashes << "\n";
}
void day2(const std::vector<std::vector<int>>& energies)
{
  std::vector<std::vector<int>> state = energies;
  for (int step = 0;; ++step)
  {
    int num_flashes = simulate_step(state);
    if (num_flashes == (energies.size() * energies[0].size()))
    {
      std::cout << step + 1 << "\n";
      return;
    }
  }
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<std::vector<int>> energies;
  std::string line;
  while (std::getline(ifstream, line))
  {
    std::vector<int> row(line.size());
    for (int i = 0; i < int(line.size()); ++i)
    {
      row[i] = line[i] - '0';
    }
    energies.push_back(row);
  }

  day1(energies);
  day2(energies);
}
