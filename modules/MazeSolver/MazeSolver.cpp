#include "MazeSolver.hpp"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <queue>

void MazeSolver::initialize(const std::vector<std::string>& map, Vec2 size, Vec2 start, Vec2 goal) {
    this->map = map;
    this->size = size;
    this->start = start;
    this->goal = goal;
    steps.clear();
    steps.resize(size.first, std::vector<int>(size.second, INF));

    visited.clear();
    visited.resize(size.first, std::vector<bool>(size.second, false));

    passed.clear();
    passed.resize(size.first, std::vector<bool>(size.second, false));

    answer.clear();
    answer.resize(size.first, std::vector<int>(size.second, INF));

    procedure.clear();

    state_cnt = 0;

    min_dists_from_before_state.clear();
    min_dists_from_before_state.resize(size.first, std::vector<int>(size.second, INF));

    dists_to_goal.clear();

    rating = INF;
}

void MazeSolver::solve() {
    std::queue<Vec2> que;
    que.push(start);
    steps[start.first][start.second] = 0;
    visited[start.first][start.second] = true;

    while (!que.empty()) {
        Vec2 curr_coord = que.front();
        que.pop();

        for (const auto& dir : DIRECTION) {
            Vec2 next_coord = curr_coord;
            int dist = 0;
            while (map[next_coord.first + dir.first][next_coord.second + dir.second] != '#') {
                passed[next_coord.first][next_coord.second] = true;
                next_coord += dir;
                dist++;
            }

            int prev_min_dist = min_dists_from_before_state[next_coord.first][next_coord.second];
            min_dists_from_before_state[next_coord.first][next_coord.second] = std::min(dist, prev_min_dist);

            if (visited[next_coord.first][next_coord.second]) {
                continue;
            }

            state_cnt++;
            visited[next_coord.first][next_coord.second] = true;
            steps[next_coord.first][next_coord.second] = steps[curr_coord.first][curr_coord.second] + 1;
            que.push(next_coord);
        }
    }

    if (!satisfied()) {
        return;
    }

    restore_procedure();
}

int MazeSolver::calcuate_rating() {
    if (rating != INF) {
        return rating;
    }

    rating = 0;
    if (!satisfied()) {
        return rating;
    }

    int stone_cnt = -(size.first * 2 + size.second * 2 - 4);
    for (const auto& s : map) {
        stone_cnt += std::count(s.begin(), s.end(), '#');
    }
    rating -= stone_cnt * 50;

    rating += procedure.size() * 100;
    rating += std::ceil(std::sqrt(state_cnt) * 100);

    return std::max(rating, 1ULL);
}

void MazeSolver::restore_procedure() {
    int curr_step = steps[goal.first][goal.second];
    auto curr_coord = goal;
    auto next_coord = curr_coord;

    while (map[curr_coord.first][curr_coord.second] != 'S') {
        answer[curr_coord.first][curr_coord.second] = curr_step;
        const int next_step = steps[curr_coord.first][curr_coord.second] - 1;

        for (const auto& dir : DIRECTION) {
            Vec2 next_coord = curr_coord;
            int dist = 0;
            while (steps[next_coord.first][next_coord.second] != next_step && map[next_coord.first - dir.first][next_coord.second - dir.second] != '#') {
                next_coord -= dir;
                dist++;
            }

            if (steps[next_coord.first][next_coord.second] != next_step) {
                continue;
            }

            curr_coord = next_coord;
            curr_step = next_step;
            if (dir == Vec2{1, 0}) {
                procedure += "D";
            } else if (dir == Vec2{0, 1}) {
                procedure += "R";
            } else if (dir == Vec2{-1, 0}) {
                procedure += "U";
            } else if (dir == Vec2{0, -1}) {
                procedure += "L";
            }
            dists_to_goal.push_back(dist);
            break;
        }
    }
    std::reverse(procedure.begin(), procedure.end());
    std::reverse(dists_to_goal.begin(), dists_to_goal.end());
}

void MazeSolver::print() {
    for (int i = 0; i < size.first; i++) {
        for (int j = 0; j < size.second; j++) {
            switch (map[i][j]) {
                case '#':
                    std::cout << std::setw(3) << "#";
                    break;
                case 'S':
                    std::cout << std::setw(3) << "S";
                    break;
                case 'G':
                    std::cout << std::setw(3) << (steps[i][j] == INF ? "." : std::to_string(steps[i][j]));
                    break;
                case '.':
                    std::cout << std::setw(3) << (steps[i][j] == INF ? "." : std::to_string(steps[i][j]));
                    break;
            }
        }
        std::cout << std::endl;
    }
    std::cout << "Procedure       : " << (procedure.size() > 0 ? procedure : "None") << std::endl;
    std::cout << "Procedure count : " << procedure.size() << std::endl;
    std::cout << "State count     : " << state_cnt << std::endl;
    std::cout << "rating          : " << rating << std::endl;
}

void MazeSolver::output(const std::string& filepath) {
    std::ofstream output_file;
    output_file.open(filepath, std::ios::out);
    for (int i = 0; i < size.first; i++) {
        for (int j = 0; j < size.second; j++) {
            switch (map[i][j]) {
                case '#':
                    output_file << std::setw(3) << "#";
                    break;
                case 'S':
                    output_file << std::setw(3) << "S";
                    break;
                case 'G':
                    output_file << std::setw(3) << "G";
                    break;
                case '.':
                    output_file << std::setw(3) << (answer[i][j] == -1 ? "." : std::to_string(answer[i][j]));
                    break;
            }
        }
        output_file << std::endl;
    }
    output_file << "Procedure       : " << (procedure.size() > 0 ? procedure : "None") << std::endl;
    output_file << "Procedure count : " << procedure.size() << std::endl;
    output_file << "State count     : " << state_cnt << std::endl;
    output_file << "rating          : " << rating << std::endl;
    output_file.close();
}

bool MazeSolver::satisfied() {
    return steps[goal.first][goal.second] != INF;
}
