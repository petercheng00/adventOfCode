#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <vector>

// Each rock is defined based on occupied xy coordinates relative to bottom
// left. x is right, y is down.
const std::vector<std::pair<int, int>> ROCK_SHAPE0 = {
    {0, 0}, {1, 0}, {2, 0}, {3, 0}};

const std::vector<std::pair<int, int>> ROCK_SHAPE1 = {
    {1, 0}, {0, -1}, {1, -1}, {2, -1}, {1, -2}};

const std::vector<std::pair<int, int>> ROCK_SHAPE2 = {
    {0, 0}, {1, 0}, {2, 0}, {2, -1}, {2, -2}};

const std::vector<std::pair<int, int>> ROCK_SHAPE3 = {
    {0, 0}, {0, -1}, {0, -2}, {0, -3}};

const std::vector<std::pair<int, int>> ROCK_SHAPE4 = {
    {0, 0}, {1, 0}, {0, -1}, {1, -1}};

const std::vector<std::vector<std::pair<int, int>>> ROCK_SHAPES = {
    ROCK_SHAPE0, ROCK_SHAPE1, ROCK_SHAPE2, ROCK_SHAPE3, ROCK_SHAPE4};

const int WORLD_HEIGHT = 1000000;
const int WORLD_WIDTH = 7;

class Simulation
{
 public:
  Simulation(const std::vector<int>& jet_pattern)
      : jet_pattern_(jet_pattern),
        world_(WORLD_HEIGHT * WORLD_WIDTH),
        next_jet_pattern_index_(0),
        next_shape_index_(0),
        tower_height_(0)
  {
  }

  bool blockCanFit(int shape_index, int x, int y);
  void dropNextBlock();
  int getTowerHeight() const { return tower_height_; }

  std::string getStateString(int rows) const;

 private:
  uint8_t& worldAt(int x, int y) { return world_[y * WORLD_WIDTH + x]; }
  const uint8_t& worldAt(int x, int y) const
  {
    return world_[y * WORLD_WIDTH + x];
  }

  std::vector<uint8_t> world_;
  const std::vector<int> jet_pattern_;
  int next_jet_pattern_index_;
  int next_shape_index_;
  int tower_height_;
};

bool Simulation::blockCanFit(int shape_index, int x, int y)
{
  const auto& shape = ROCK_SHAPES[shape_index];
  for (const auto& xy : shape)
  {
    if (xy.first + x < 0 || xy.first + x >= WORLD_WIDTH || xy.second + y < 0 ||
        xy.second + y >= WORLD_HEIGHT)
    {
      // Out of bounds.
      return false;
    }
    if (worldAt(xy.first + x, xy.second + y))
    {
      // Hits an existing rock.
      return false;
    }
  }
  return true;
}

void Simulation::dropNextBlock()
{
  int shape_index = next_shape_index_;
  next_shape_index_ = (next_shape_index_ + 1) % ROCK_SHAPES.size();

  // Figure out where the block starts.
  int x = 2;
  int y = WORLD_HEIGHT - tower_height_ - 4;

  // Repeatedly go sideways and down.
  while (true)
  {
    int x_shift = jet_pattern_[next_jet_pattern_index_];
    next_jet_pattern_index_ =
        (next_jet_pattern_index_ + 1) % jet_pattern_.size();
    if (blockCanFit(shape_index, x + x_shift, y))
    {
      x += x_shift;
    }
    if (blockCanFit(shape_index, x, y + 1))
    {
      y += 1;
    }
    else
    {
      break;
    }
  }

  // Update the world.
  const auto& shape = ROCK_SHAPES[shape_index];
  for (const auto& xy : shape)
  {
    worldAt(xy.first + x, xy.second + y) = 1;
    int height = WORLD_HEIGHT - (xy.second + y);
    tower_height_ = std::max(height, tower_height_);
  }
}

std::string Simulation::getStateString(int rows) const
{
  std::string out = std::to_string(next_jet_pattern_index_) +
                    std::to_string(next_shape_index_);
  for (int row = WORLD_HEIGHT - tower_height_;
       row < rows + WORLD_HEIGHT - tower_height_; ++row)
  {
    for (int col = 0; col < WORLD_WIDTH; ++col)
    {
      out += std::to_string(worldAt(col, row));
    }
  }
  return out;
}

void part1(const std::vector<int>& jet_pattern)
{
  Simulation simulation(jet_pattern);
  for (int i = 0; i < 2022; ++i)
  {
    simulation.dropNextBlock();
  }
  std::cout << simulation.getTowerHeight() << "\n";
}

void part2(const std::vector<int>& jet_pattern)
{
  Simulation simulation(jet_pattern);
  const int state_string_rows = 10;
  std::unordered_map<std::string, std::pair<int, int>>
      state_to_blocks_and_height;
  int matching_state_numblocks1 = -1;
  int matching_state_numblocks2 = -1;
  int matching_state_height_change = -1;
  for (int num_blocks = 0; simulation.getTowerHeight() < 0.9 * WORLD_HEIGHT;
       ++num_blocks)
  {
    if (simulation.getTowerHeight() > state_string_rows)
    {
      auto state_string = simulation.getStateString(state_string_rows);
      if (state_to_blocks_and_height.find(state_string) !=
          state_to_blocks_and_height.end())
      {
        int past_num_blocks, past_height;
        std::tie(past_num_blocks, past_height) =
            state_to_blocks_and_height[state_string];
        matching_state_numblocks1 = past_num_blocks;
        matching_state_numblocks2 = num_blocks;
        matching_state_height_change =
            simulation.getTowerHeight() - past_height;

        std::cout << "Before we dropped " << past_num_blocks
                  << " blocks for a height of " << past_height << "\n";
        std::cout << "Now we've dropped " << num_blocks
                  << " blocks for a height of " << simulation.getTowerHeight()
                  << "\n";
        break;
      }
      state_to_blocks_and_height[state_string] =
          std::make_pair(num_blocks, simulation.getTowerHeight());
    }
    simulation.dropNextBlock();
  }

  int cycle_num_blocks = matching_state_numblocks2 - matching_state_numblocks1;
  std::cout << "Cycle num blocks is " << cycle_num_blocks << " and adds "
            << matching_state_height_change << " height\n";
  long target_num_blocks = 1000000000000;
  long remaining_after_numblocks1 =
      target_num_blocks - matching_state_numblocks1;
  int shortcut_remaining = remaining_after_numblocks1 % cycle_num_blocks;
  long shortcut_height_skipped =
      matching_state_height_change *
      (remaining_after_numblocks1 / cycle_num_blocks);
  int shortcut_target_num_blocks =
      matching_state_numblocks1 + shortcut_remaining;

  Simulation simulation2(jet_pattern);
  for (int i = 0; i < shortcut_target_num_blocks; ++i)
  {
    simulation2.dropNextBlock();
  }
  std::cout << shortcut_height_skipped + simulation2.getTowerHeight() << "\n";
}

int main(int argc, char* argv[])
{
  assert(argc == 2);
  std::ifstream ifstream(argv[1]);
  std::string jet_pattern_str;
  std::getline(ifstream, jet_pattern_str);

  std::vector<int> jet_pattern(jet_pattern_str.size());
  for (int i = 0; i < int(jet_pattern.size()); ++i)
  {
    jet_pattern[i] = (jet_pattern_str[i] == '>') ? 1 : -1;
  }

  part1(jet_pattern);
  part2(jet_pattern);
}
