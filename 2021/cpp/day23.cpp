#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

// Example:
// #############
// #...........#
// ###B#C#B#D###
//   #A#D#C#A#
//   #########

// 11 hallway spots, 0-10 left to right.
// 4 side rooms, top and bottom spots.

// A: 1 energy
// B: 10 energy
// C: 100 energy
// D: 1000 energy

// 1. No stopping on spots right outside side rooms.
// 2. No moving into a room unless its the destination.
// 3. No creation of mixed types in a room.
// 4. Cannot move from hallway spot to hallway spot.

// Thus, the possible moves are:
// 1. Move from room to hallway
// 2. Move from hallway to room

// And the possible spots are
// hallway_0, hallway_1, (also 3, 5, 7, 9, 10)
// side2_top, side2_bottom, side4_top, side4_bottom (also side6 and side 8)

// From every start spot we can explore moving to all other reachable spots.
// We'll also hash the world state so we avoid going in loops.

std::unordered_map<char, int> STEP_COSTS = {
    {'A', 1}, {'B', 10}, {'C', 100}, {'D', 1000}};

// A slot represent a spot that can store 1 or more anthropods(chars).
// Basically behaves like a LIFO stack.
class Slot
{
 public:
  Slot(const std::vector<char>& data, int max_size, bool is_hallway,
       int x_coord)
      : data_(data),
        max_size_(max_size),
        is_hallway_(is_hallway),
        x_coord_(x_coord)
  {
  }

  bool operator==(const Slot&) const = default;
  bool isFull() const { return data_.size() == max_size_; }
  bool isEmpty() const { return data_.empty(); }
  size_t size() const { return data_.size(); }

  void push(char c) { data_.push_back(c); }
  void pop() { data_.pop_back(); }
  char top() const { return data_.back(); }
  char getChar(int i = 0) const { return i < size() ? data_[i] : '.'; }

  int topElemY() const
  {
    // y coord of the element retried by top().
    if (is_hallway_)
    {
      return 0;
    }
    return max_size_ - size() + 1;
  }
  int nextEmptyY() const
  {
    // y coord where we'd put something via push.
    if (is_hallway_)
    {
      return 0;
    }
    return max_size_ - size();
  }

  const std::vector<char>& data() const { return data_; }
  int maxSize() const { return max_size_; }
  bool isHallway() const { return is_hallway_; }
  int xCoord() const { return x_coord_; }

 private:
  std::vector<char> data_;
  const int max_size_;
  const bool is_hallway_;
  const int x_coord_;
};

class WorldState
{
 public:
  WorldState(const std::vector<std::string>& input_lines, bool is_part2);

  bool operator==(const WorldState& other) const;

  void print() const;

  bool finished() const;

  bool emptySpaceBetween(int i, int j) const;

  int getMoveCost(int i, int j) const;

  bool canMove(int src, int dst) const;

  void move(int src, int dst)
  {
    slots_[dst].push(slots_[src].top());
    slots_[src].pop();
  }

  friend std::hash<WorldState>;

  const std::vector<Slot>& slots() const { return slots_; }

 private:
  // Based on constructor, the slots have a fixed order.
  std::vector<Slot> slots_;
};

WorldState::WorldState(const std::vector<std::string>& input_lines,
                       bool is_part2)
{
  // Assume all start positions are in the side rooms.
  const std::string& top_side = input_lines[2];
  const std::string& bottom_side = input_lines[3];

  // Left hallway spots
  slots_.emplace_back(std::vector<char>{}, 1, true, 0);
  slots_.emplace_back(std::vector<char>{}, 1, true, 1);
  // Middle hallway spots
  slots_.emplace_back(std::vector<char>{}, 1, true, 3);
  slots_.emplace_back(std::vector<char>{}, 1, true, 5);
  slots_.emplace_back(std::vector<char>{}, 1, true, 7);
  // Right hallway spots
  slots_.emplace_back(std::vector<char>{}, 1, true, 9);
  slots_.emplace_back(std::vector<char>{}, 1, true, 10);
  // Side rooms
  if (!is_part2)
  {
    slots_.emplace_back(std::vector<char>{bottom_side[3], top_side[3]}, 2,
                        false, 2);
    slots_.emplace_back(std::vector<char>{bottom_side[5], top_side[5]}, 2,
                        false, 4);
    slots_.emplace_back(std::vector<char>{bottom_side[7], top_side[7]}, 2,
                        false, 6);
    slots_.emplace_back(std::vector<char>{bottom_side[9], top_side[9]}, 2,
                        false, 8);
  }
  else
  {
    // Hardcoded!
    slots_.emplace_back(
        std::vector<char>{bottom_side[3], 'D', 'D', top_side[3]}, 4, false, 2);
    slots_.emplace_back(
        std::vector<char>{bottom_side[5], 'B', 'C', top_side[5]}, 4, false, 4);
    slots_.emplace_back(
        std::vector<char>{bottom_side[7], 'A', 'B', top_side[7]}, 4, false, 6);
    slots_.emplace_back(
        std::vector<char>{bottom_side[9], 'C', 'A', top_side[9]}, 4, false, 8);
  }
}

bool WorldState::operator==(const WorldState& other) const
{
  for (int i = 0; i < int(slots_.size()); ++i)
  {
    if (slots_[i] != other.slots_[i])
    {
      return false;
    }
  }
  return true;
}

