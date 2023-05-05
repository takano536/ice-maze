#include "GeneticAlgorithm.hpp"
#include "../Vec2/Vec2.hpp"
#include <algorithm>
#include <iostream>
#include <random>

namespace {

const int MAX_CHROMOSOME_COUNT = 50;
const int CROSSING_PROBABILITY = 990;
const Vec2 SIZE = {14, 14};
const Vec2 START = {14, 14};
const Vec2 GOAL = {1, 1};

}    // namespace

void GeneticAlgorithm::initialize() {
    parents.clear();
    children.clear();
    parents.resize(MAX_CHROMOSOME_COUNT);
    children.resize(MAX_CHROMOSOME_COUNT);
    for (auto& parent : parents) {
        parent.initialize(SIZE.column * SIZE.row);
    }
    curr_generation = 0;
}

void GeneticAlgorithm::update_rating() {
    for (auto& parent : parents) {
        maze_generator.initialize(parent, SIZE, START, GOAL);
        maze_solver.initialize(maze_generator.get_map());
        maze_solver.solve();
        parent.update_rating(maze_solver.get_rating());
    }
}

void GeneticAlgorithm::change_generation() {
    std::sort(parents.begin(), parents.end());
    if (best_chromosome.get_rating() == 0 ||
        parents[MAX_CHROMOSOME_COUNT - 1].get_rating() > best_chromosome.get_rating()) {
        best_chromosome = parents[MAX_CHROMOSOME_COUNT - 1];

        // 現在の情報を表示
        std::cout << "Generation : " << curr_generation << std::endl;
        std::cout << "Rating     : " << parents[MAX_CHROMOSOME_COUNT - 1].get_rating() << std::endl;
        // std::cout << "Max Rating : " << best_chromosome.get_rating() << std::endl;
        std::cout << std::endl;
    }

    int total_rating = 0;
    for (int i = 0; i < MAX_CHROMOSOME_COUNT; i++)
        total_rating += parents[i].get_rating();
    std::vector<int> rating_cumulative_sum(MAX_CHROMOSOME_COUNT + 1);
    for (int i = 0; i < MAX_CHROMOSOME_COUNT; i++)
        rating_cumulative_sum[i + 1] = rating_cumulative_sum[i] + parents[i].get_rating();

    // 乱数生成機を生成
    std::random_device rnd;
    std::mt19937 mt(rnd());
    std::uniform_int_distribution<int> dist_total_rating(0, total_rating - 1);

    // children の生成
    children.clear();
    int children_count = 0;
    children.reserve(MAX_CHROMOSOME_COUNT + 1);
    std::uniform_int_distribution<int> dist(0, 1000 - 1);
    while (children_count < MAX_CHROMOSOME_COUNT) {
        if (dist(mt) < CROSSING_PROBABILITY) {
            std::pair<int, int> crossing_idx;
            do {
                auto iter1 = std::lower_bound(rating_cumulative_sum.begin(), rating_cumulative_sum.end(), dist_total_rating(mt));
                auto iter2 = std::lower_bound(rating_cumulative_sum.begin(), rating_cumulative_sum.end(), dist_total_rating(mt));
                int idx1 = std::max(0, static_cast<int>(iter1 - rating_cumulative_sum.begin()) - 1);
                int idx2 = std::max(0, static_cast<int>(iter2 - rating_cumulative_sum.begin()) - 1);
                crossing_idx = std::make_pair(idx1, idx2);
            } while (crossing_idx.first == crossing_idx.second);
            auto descendants = parents[crossing_idx.first].execute_two_point_crossing(parents[crossing_idx.second]);
            children.push_back(descendants.first);
            children.push_back(descendants.second);
            children_count += 2;
        } else {
            int mutate_idx = std::max(0, static_cast<int>(std::lower_bound(rating_cumulative_sum.begin(), rating_cumulative_sum.end(), dist_total_rating(mt)) - rating_cumulative_sum.begin()) - 1);
            children.push_back(parents[mutate_idx].mutate());
            children_count++;
        }
    }
    while (children_count > MAX_CHROMOSOME_COUNT) {
        children_count--, children.pop_back();
    }
    children.shrink_to_fit();
    std::copy(children.begin(), children.end(), parents.begin());
    curr_generation++;
}

int GeneticAlgorithm::get_generation() {
    return curr_generation;
}

int GeneticAlgorithm::get_rating() {
    return best_chromosome.get_rating();
}

void GeneticAlgorithm::output_best_map(std::string dirpath) {
    maze_generator.initialize(best_chromosome, SIZE, START, GOAL);
    maze_generator.output_map(dirpath + "maze.txt");
    maze_solver.initialize(maze_generator.get_map());
    maze_solver.solve();
    maze_solver.output_result(dirpath + "answer.txt");
}