#include "./modules/MazeGenerator/MazeGenerator.hpp"
#include "./modules/MazeSolver/MazeSolver.hpp"

#include "./nlohmann/json.hpp"

#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <random>
#include <string>

const std::string CONFIG_FILEPATH = "config/params.json";

int main() {
    std::random_device seed_gen;
    std::mt19937 rand_engine(seed_gen());
    auto rand = [&rand_engine](int max) -> int { return rand_engine() % max; };

    std::ifstream ifs(CONFIG_FILEPATH);
    nlohmann::json config;
    ifs >> config;

    const auto BATCH_COUNT = config["batch_count"].get<int>();
    const Vec2 SIZE = {config["size"]["height"].get<int>(), config["size"]["width"].get<int>()};
    const Vec2 SIZE_WITHOUT_WALL = SIZE - Vec2{2, 2};
    const int BIT_LENGTH = SIZE_WITHOUT_WALL.first * SIZE_WITHOUT_WALL.second;

    const Vec2 START = {config["start"]["y"].get<int>(), config["start"]["x"].get<int>()};
    const Vec2 GOAL = {config["goal"]["y"].get<int>(), config["goal"]["x"].get<int>()};

    const auto RESULT_DIRPATH = config["output_dirpath"].get<std::string>() + '/';
    const auto MAP_FILEPATH = RESULT_DIRPATH + config["map_filename"].get<std::string>();
    const auto ANSWER_FILEPATH = RESULT_DIRPATH + config["answer_filename"].get<std::string>();

    // メインループ
    int curr_batch_cnt = 0;
    int best_rating = 0;
    while (curr_batch_cnt < BATCH_COUNT) {
        curr_batch_cnt++;

        // ランダムビット列の生成
        std::uint32_t stone_pop_count = rand(BIT_LENGTH);
        std::string bit_string;
        bit_string = std::string(stone_pop_count, '1') + std::string(BIT_LENGTH - stone_pop_count, '0');
        std::shuffle(bit_string.begin(), bit_string.end(), rand_engine);

        // 迷路を作る
        Vec2 start = START;
        Vec2 goal = GOAL;
        if (start < Vec2{1, 1} || SIZE_WITHOUT_WALL < start) {
            start = {rand(SIZE_WITHOUT_WALL.first) + 1, rand(SIZE_WITHOUT_WALL.second) + 1};
        }
        if (goal < Vec2{1, 1} || SIZE_WITHOUT_WALL < goal) {
            goal = {rand(SIZE_WITHOUT_WALL.first) + 1, rand(SIZE_WITHOUT_WALL.second) + 1};
        }
        if (start == goal) {
            continue;
        }
        MazeGenerator maze_generator;
        maze_generator.initialize(bit_string, SIZE, start, goal);

        // 迷路を解く
        MazeSolver maze_solver;
        maze_solver.initialize(maze_generator.get(), SIZE, start, goal);
        maze_solver.solve();

        // 結果を出力
        if (maze_solver.calcuate_rating() <= best_rating) {
            continue;
        }

        maze_generator.output(MAP_FILEPATH);
        maze_solver.output(ANSWER_FILEPATH);
        best_rating = maze_solver.calcuate_rating();
        std::cout << "Batch Count : " << curr_batch_cnt << std::endl;
        std::cout << "Rating      : " << best_rating << std::endl;
        std::cout << std::endl;
    }
}
