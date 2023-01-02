#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void day1(const std::vector<int>& nums, int num_bits)
{
  // Traverse from MSB to LSB.
  int gamma_rate = 0;
  int epsilon_rate = 0;
  for (int position = 0; position < num_bits; ++position)
  {
    int mask = 1 << (num_bits - 1 - position);
    int num_ones = 0;
    for (const auto& num : nums)
    {
      if (num & mask)
      {
        ++num_ones;
      }
    }
    gamma_rate <<= 1;
    epsilon_rate <<= 1;
    if (num_ones > nums.size() / 2)
    {
      gamma_rate += 1;
    }
    else
    {
      epsilon_rate += 1;
    }
  }

  std::cout << gamma_rate * epsilon_rate << "\n";
}

void day2(const std::vector<int>& nums, int num_bits)
{
  // Track oxygen and co2 numbers independently.
  std::vector<uint8_t> oxygen_candidates(nums.size(), true);
  std::vector<uint8_t> co2_candidates(nums.size(), true);
  bool oxygen_done = false;
  bool co2_done = false;
  for (int position = 0; position < num_bits; ++position)
  {
    int mask = 1 << (num_bits - 1 - position);
    int oxygen_num_ones = 0;
    int oxygen_num_zeros = 0;
    int co2_num_ones = 0;
    int co2_num_zeros = 0;
    for (int i = 0; i < int(nums.size()); ++i)
    {
      if (oxygen_candidates[i])
      {
        if (nums[i] & mask)
        {
          ++oxygen_num_ones;
        }
        else
        {
          ++oxygen_num_zeros;
        }
      }
      if (co2_candidates[i])
      {
        if (nums[i] & mask)
        {
          ++co2_num_ones;
        }
        else
        {
          ++co2_num_zeros;
        }
      }
    }

    // Stop updates when only one candidate number left.
    oxygen_done = (oxygen_num_ones + oxygen_num_zeros) == 1;
    co2_done = (co2_num_ones + co2_num_zeros) == 1;

    bool oxygen_keep_ones = oxygen_num_ones >= oxygen_num_zeros;
    bool co2_keep_ones = co2_num_ones < co2_num_zeros;
    for (int i = 0; i < int(nums.size()); ++i)
    {
      if (!oxygen_done && oxygen_candidates[i])
      {
        if (!oxygen_keep_ones && (nums[i] & mask))
        {
          oxygen_candidates[i] = false;
        }
        if (oxygen_keep_ones && !(nums[i] & mask))
        {
          oxygen_candidates[i] = false;
        }
      }
      if (!co2_done && co2_candidates[i])
      {
        if (!co2_keep_ones && (nums[i] & mask))
        {
          co2_candidates[i] = false;
        }
        if (co2_keep_ones && !(nums[i] & mask))
        {
          co2_candidates[i] = false;
        }
      }
    }
  }

  // Find the one candidate left.
  int oxygen_num = 0;
  for (int i = 0; i < int(nums.size()); ++i)
  {
    if (oxygen_candidates[i])
    {
      oxygen_num = nums[i];
      break;
    }
  }
  int co2_num = 0;
  for (int i = 0; i < int(nums.size()); ++i)
  {
    if (co2_candidates[i])
    {
      co2_num = nums[i];
      break;
    }
  }
  std::cout << oxygen_num * co2_num << "\n";
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

  // Convert to decimal numbers.
  std::vector<int> nums(lines.size());
  for (int i = 0; i < int(lines.size()); ++i)
  {
    int x = 0;
    for (const auto& c : lines[i])
    {
      x <<= 1;
      x += (c == '1') ? 1 : 0;
    }
    nums[i] = x;
  }

  int num_bits = lines[0].size();

  day1(nums, num_bits);
  day2(nums, num_bits);
}
