#pragma once
#include <ostream>
class Position
{
public:
	Position();
	Position(int x, int y);
	~Position();

	Position operator+(const Position& pos);
	Position operator+=(const Position& pos);
	Position operator-(const Position& pos);
	bool operator==(const Position& pos);
	friend std::ostream& operator<<(std::ostream& os, const Position& pos); 

	int x = 0;
	int y = 0;
};

