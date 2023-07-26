#include "Vec2.hpp"

bool Vec2::operator==(const Vec2& rhs) const {
    return column == rhs.column && row == rhs.row;
}

bool Vec2::operator!=(const Vec2& rhs) const {
    return !(*this == rhs);
}

const Vec2 Vec2::operator+(const Vec2& rhs) const {
    return Vec2{column + rhs.column, row + rhs.row};
}

const Vec2 Vec2::operator-(const Vec2& rhs) const {
    return Vec2{column - rhs.column, row - rhs.row};
}

Vec2& Vec2::operator+=(const Vec2& rhs) {
    column += rhs.column;
    row += rhs.row;
    return *this;
}

Vec2& Vec2::operator-=(const Vec2& rhs) {
    column -= rhs.column;
    row -= rhs.row;
    return *this;
}
