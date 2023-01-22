#include <Eigen/Dense>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<Eigen::Matrix3i> createRotationMatrics()
{
  std::vector<Eigen::Matrix3i> mats;
  // 6 choices for x column
  // 4 choices for y column per x column
  // z generated via cross product
  mats.reserve(24);
  std::vector<Eigen::Vector3i> all_axes = {
      Eigen::Vector3i::UnitX(), -Eigen::Vector3i::UnitX(),
      Eigen::Vector3i::UnitY(), -Eigen::Vector3i::UnitY(),
      Eigen::Vector3i::UnitZ(), -Eigen::Vector3i::UnitZ()};
  for (const auto& x_vec : all_axes)
  {
    for (const auto& y_vec : all_axes)
    {
      if (x_vec.dot(y_vec) != 0)
      {
        continue;
      }
      Eigen::Vector3i z_vec = x_vec.cross(y_vec);
      Eigen::Matrix3i m;
      m << x_vec, y_vec, z_vec;
      mats.push_back(m);
    }
  }
  return mats;
}

int countMatchingPoints(const std::vector<Eigen::Vector3i>& points1,
                        const Eigen::Matrix3i& rotation1,
                        const Eigen::Vector3i& translation1,
                        const std::vector<Eigen::Vector3i>& points2,
                        const Eigen::Matrix3i& rotation2,
                        const Eigen::Vector3i& translation2)
{
  int num_matches = 0;
  for (const auto& p1 : points1)
  {
    for (const auto& p2 : points2)
    {
      if (rotation1 * p1 + translation1 == rotation2 * p2 + translation2)
      {
        ++num_matches;
      }
    }
  }

  return num_matches;
}

bool findOverlap(const std::vector<Eigen::Vector3i>& points1,
                 const std::vector<Eigen::Vector3i>& points2,
                 const Eigen::Matrix3i& rotation1,
                 const Eigen::Vector3i& translation1,
                 const std::vector<Eigen::Matrix3i>& possible_rotations,
                 Eigen::Matrix3i& rotation2_out,
                 Eigen::Vector3i& translation2_out)
{
  // We have a guarantee that a sensor can see all points within 1000 units.
  // We should conclude no overlap if a point that should be visible in either
  // sensor is not present. We're not doing this yet, maybe we can get away
  // without this check if there's no ambiguous cases.
  for (const auto& p1 : points1)
  {
    for (const auto& p2 : points2)
    {
      for (const auto& rotation2 : possible_rotations)
      {
        Eigen::Vector3i translation2 =
            rotation1 * p1 + translation1 - rotation2 * p2;
        int num_matching = countMatchingPoints(
            points1, rotation1, translation1, points2, rotation2, translation2);
        if (num_matching >= 12)
        {
          rotation2_out = rotation2;
          translation2_out = translation2;
          return true;
        }
      }
    }
  }
  return false;
}

void day1And2(const std::vector<std::vector<Eigen::Vector3i>>& scanner_pts,
              std::vector<Eigen::Matrix3i>& rotation_mats)
{
  // Start with scanner 0 already figured out.
  std::vector<uint8_t> is_aligned(scanner_pts.size(), false);
  is_aligned[0] = true;

  // scanner0_T_scannerN
  std::vector<Eigen::Matrix3i> rotations(scanner_pts.size(),
                                         Eigen::Matrix3i::Identity());
  std::vector<Eigen::Vector3i> translations(scanner_pts.size(),
                                            Eigen::Vector3i(0, 0, 0));

  // Repeatedly try pairwise alignments between aligned scanners and unaligned
  // scanners, until they're all aligned.
  int num_aligned = 1;
  while (num_aligned < int(scanner_pts.size()))
  {
    for (int i0 = 0; i0 < int(scanner_pts.size()); ++i0)
    {
      if (!is_aligned[i0])
      {
        continue;
      }
      for (int i1 = 0; i1 < int(scanner_pts.size()); ++i1)
      {
        if (i0 == i1 || is_aligned[i1])
        {
          continue;
        }
        // i0 is aligned, i1 is unaligned.
        Eigen::Matrix3i new_rotation;
        Eigen::Vector3i new_translation;
        bool overlaps = findOverlap(
            scanner_pts[i0], scanner_pts[i1], rotations[i0], translations[i0],
            rotation_mats, new_rotation, new_translation);
        if (overlaps)
        {
          std::cout << i0 << " overlaps with " << i1 << "\n";
          rotations[i1] = new_rotation;
          translations[i1] = new_translation;
          is_aligned[i1] = true;
          ++num_aligned;
        }
      }
    }
  }
  std::vector<Eigen::Vector3i> all_beacons;
  all_beacons.reserve(scanner_pts.size() * scanner_pts[0].size());
  for (int i = 0; i < int(scanner_pts.size()); ++i)
  {
    for (const auto& orig_pt : scanner_pts[i])
    {
      Eigen::Vector3i transformed_pt = rotations[i] * orig_pt + translations[i];
      if (std::find(all_beacons.begin(), all_beacons.end(), transformed_pt) ==
          all_beacons.end())
      {
        all_beacons.push_back(transformed_pt);
      }
    }
  }
  std::cout << all_beacons.size() << "\n";
  int max_l1_distance = 0;
  for (const auto& t1 : translations)
  {
    for (const auto& t2 : translations)
    {
      max_l1_distance = std::max(max_l1_distance, (t1 - t2).lpNorm<1>());
    }
  }
  std::cout << max_l1_distance << "\n";
}

int main(int argc, char* argv[])
{
  std::ifstream ifstream(argv[1]);
  std::vector<std::vector<Eigen::Vector3i>> scanner_pts;
  std::string line;
  while (std::getline(ifstream, line))
  {
    if (line.find("scanner") != std::string::npos)
    {
      scanner_pts.resize(scanner_pts.size() + 1);
    }
    else if (line.empty())
    {
      continue;
    }
    else
    {
      scanner_pts.back().resize(scanner_pts.back().size() + 1);
      std::stringstream s(line);
      Eigen::Vector3i& xyz = scanner_pts.back().back();
      char comma;
      s >> xyz.x() >> comma >> xyz.y() >> comma >> xyz.z();
    }
  }

  auto rotation_mats = createRotationMatrics();
  day1And2(scanner_pts, rotation_mats);
}
