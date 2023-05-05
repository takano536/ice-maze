#pragma once
#include "../Chromosome/Chromosome.hpp"
#include "../MazeGenerator/MazeGenerator.hpp"
#include "../MazeSolver/MazeSolver.hpp"
#include <vector>
#include <string>

class GeneticAlgorithm {
  public:
    void initialize();
    void update_rating();
    void change_generation();
    int get_generation();
    int get_rating();
    void output_best_map(std::string filepath);

  private:
    std::vector<Chromosome> parents;
    std::vector<Chromosome> children;
    Chromosome best_chromosome;
    MazeGenerator maze_generator;
    MazeSolver maze_solver;
    int curr_generation;
};