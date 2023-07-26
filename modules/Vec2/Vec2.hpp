#pragma once

struct Vec2 {
    int column;
    int row;

    bool operator==(const Vec2& rhs) const;
    bool operator!=(const Vec2& rhs) const;
    const Vec2 operator+(const Vec2& rhs) const;
    const Vec2 operator-(const Vec2& rhs) const;
    Vec2& operator+=(const Vec2& rhs);
    Vec2& operator-=(const Vec2& rhs);
};