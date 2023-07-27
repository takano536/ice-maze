#include "MazeGenerator.hpp"

#include <array>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <regex>

void MazeGenerator::initialize(const std::string& bit_string, Vec2 size, Vec2 start, Vec2 goal) {
    std::random_device seed_gen;
    std::mt19937 rand_engine(seed_gen());
    auto rand = [&rand_engine](int max) -> int { return rand_engine() % max; };

    map.clear();
    this->size = size;
    this->size_without_wall = size - Vec2{2, 2};
    this->start = start;
    this->goal = goal;

    map.push_back(std::string(this->size.second, '#'));
    for (int i = 1; i <= size_without_wall.first; i++) {
        map.push_back("#");
        int start_idx = (i - 1) * size_without_wall.second;
        map[i] += bit_string.substr(start_idx, size_without_wall.second);
        map[i] += '#';
        map[i] = std::regex_replace(map[i], std::regex("0"), ".");
        map[i] = std::regex_replace(map[i], std::regex("1"), "#");
    }
    map.push_back(std::string(this->size.second, '#'));

    std::vector<Vec2> in_directions;
    for (std::size_t i = 0; i < DIRECTION.size(); i++) {
        auto dir = DIRECTION[i];
        if (map[goal.first + dir.first][goal.second + dir.second] == '.') {
            in_directions.push_back(dir);
        }
    }
    std::shuffle(in_directions.begin(), in_directions.end(), rand_engine);
    for (std::size_t i = 1; i < in_directions.size(); i++) {
        map[goal.first + in_directions[i].first][goal.second + in_directions[i].second] = '#';
    }

    map[start.first][start.second] = 'S';
    map[goal.first][goal.second] = 'G';
    map_id = bin2hex(bit_string);
}

std::vector<std::string> MazeGenerator::get() {
    return map;
}

void MazeGenerator::print() {
    std::cout << size.first << ' ' << size.second << std::endl;
    for (const auto& s : map) {
        for (const auto& c : s) {
            std::cout << std::setw(3) << c;
        }
        std::cout << std::endl;
    }
}

void MazeGenerator::output(const std::string& filepath) {
    std::ofstream output_file;
    output_file.open(filepath, std::ios::out);

    output_file << size.first << ' ' << size.second << std::endl;
    for (const auto& s : map) {
        for (const auto& c : s) {
            output_file << std::setw(3) << c;
        }
        output_file << std::endl;
    }
    output_file << "ID : " << map_id << std::endl;
    output_file.close();
}

std::string MazeGenerator::bin2hex(const std::string& bin) {
    std::array<char, 16> hexchar_lookup_table{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
    int len = bin.size();
    if (len % 4 != 0) {
        return "";
    }
    std::string res = std::string(len / 4, '0');
    int idx = 0;
    for (int i = 0; i < len; i += 4) {
        int val = 0;
        for (int j = 0; j < 4; j++) {
            if (bin[i + j] == '1') {
                val += (1 << (3 - j));
            }
        }
        res[idx++] = hexchar_lookup_table[val];
    }
    return res;
}

std::string MazeGenerator::hex2bin(const std::string& hex) {
    int len = hex.size();
    std::string res = std::string(len * 4, '0');
    for (int i = 0; i < len; i++) {
        unsigned int idx = i * 4;
        int val = (hex[i] >= 'A') ? (hex[i] >= 'a') ? (hex[i] - 'a' + 10) : (hex[i] - 'A' + 10) : (hex[i] - '0');
        for (size_t j = 0; j < 4; j++) {
            res[idx + 3 - j] = ((val & (1 << j)) != 0) ? '1' : '0';
        }
    }
    return res;
}