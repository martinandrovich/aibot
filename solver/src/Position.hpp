#pragma once
#include <ostream>
class Position
{
public:
	Position();
	Position(int x, int y);
	~Position();

	Position& operator+= (const Position& pos);

	friend std::ostream& operator<< (std::ostream& os, const Position& pos); 
	friend Position operator+ (const Position& rhs, const Position& lhs);
	friend Position operator- (const Position& rhs, const Position& lhs);
	friend bool operator== (const Position& rhs, const Position& lhs);

	int x = 0;
	int y = 0;
};

