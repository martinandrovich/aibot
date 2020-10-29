
#include "Position.hpp"

Position::Position() {}

Position::Position(int x, int y) 
	: x(x) , y(y) {}

Position::~Position() { }

Position Position::operator+(const Position& pos)
{
	Position res;
	res.x = this->x + pos.x;
	res.y = this->y + pos.y;
	return res;
}

Position Position::operator-(const Position& pos)
{
	Position res;
	res.x = this->x - pos.x;
	res.y = this->y - pos.y;
	return res;
}

bool Position::operator==(const Position& pos)
{
	return (this->x == pos.x && this->y == pos.y);
}

Position Position::operator+=(const Position &pos)
{
	Position res;
	res.x = this->x + pos.x;
	res.y = this->y + pos.y;
	return res;
}

std::ostream& operator<<(std::ostream& os, const Position& pos)
{
	return os << "{" << pos.x << "," << pos.y << "}";
}


