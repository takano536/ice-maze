#include "./modules/GeneticAlgorithm/GeneticAlgorithm.hpp"

int main() {
    const int MAX_GENERATION_COUNT = 10000;
    const std::string RESULT_DIRPATH = "../res/";

    GeneticAlgorithm genetic_algorithm;

    genetic_algorithm.initialize();
    while (genetic_algorithm.get_generation() <= MAX_GENERATION_COUNT) {
        genetic_algorithm.update_rating();
        genetic_algorithm.change_generation();
    }
    genetic_algorithm.output_best_map(RESULT_DIRPATH);
}
