#pragma once

#include "../Vec2/Vec2.hpp"

#include <algorithm>
#include <array>
#include <map>
#include <set>
#include <string>
#include <vector>

class MazeSolver {
  public:
    void initialize(const std::vector<std::string>& map, Vec2 size, Vec2 start, Vec2 goal);
    void solve();
    void print();
    void output(const std::string& filepath);
    bool satisfied();
    int calcuate_rating();

  private:
    void restore_procedure();

  private:
    const std::array<Vec2, 4> DIRECTION = {Vec2{1, 0}, Vec2{0, 1}, Vec2{-1, 0}, Vec2{0, -1}};
    const int INF = -1;

    std::vector<std::string> map;
    Vec2 size;
    Vec2 start;
    Vec2 goal;

    std::vector<std::vector<int>> steps;
    std::vector<std::vector<bool>> visited;
    std::vector<std::vector<bool>> passed;
    std::vector<std::vector<int>> answer;
    std::string procedure;

    int stone_cnt;
    int state_cnt;
    std::vector<std::vector<int>> min_dists_from_before_state;
    std::vector<int> dists_to_goal;
    unsigned long long int rating;
};
