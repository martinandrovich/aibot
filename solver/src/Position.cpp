#include "Position.hpp"

Position::Position() {}

Position::Position(int x, int y) 
	: x(x) , y(y) {}

Position::~Position() {}

Position operator+ (const Position& rhs, const Position& lhs)
{
	// Position res;
	// res.x = rhs.x + lhs.x;
	// res.y = rhs.y + lhs.y;
	// return res;
	return { rhs.x + lhs.x, rhs.y + lhs.y };
}

Position operator- (const Position& rhs, const Position& lhs)
{
	// Position res;
	// res.x = rhs.x - lhs.x;
	// res.y = rhs.y - lhs.y;
	// return res;
	return { rhs.x - lhs.x, rhs.y - lhs.y };
}

bool operator== (const Position& rhs, const Position& lhs)
{
	return (rhs.x == lhs.x && rhs.y == lhs.y);
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


