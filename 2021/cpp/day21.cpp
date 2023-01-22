#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void day1(const std::vector<std::string>& input_lines)
{
  std::array<int, 2> positions = {std::stoi(input_lines[0].substr(28)),
                                  std::stoi(input_lines[1].substr(28))};
  std::array<int, 2> scores = {0, 0};
  int turn = 0;
  int num_rolls = 0;
  int dice_value = 1;

  while (true)
  {
    // Do the dice rolls.
    int sum_rolls = 3 * dice_value + 3;
    num_rolls += 3;
    dice_value = ((dice_value + 3 - 1) % 1000) + 1;

    // Update position and score.
    positions[turn] = ((positions[turn] + sum_rolls - 1) % 10) + 1;
    scores[turn] += positions[turn];

    // Check if player won.
    if (scores[turn] >= 1000)
    {
      std::cout << scores[(turn + 1) % 2] * num_rolls << "\n";
      return;
    }

    turn = (turn + 1) % 2;
  }
}

std::pair<long, long> day2Solver(int pos1, int pos2, int score1, int score2,
                                 bool player1_turn,
                                 const std::vector<int>& roll_choices_from_3)
{
  // Returns number of scenarios where player 1/2 wins given input starting
  // condition.
  if (score1 >= 21)
  {
    return {1, 0};
  }
  if (score2 >= 21)
  {
    return {0, 1};
  }
  long total_wins1 = 0;
  long total_wins2 = 0;
  for (int i = 0; i < int(roll_choices_from_3.size()); ++i)
  {
    int roll_value = i + 3;
    int choice_multiplier = roll_choices_from_3[i];
    if (player1_turn)
    {
      int new_pos1 = ((pos1 + roll_value - 1) % 10) + 1;
      int new_score1 = score1 + new_pos1;
      auto [wins1, wins2] = day2Solver(new_pos1, pos2, new_score1, score2,
                                       !player1_turn, roll_choices_from_3);
      total_wins1 += choice_multiplier * wins1;
      total_wins2 += choice_multiplier * wins2;
    }
    else
    {
      int new_pos2 = ((pos2 + roll_value - 1) % 10) + 1;
      int new_score2 = score2 + new_pos2;
      auto [wins1, wins2] = day2Solver(pos1, new_pos2, score1, new_score2,
                                       !player1_turn, roll_choices_from_3);
      total_wins1 += choice_multiplier * wins1;
      total_wins2 += choice_multiplier * wins2;
    }
  }
  return {total_wins1, total_wins2};
}

void day2(const std::vector<std::string>& input_lines)
{
  std::array<int, 2> positions = {std::stoi(input_lines[0].substr(28)),
                                  std::stoi(input_lines[1].substr(28))};

  // We always do 3 rolls at a time.
  // Precompute possible values, from 3 to 9.
  std::vector<int> roll_choices_from_3(7);
  for (int a = 1; a <= 3; ++a)
  {
    for (int b = 1; b <= 3; ++b)
    {
      for (int c = 1; c <= 3; ++c)
      {
        ++roll_choices_from_3[a + b + c - 3];
      }
    }
  }
  auto [wins1, wins2] =
      day2Solver(positions[0], positions[1], 0, 0, true, roll_choices_from_3);
  std::cout << wins1 << "\n";
  std::cout << wins2 << "\n";
  std::cout << std::max(wins1, wins2) << "\n";
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
