
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <chrono>
#include <cctype>
#include "SokobanSolver.hpp"
#include "Position.hpp"

int main(int argc, char *argv[])
{
	
	// check input arguments
	if (argc < 2)
	{
		std::cerr << "Usage: ./solver filename" << std::endl;
		exit(-1);
	}

	// get map filename from argument
	const auto map_filename = std::string(argv[1]);

	// create solver with desired map
	SokobanSolver sbs(map_filename);
	
	// start solving; measure execution time
	std::cout << "I have started solving the sokoban puzzle..." << std::endl;

	double time_elapsed = 0.;
	const auto time_start = std::chrono::steady_clock::now();
	auto sol = sbs.solve();
	time_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - time_start).count();
	
	// Convert to solution string to all lower case
	std::transform(sol.begin(), sol.end(), sol.begin(),
    [](unsigned char c){ return std::tolower(c); });

	std::string sol_lc = "lllluddllurrrrrdruudlluluulldrurddulldrdrrrdruudlllluurdldrrrdrulllldllurrrrrdruuruulldrlrurd";

	std::cout << "Execution took: " << time_elapsed << " ms" << std::endl;
	//std::cout << "Solution: " << ((sol == "") ? "Not found." : sol) << std::endl;
	//std::cout << "Solution is " << (sol_lc == sol) << std::endl;

	return 0;
}
