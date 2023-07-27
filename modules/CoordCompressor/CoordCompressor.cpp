#include "CoordCompressor.hpp"

void CoordCompressor::add(int first, int second) {
    coords.emplace_back(first, second);
}
void CoordCompressor::add(const Vec2& p) {
    coords.push_back(p);
}
void CoordCompressor::sort() {
    std::sort(coords.begin(), coords.end());
    coords.erase(std::unique(coords.begin(), coords.end()), coords.end());
}
Vec2 CoordCompressor::operator[](int i) const {
    return coords[i];
}
int CoordCompressor::operator()(int first, int second) const {
    return std::lower_bound(coords.begin(), coords.end(), std::make_pair(first, second)) - coords.begin();
}
int CoordCompressor::operator()(const Vec2& p) const {
    return std::lower_bound(coords.begin(), coords.end(), p) - coords.begin();
}
int CoordCompressor::size() const {
    return coords.size();
}