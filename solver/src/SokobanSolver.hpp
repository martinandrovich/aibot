#pragma once
#include <fstream>
#include <string>
#include <vector>
#include<unordered_set>
#include "State.hpp"



class SokobanSolver
{
public:
	SokobanSolver();
	SokobanSolver(std::string);
	SokobanSolver(std::fstream file);
	~SokobanSolver();
	

	Position                 getRobotStart();
	std::vector<std::string> getMap();
	std::vector<Position>    getCansStart();
	std::vector<Position>    getGoalPositions();
	std::string              getStartHash();
	std::vector<std::string> getCleanMap();
	void                     cleanMap(std::vector<std::string>& map);
	bool                     stateExsists(State* state);

	std::string              solve();


protected:
	std::vector<std::string> m_orig_map; /*!< Member description */
	std::vector<std::string> m_clean_map;
	std::unordered_set<std::string> visited_states;
};
