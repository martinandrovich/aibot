#include "Position.hpp"

Position::Position() {}

Position::Position(int x, int y) 
	: x(x) , y(y) {}

Position::~Position() {}

Position operator+ (const Position& lhs, const Position& rhs)
{
	// Position res;
	// res.x = rhs.x + lhs.x;
	// res.y = rhs.y + lhs.y;
	// return res;
	return { lhs.x + rhs.x, lhs.y + rhs.y };
}

Position operator- (const Position& lhs, const Position& rhs)
{
	// Position res;
	// res.x = rhs.x - lhs.x;
	// res.y = rhs.y - lhs.y;
	// return res;
	return { lhs.x - rhs.x, lhs.y - rhs.y };
}

bool operator== (const Position& lhs, const Position& rhs)
{
	return (lhs.x == rhs.x && lhs.y == rhs.y);
}

Position& Position::operator+= (const Position &pos)
{
	this->x += pos.x;
	this->y += pos.y;
	return *this;
}

std::ostream& operator<<(std::ostream& os, const Position& pos)
{
	return os << "{" << pos.x << "," << pos.y << "}";
}


