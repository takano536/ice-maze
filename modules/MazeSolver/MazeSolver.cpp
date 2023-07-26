#include "MazeSolver.hpp"
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <queue>

namespace {

const int STONE_CONSTANT = 20;

}    // namespace

void MazeSolver::initialize(const std::vector<std::string>& map) {
    this->map = map;
    procedure.clear();
    height = static_cast<int>(map.size());
    width = static_cast<int>(map[0].size());
    step_counts.clear();
    step_counts.resize(height, std::vector<int>(width, -1));
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (this->map[i][j] == 'S') {
                start = Vec2{i, j};
            }
            if (this->map[i][j] == 'G') {
                goal = Vec2{i, j};
            }
        }
    }
    state_count = 0;
    max_step_counts = 0;
    move_distances.clear();
    rating = 0;
}

void MazeSolver::solve() {
    std::queue<Vec2> que;
    step_counts[start.column][start.row] = 0;
    que.push(start);
    bool satisfied = false;

    while (!que.empty()) {
        Vec2 prev_pos = que.front();
        que.pop();

        for (const auto& direction : SEARCH_DIRECTION) {
            Vec2 curr_pos = prev_pos + direction;
            if (curr_pos.column < 0 || curr_pos.row < 0) {    // 画面の外に出るならスキップ
                continue;
            }
            if (curr_pos.column >= height || curr_pos.row >= width) {    // 画面の外に出るならスキップ
                continue;
            }
            if (map[curr_pos.column][curr_pos.row] == '#') {    // 壁に埋まっているならスキップ
                continue;
            }

            bool can_continue = true;
            int move_distance = 0;
            do {    // 氷による滑り
                curr_pos += direction;
                move_distance++;
                if (curr_pos.column < 0 || curr_pos.row < 0) {    // 画面の外に出るならスキップ
                    can_continue = false;
                    break;
                }
                if (curr_pos.column >= height || curr_pos.row >= width) {    // 画面の外に出るならスキップ
                    can_continue = false;
                    break;
                }
            } while (map[curr_pos.column][curr_pos.row] != '#');
            curr_pos -= direction;

            if (!can_continue) {
                continue;
            }

            if (map[curr_pos.column][curr_pos.row] == 'G') {
                satisfied = true;
            }

            if (step_counts[curr_pos.column][curr_pos.row] != -1) {    // 到達座標ならスキップ
                continue;
            }

            // 未到達座標なら記録
            que.push(curr_pos);
            step_counts[curr_pos.column][curr_pos.row] = step_counts[prev_pos.column][prev_pos.row] + 1;
            max_step_counts = std::max(step_counts[curr_pos.column][curr_pos.row], max_step_counts);
            state_count++;
        }
    }
    if (!satisfied) {
        return;
    }

    restore_procedure();
    int stone_count = -(height * 2 + width * 2 - 4);
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            stone_count += map[i][j] == '#';

    int move_count = procedure.size();
    rating = std::max(2, move_count * state_count - stone_count * STONE_CONSTANT);
}

void MazeSolver::restore_procedure() {
    std::queue<Vec2> que;
    que.push(goal);
    int curr_step_count = step_counts[goal.column][goal.row];
    std::vector<std::vector<int>> answer_step_counts(height, std::vector<int>(width, -1));

    while (!que.empty() && map[que.front().column][que.front().row] != 'S') {
        curr_step_count--;
        Vec2 prev_pos = que.front();
        que.pop();

        for (const auto& direction : SEARCH_DIRECTION) {
            if ((prev_pos + direction).column < 0 || (prev_pos + direction).row < 0) {    // 画面の外に出るならスキップ
                continue;
            }
            if ((prev_pos + direction).column >= height || (prev_pos + direction).row >= width) {    // 画面の外に出るならスキップ
                continue;
            }
            if (map[(prev_pos + direction).column][(prev_pos + direction).row] == '#') {    // 壁に埋まっているならスキップ
                continue;
            }

            Vec2 curr_pos = prev_pos;
            int curr_move_distance = 0;
            bool can_continue = true;
            do {
                curr_pos += direction;
                curr_move_distance++;
                if (curr_pos.column < 0 || curr_pos.row < 0) {    // 画面の外に出るならスキップ
                    can_continue = false;
                    break;
                }
                if (curr_pos.column >= height || curr_pos.row >= width) {    // 画面の外に出るならスキップ
                    can_continue = false;
                    break;
                }
                if (map[curr_pos.column][curr_pos.row] == '#') {    // 壁に埋まっているならスキップ
                    can_continue = false;
                    break;
                }
            } while (step_counts[curr_pos.column][curr_pos.row] != curr_step_count);

            if (!can_continue) {
                continue;
            }

            move_distances.push_back(curr_move_distance);
            answer_step_counts[curr_pos.column][curr_pos.row] = curr_step_count;
            que.push(curr_pos);

            if (direction == Vec2{1, 0}) {
                procedure += 'U';
            } else if (direction == Vec2{0, 1}) {
                procedure += 'L';
            } else if (direction == Vec2{-1, 0}) {
                procedure += 'D';
            } else {
                procedure += 'R';
            }
            break;
        }
    }
    std::reverse(procedure.begin(), procedure.end());
    step_counts = answer_step_counts;
}

std::string MazeSolver::get_answer() {
    return procedure;
}

void MazeSolver::show_result() {
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (map[i][j] == '#') {
                std::cout << "  #";
            } else if (map[i][j] == 'S') {
                std::cout << "  S";
            } else if (map[i][j] == 'G') {
                std::cout << "  G";
            } else if (step_counts[i][j] == -1) {
                std::cout << "  .";
            } else {
                printf("%3d", step_counts[i][j]);
            }
        }
        std::cout << std::endl;
    }
    std::cout << "Procedure       : " << (procedure.size() > 0 ? procedure : "None") << std::endl;
    std::cout << "Procedure Count : " << procedure.size() << std::endl;
    std::cout << "State Count     : " << state_count << std::endl;
    std::cout << "rating          : " << rating << std::endl;
}

void MazeSolver::output_result(const std::string& filepath) {
    std::ofstream output_file;
    output_file.open(filepath, std::ios::out);
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (map[i][j] == '#') {
                output_file << "  #";
            } else if (map[i][j] == 'S') {
                output_file << "  S";
            } else if (map[i][j] == 'G') {
                output_file << "  G";
            } else if (step_counts[i][j] == -1) {
                output_file << "  .";
            } else {
                output_file << std::setw(3) << step_counts[i][j];
            }
        }
        output_file << std::endl;
    }
    output_file << "Procedure       : " << (procedure.size() > 0 ? procedure : "None") << std::endl;
    output_file << "Procedure Count : " << procedure.size() << std::endl;
    output_file << "State Count     : " << state_count << std::endl;
    output_file << "rating          : " << rating << std::endl;
    output_file.close();
}

bool MazeSolver::satisfied() {
    return procedure.size() > 0;
}

int MazeSolver::get_rating() {
    return rating;
}