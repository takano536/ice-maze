#pragma once
#include <string>
#include <utility>

class Chromosome {
  public:
    void initialize(int bitmap_length);
    std::pair<Chromosome, Chromosome> execute_two_point_crossing(const Chromosome& another);
    Chromosome mutate();
    void update_rating(int rating);
    bool operator<(const Chromosome& another) const;
    std::string get_bitmap() const;
    int get_rating() const;

  private:
    void initialize(const std::string& bitmap);

  private:
    std::string bitmap;
    int rating;
};