void WorldState::print() const
{
  std::cout << "#############\n";
  // Print hallway.
  std::cout << "#" << slots_[0].getChar() << slots_[1].getChar() << "."
            << slots_[2].getChar() << "." << slots_[3].getChar() << "."
            << slots_[4].getChar() << "." << slots_[5].getChar()
            << slots_[6].getChar() << "#\n";
  for (int row = slots_[7].maxSize() - 1; row >= 0; --row)
  {
    std::cout << "###" << slots_[7].getChar(row) << "#"
              << slots_[8].getChar(row) << "#" << slots_[9].getChar(row) << "#"
              << slots_[10].getChar(row) << "###\n";
  }
  std::cout << "  #########  \n";
}

bool WorldState::finished() const
{
  for (int i = 7; i <= 10; ++i)
  {
    if (slots_[i].size() != slots_[i].maxSize())
    {
      return false;
    }
  }
  for (int row = 0; row < slots_[7].maxSize(); ++row)
  {
    if (slots_[7].data()[row] != 'A' || slots_[8].data()[row] != 'B' ||
        slots_[9].data()[row] != 'C' || slots_[10].data()[row] != 'D')
    {
      return false;
    }
  }
  return true;
}

bool WorldState::emptySpaceBetween(int i, int j) const
{
  int x1 = slots_[i].xCoord();
  int x2 = slots_[j].xCoord();
  if (x1 > x2)
  {
    std::swap(x1, x2);
  }
  for (const auto& slot : slots_)
  {
    if (slot.isHallway() && !slot.isEmpty() && slot.xCoord() > x1 &&
        slot.xCoord() < x2)
    {
      return false;
    }
  }
  return true;
}

int WorldState::getMoveCost(int i, int j) const
{
  int step_cost = STEP_COSTS[slots_[i].top()];
  // For the diffs, we assume we're moving inner to inner here.
  int x_diff = std::abs(slots_[i].xCoord() - slots_[j].xCoord());
  // Always moving between hallway and room.
  // y diff depends on how deep into a room we are.
  int y_diff = std::abs(slots_[i].topElemY() - slots_[j].nextEmptyY());

  int num_steps = x_diff + y_diff;

  return step_cost * num_steps;
}

bool WorldState::canMove(int src_ind, int dst_ind) const
{
  if (src_ind == dst_ind)
  {
    return false;
  }
  const auto& src = slots_[src_ind];
  const auto& dst = slots_[dst_ind];

  if (src.isHallway() == dst.isHallway())
  {
    // Must move between hallway and room.
    return false;
  }
  if (src.isEmpty() || dst.isFull())
  {
    // Must have something to move, and an empty spot at dst.
    return false;
  }
  if (!dst.isHallway())
  {
    // Can only move to the proper room, and only if no nonmatching types
    // are there.
    char type = src.top();
    // First check proper room.
    if ((type == 'A') && (dst.xCoord() != 2))
    {
      return false;
    }
    if ((type == 'B') && (dst.xCoord() != 4))
    {
      return false;
    }
    if ((type == 'C') && (dst.xCoord() != 6))
    {
      return false;
    }
    if ((type == 'D') && (dst.xCoord() != 8))
    {
      return false;
    }
    // Now check no nonmatching type.
    for (char c : dst.data())
    {
      if (c != type)
      {
        return false;
      }
    }
  }
  if (!emptySpaceBetween(src_ind, dst_ind))
  {
    // Must not be anything in between.
    return false;
  }
  return true;
}

template <>
struct std::hash<WorldState>
{
  // djb2 hash: http://www.cse.yorku.ca/~oz/hash.html
  std::size_t operator()(const WorldState& s) const
  {
    size_t hash = 5381;
    for (const auto& slot : s.slots_)
    {
      for (char c : slot.data())
      {
        hash = ((hash << 5) + hash) + c;
      }
    }
    return hash;
  };
};

int solver(const WorldState& state)
{
  std::unordered_set<WorldState> seen_states;

  auto cmp = [](const std::pair<int, WorldState>& left,
                const std::pair<int, WorldState>& right) {
    return left.first > right.first;
  };
  std::priority_queue<std::pair<int, WorldState>,
                      std::vector<std::pair<int, WorldState>>, decltype(cmp)>
      pq(cmp);
  pq.emplace(0, state);

  int best_solution = -1;
  while (!pq.empty())
  {
    auto [cost, state] = pq.top();
    pq.pop();

    if (seen_states.contains(state))
    {
      continue;
    }
    seen_states.emplace(state);

    if (state.finished())
    {
      if (best_solution == -1 || cost < best_solution)
      {
        best_solution = cost;
      }
      continue;
    }

    for (int src_ind = 0; src_ind < int(state.slots().size()); ++src_ind)
    {
      for (int dst_ind = 0; dst_ind < int(state.slots().size()); ++dst_ind)
      {
        if (!state.canMove(src_ind, dst_ind))
        {
          continue;
        }

        // We can make a move!
        int move_cost = state.getMoveCost(src_ind, dst_ind);
        WorldState state2(state);
        state2.move(src_ind, dst_ind);
        int state2_cost = cost + move_cost;
        pq.emplace(state2_cost, state2);
      }
    }
  }

  return best_solution;
}

void day1(const std::vector<std::string>& input_lines)
{
  WorldState state(input_lines, false);

  state.print();

  std::cout << solver(state) << "\n";
}

void day2(const std::vector<std::string>& input_lines)
{
  WorldState state(input_lines, true);

  state.print();

  std::cout << solver(state) << "\n";
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
