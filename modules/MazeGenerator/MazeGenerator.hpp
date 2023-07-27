#pragma once

#include "../Vec2/Vec2.hpp"

#include <array>
#include <string>
#include <vector>

class MazeGenerator {
  public:
    void initialize(const std::string& bit_string, Vec2 size, Vec2 start, Vec2 goal);
    std::vector<std::string> get();
    void print();
    void output(const std::string& filepath);

  private:
    std::string bin2hex(const std::string& bin);
    std::string hex2bin(const std::string& hex);

  private:
    const std::array<Vec2, 4> DIRECTION = {Vec2{1, 0}, Vec2{0, 1}, Vec2{-1, 0}, Vec2{0, -1}};
    std::vector<std::string> map;
    Vec2 size;
    Vec2 size_without_wall;
    Vec2 start;
    Vec2 goal;
    std::string map_id;
};