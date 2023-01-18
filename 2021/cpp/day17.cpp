#include <fstream>
#include <iostream>
#include <string>
#include <vector>

bool doesShotEnterRegion(int initial_velocity_x, int initial_velocity_y,
                         int min_x, int max_x, int min_y, int max_y,
                         int& highest_y_out)
{
  int velocity_x = initial_velocity_x;
  int velocity_y = initial_velocity_y;
  int position_x = 0;
  int position_y = 0;
  highest_y_out = 0;
  while (true)
  {
    highest_y_out = std::max(highest_y_out, position_y);
    if (position_x >= min_x && position_x <= max_x && position_y >= min_y &&
        position_y <= max_y)
    {
      return true;
    }
    if (position_x > max_x)
    {
      // We assume we are shooting to the right, and so if we're right of the
      // target, we're too far.
      return false;
    }
    if (position_y < min_y && velocity_y < 0)
    {
      // We are below the target and going downwards, we'll never reach it due
      // to gravity.
      return false;
    }
    position_x += velocity_x;
    position_y += velocity_y;
    if (velocity_x > 0)
    {
      --velocity_x;
    }
    else if (velocity_x < 0)
    {
      ++velocity_x;
    }
    --velocity_y;
  }
  return false;
}

void day1(int min_x, int max_x, int min_y, int max_y)
{
  int max_highest_y = 0;
  // Assuming the region is to the right.
  for (int velocity_x = 0; velocity_x <= 100; ++velocity_x)
  {
    // Since we want height, assume only upwards shots make sense.
    for (int velocity_y = 0; velocity_y <= 100; ++velocity_y)
    {
      int highest_y;
      bool success = doesShotEnterRegion(velocity_x, velocity_y, min_x, max_x,
                                         min_y, max_y, highest_y);
      if (success)
      {
        max_highest_y = std::max(highest_y, max_highest_y);
      }
    }
  }
  std::cout << max_highest_y << "\n";
}

void day2(int min_x, int max_x, int min_y, int max_y)
{
  int num_solutions = 0;
  // Assuming the region is to the right.
  for (int velocity_x = 0; velocity_x <= 1000; ++velocity_x)
  {
    for (int velocity_y = -100; velocity_y <= 100; ++velocity_y)
    {
      int highest_y;
      bool success = doesShotEnterRegion(velocity_x, velocity_y, min_x, max_x,
                                         min_y, max_y, highest_y);
      if (success)
      {
        ++num_solutions;
      }
    }
  }
  std::cout << num_solutions << "\n";
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

  int x_equals_pos = line.find("=");
  int x_dot_pos = line.find("..");
  int comma_pos = line.find(",");
  int y_equals_pos = line.find("=", x_dot_pos);
  int y_dot_pos = line.find("..", y_equals_pos);
  int min_x =
      std::stoi(line.substr(x_equals_pos + 1, (x_dot_pos - x_equals_pos - 1)));
  int max_x =
      std::stoi(line.substr(x_dot_pos + 2, (comma_pos - x_dot_pos - 2)));
  int min_y =
      std::stoi(line.substr(y_equals_pos + 1, (y_dot_pos - y_equals_pos - 1)));
  int max_y = std::stoi(line.substr(y_dot_pos + 2));

  std::cout << "Target region is: " << min_x << ", " << max_x << ", " << min_y
            << ", " << max_y << "\n";

  day1(min_x, max_x, min_y, max_y);
  day2(min_x, max_x, min_y, max_y);
}
