
#include <iostream>
#include "SokobanSolver.hpp"
#include "Position.hpp"


int main(int argc, char *argv[])
{
	SokobanSolver sbs("maps/test.txt");	
	//SokobanSolver sbs("maps/map1.txt");	
	std::vector<Position> cans = {Position(1,3)};
	std::vector<Position> maps = sbs.getGoalPositions();
	//State state(Position(2,2), cans, nullptr, maps);

	std::cout << "I have started solving the sokoban puzzle..." << std::endl;
	std::cout << "Solution? : " << sbs.solve() << std::endl;
	return 0;
}

