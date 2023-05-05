#include "MazeGenerator.hpp"
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <regex>

void MazeGenerator::initialize(const Chromosome& chromosome, Vec2 size, Vec2 start, Vec2 goal) {
    map.clear();
    this->size = size;
    this->start = start;
    this->goal = goal;

    std::string bitmap = chromosome.get_bitmap();
    map.push_back(std::string(this->size.row + 2, '#'));
    for (int i = 1; i <= size.column; i++) {
        map.push_back("#");
        int start_index = (i - 1) * size.row;
        map[i] += bitmap.substr(start_index, size.row);
        map[i] += '#';
        map[i] = std::regex_replace(map[i], std::regex("0"), ".");
        map[i] = std::regex_replace(map[i], std::regex("1"), "#");
    }
    map.push_back(std::string(this->size.row + 2, '#'));
    map[start.column][start.row] = 'S';
    map[goal.column][goal.row] = 'G';
}

std::vector<std::string> MazeGenerator::get_map() {
    return map;
}

void MazeGenerator::show_map() {
    for (int i = 0; i < static_cast<int>(map.size()); i++) {
        for (int j = 0; j < static_cast<int>(map[i].size()); j++) {
            std::cout << std::setw(3) << map[i][j];
        }
        std::cout << std::endl;
    }
}

void MazeGenerator::output_map(std::string filepath) {
    std::ofstream output_file;
    output_file.open(filepath, std::ios::out);
    for (int i = 0; i < static_cast<int>(map.size()); i++) {
        for (int j = 0; j < static_cast<int>(map[i].size()); j++) {
            output_file << std::setw(3) << map[i][j];
        }
        output_file << std::endl;
    }
    output_file.close();
}