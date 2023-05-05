#include "Chromosome.hpp"
#include <iostream>
#include <random>

namespace {

const int STONE_POP_PROBABILITY = 100;

}

void Chromosome::initialize(int bitmap_length) {
    std::random_device rnd;
    std::mt19937 mt(rnd());
    std::uniform_int_distribution<int> dist(0, 1000 - 1);
    for (int i = 0; i < bitmap_length; i++) {
        bitmap += (dist(mt) < STONE_POP_PROBABILITY ? '1' : '0');
    }
    rating = 0;
}

std::pair<Chromosome, Chromosome> Chromosome::execute_two_point_crossing(const Chromosome& another) {
    // 乱数生成機を生成
    std::random_device rnd;
    std::mt19937 mt(rnd());
    std::uniform_int_distribution<int> dist(0, static_cast<int>(this->bitmap.size()) - 1);

    // 入れ替える２点のインデックスを生成
    std::pair<int, int> switch_index = std::make_pair(dist(mt), dist(mt));
    if (switch_index.first > switch_index.second) {
        std::swap(switch_index.first, switch_index.second);
    }
    int replacing_length = switch_index.second - switch_index.first;

    // ビット列を２つ生成
    std::pair<std::string, std::string> bitmaps = std::make_pair(this->bitmap, another.bitmap);
    bitmaps.first.replace(switch_index.first, replacing_length, another.bitmap.substr(switch_index.first, replacing_length));
    bitmaps.second.replace(switch_index.first, replacing_length, this->bitmap.substr(switch_index.first, replacing_length));

    // 染色体を２つ生成
    std::pair<Chromosome, Chromosome> res;
    res.first.initialize(bitmaps.first);
    res.second.initialize(bitmaps.second);
    return res;
}

Chromosome Chromosome::mutate() {
    // 乱数生成機を生成
    std::random_device rnd;
    std::mt19937 mt(rnd());
    std::uniform_int_distribution<int> dist(0, static_cast<int>(this->bitmap.size()) - 1);

    int switch_count = dist(mt);
    for (int i = 0; i < switch_count; i++) {
        bitmap[dist(mt)] = (bitmap[dist(mt)] == '0' ? '1' : '0');
    }
    Chromosome res;
    res.initialize(bitmap);
    return res;
}

void Chromosome::update_rating(int rating) {
    this->rating = rating;
}

bool Chromosome::operator<(const Chromosome& another) const {
    return rating < another.rating;
};

std::string Chromosome::get_bitmap() const {
    return bitmap;
}

void Chromosome::initialize(const std::string& bitmap) {
    this->bitmap = bitmap;
    rating = 0;
}

int Chromosome::get_rating() const {
    return rating;
}