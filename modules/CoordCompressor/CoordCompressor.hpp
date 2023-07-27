#include "../Vec2/Vec2.hpp"

#include <algorithm>
#include <vector>

class CoordCompressor {
  public:
    void add(int first, int second) {
        Vec2 coord = {first, second};
        coords.push_back(coord);
    }
    void add(const Vec2& p) {
        coords.push_back(p);
    }
    void sort() {
        std::sort(coords.begin(), coords.end());
        coords.erase(std::unique(coords.begin(), coords.end()), coords.end());
    }
    Vec2 operator[](int i) const {
        return coords[i];
    }
    int operator()(int first, int second) const {
        Vec2 coord = {first, second};
        return std::lower_bound(coords.begin(), coords.end(), coord) - coords.begin();
    }
    int operator()(const Vec2& p) const {
        return std::lower_bound(coords.begin(), coords.end(), p) - coords.begin();
    }
    int size() const {
        return coords.size();
    }
    void clear() {
        coords.clear();
    }

  private:
    std::vector<Vec2> coords;
};