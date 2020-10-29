
#include <iostream>
#include "SokobanSolver.hpp"
#include "Position.hpp"


int main(int argc, char *argv[])
{
	SokobanSolver sbs("maps/test.txt");	
	std::cout << "I have started solving the sokoban puzzle..." << std::endl;
	std::cout << sbs.solve() << std::endl;
	return 0;
}

