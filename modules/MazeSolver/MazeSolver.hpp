#pragma once
#include "../Vec2/Vec2.hpp"
#include <algorithm>
#include <array>
#include <string>
#include <vector>

class MazeSolver {
  public:
    void initialize(const std::vector<std::string>& map);
    void solve();
    std::string get_answer();
    void show_result();
    void output_result(const std::string& filepath);
    bool satisfied();
    int get_rating();

  private:
    void restore_procedure();

  private:
    const std::array<Vec2, 4> SEARCH_DIRECTION = {Vec2{1, 0}, Vec2{0, 1}, Vec2{-1, 0}, Vec2{0, -1}};
    std::vector<std::string> map;
    std::vector<std::vector<int>> step_counts;
    int height;
    int width;
    Vec2 start;
    Vec2 goal;
    std::string procedure;
    int state_count;
    int max_step_counts;
    std::vector<int> move_distances;
    int rating;
};
