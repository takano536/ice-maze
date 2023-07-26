#include "./modules/MazeGenerator/MazeGenerator.hpp"
#include "./modules/MazeSolver/MazeSolver.hpp"

#include <algorithm>
#include <array>
#include <iostream>
#include <random>

int main() {
    std::random_device rnd;
    std::mt19937 gen(rnd());

    // パラメータ
    const int MAX_GENERATION_COUNT = 1e4;
    const std::string RESULT_DIRPATH = "./res/";

    const Vec2 SIZE = {13, 13};

    const int BIT_LENGTH = SIZE.row * SIZE.column;

    // メインループ
    int generation_count = 0;
    int best_rating = 0;
    while (generation_count < MAX_GENERATION_COUNT) {
        generation_count++;

        // ランダムビット列の生成
        int stone_pop_count = std::abs(static_cast<int>(gen())) % BIT_LENGTH;
        std::string bit_string;
        bit_string = std::string(stone_pop_count, '1') + std::string(BIT_LENGTH - stone_pop_count, '0');
        std::shuffle(bit_string.begin(), bit_string.end(), gen);

        // 迷路を解く
        MazeGenerator maze_generator;
        Vec2 start = {1, 1};
        Vec2 goal = {std::abs(static_cast<int>(gen())) % SIZE.column + 1, std::abs(static_cast<int>(gen())) % SIZE.row + 1};
        if (start == goal) {
            continue;
        }
        maze_generator.initialize(bit_string, SIZE, start, goal);

        MazeSolver maze_solver;
        maze_solver.initialize(maze_generator.get_map());
        maze_solver.solve();

        // 結果を出力
        if (maze_solver.get_rating() <= best_rating) {
            continue;
        }
        maze_generator.output_map(RESULT_DIRPATH + "maze.txt", false);
        maze_generator.output_map(RESULT_DIRPATH + "map.txt", true);
        maze_solver.output_result(RESULT_DIRPATH + "result.txt");
        best_rating = maze_solver.get_rating();
        std::cout << "Generation : " << generation_count << std::endl;
        std::cout << "Rating     : " << best_rating << std::endl;
        std::cout << std::endl;
    }
}
