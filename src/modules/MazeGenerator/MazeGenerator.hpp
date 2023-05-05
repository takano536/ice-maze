#pragma once
#include "../Chromosome/Chromosome.hpp"
#include "../Vec2/Vec2.hpp"
#include <string>
#include <vector>

class MazeGenerator {
  public:
    void initialize(const Chromosome& chromosome, Vec2 size, Vec2 start, Vec2 goal);
    std::vector<std::string> get_map();
    void show_map();
    void output_map(std::string filepath);

  private:
    std::vector<std::string> map;
    Vec2 size;
    Vec2 start;
    Vec2 goal;
};