#include "MazeGenerator.hpp"
#include <array>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <regex>

void MazeGenerator::initialize(const std::string& bit_string, Vec2 size, Vec2 start, Vec2 goal) {
    map.clear();
    this->size = size;
    this->start = start;
    this->goal = goal;

    map.push_back(std::string(this->size.row + 2, '#'));
    for (int i = 1; i <= size.column; i++) {
        map.push_back("#");
        int start_index = (i - 1) * size.row;
        map[i] += bit_string.substr(start_index, size.row);
        map[i] += '#';
        map[i] = std::regex_replace(map[i], std::regex("0"), ".");
        map[i] = std::regex_replace(map[i], std::regex("1"), "#");
    }
    map.push_back(std::string(this->size.row + 2, '#'));
    map[start.column][start.row] = 'S';
    map[goal.column][goal.row] = 'G';
    map_id = bin2hex(bit_string);
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

void MazeGenerator::output_map(const std::string& filepath, bool is_format) {
    std::ofstream output_file;
    output_file.open(filepath, std::ios::out);
    for (int i = 0; i < static_cast<int>(map.size()); i++) {
        for (int j = 0; j < static_cast<int>(map[i].size()); j++) {
            output_file << std::setw(is_format ? 3 : 0) << map[i][j];
        }
        output_file << std::endl;
    }
    if (is_format) {
        output_file << "ID : " << map_id << std::endl;
    }
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