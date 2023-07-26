#pragma once
#include "../Vec2/Vec2.hpp"

#include <string>
#include <vector>

class MazeGenerator {
  public:
    void initialize(const std::string& bit_string, Vec2 size, Vec2 start, Vec2 goal);
    std::vector<std::string> get_map();
    void show_map();
    void output_map(const std::string& filepath);

  private:
    std::string bin2hex(const std::string& bin);
    std::string hex2bin(const std::string& hex);

  private:
    std::vector<std::string> map;
    Vec2 size;
    Vec2 start;
    Vec2 goal;
    std::string map_id;
};