#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void day1(const std::vector<int>& nums)
{
  int num_increases = 0;
  for (int i = 0; i < int(nums.size()) - 1; ++i)
  {
    if (nums[i] < nums[i + 1])
    {
      ++num_increases;
    }
  }
  std::cout << num_increases << "\n";
}

void day2(const std::vector<int>& nums)
{
  int num_increases = 0;
  for (int i = 0; i < int(nums.size()) - 3; ++i)
  {
    int sum1 = nums[i] + nums[i + 1] + nums[i + 2];
    int sum2 = nums[i + 1] + nums[i + 2] + nums[i + 3];
    if (sum1 < sum2)
    {
      ++num_increases;
    }
  }
  std::cout << num_increases << "\n";
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<int> nums;
  std::string line;
  while (std::getline(ifstream, line))
  {
    nums.push_back(std::stoi(line));
  }

  day1(nums);
  day2(nums);
}
