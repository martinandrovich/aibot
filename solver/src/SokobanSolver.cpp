#include <algorithm>
#include <cctype>
#include <iostream>
#include <cstddef>
#include <fstream>
#include <ostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

#include "debug.h"
#include "Position.hpp"
#include "SokobanSolver.hpp"

SokobanSolver::SokobanSolver() {}

SokobanSolver::SokobanSolver(std::string map)
{
	this->m_map_name = map;
	std::fstream fs(map);
	std::string line;
	while (std::getline(fs, line))
	{
		this->m_orig_map.push_back(line);
	}
	m_clean_map = m_orig_map;
	cleanMap(m_clean_map);
}

SokobanSolver::SokobanSolver(std::fstream file) 
{
	std::string line;
	while (std::getline(file, line))
		this->m_orig_map.push_back(line);
	m_clean_map = m_orig_map;
	cleanMap(m_clean_map);
}

SokobanSolver::~SokobanSolver() {}

void SokobanSolver::cleanMap(std::vector<std::string>& map)
{
	for (auto& row : map) 
	{
		for (char& ch : row) 
		{
			if (ch != 'X' and ch != '.') 
			{
				ch = '.';
			}
		}
	}
}

std::vector<Position> SokobanSolver::generateIllegalCanPositions()
{
	std::vector<Position> illegal_pos;

	// Position in upper corners 
	//
	// XXXXX  |  XXXXX
	// XO     |     OX
	// X      |      X
	//
	// Position in lower corners
	//
	// X      |      X
	// XO     |     OX
	// XXXXX  |  XXXXX
	//
	
	bool upper_corner_illegal = false;
	bool lower_corner_illegal = false;

	// Search for each location in a corner.
	for (int y = 0; y < this->m_clean_map.size(); ++y) {
		for (int x = 0; x < this->m_clean_map[y].length(); ++x) {
			if (this->m_clean_map[y][x] == '.' || this->m_orig_map[y][x] == 'G')
			{
				upper_corner_illegal = this->m_orig_map[y - 1][x] == 'X' && ( this->m_orig_map[y][x + 1] == 'X' || this->m_orig_map[y][x - 1] == 'X' );
				lower_corner_illegal = this->m_orig_map[y + 1][x] == 'X' && ( this->m_orig_map[y][x + 1] == 'X' || this->m_orig_map[y][x - 1] == 'X' );
				// Upper corners
				if (upper_corner_illegal && this->m_orig_map[y][x] != 'G')
					illegal_pos.push_back(Position(x,y));
				// Lower corners
				if (lower_corner_illegal && this->m_orig_map[y][x] != 'G')
					illegal_pos.push_back(Position(x,y));
			}
		}
	}
	return illegal_pos;
}

std::vector<std::string> SokobanSolver::getCleanMap()
{
	return this->m_clean_map;
}

std::vector<std::string> SokobanSolver::getMap()
{
	return this->m_orig_map;
}

Position SokobanSolver::getRobotStart()
{
	Position robot_start;
	for (int y = 0; y < this->m_orig_map.size(); ++y) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); ++x) 
		{
			if (this->m_orig_map[y][x] == 'M')
				return Position(x,y);
		}	
	}	
	return Position(-1,-1);
}

std::vector<Position> SokobanSolver::getCansStart()
{	
	std::vector<Position> cans_start;
	for (int y = 0; y < this->m_orig_map.size(); ++y) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); ++x) 
		{
			if (this->m_orig_map[y][x] == 'J')
				cans_start.push_back(Position(x,y));
		}	
	}	
	return cans_start;
}

std::vector<Position> SokobanSolver::getGoalPositions()
{	
	std::vector<Position> goal_positions;
	for (int y = 0; y < this->m_orig_map.size(); ++y) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); ++x) 
		{
			if (this->m_orig_map[y][x] == 'G')
				goal_positions.push_back(Position(x,y));
		}	
	}	
	return goal_positions;
}

std::string SokobanSolver::getStartHash()
{
	std::string hash = "";
	for (const auto& line : this->m_orig_map)
		hash += line;
	return hash;
}
std::string SokobanSolver::solve()
{
	/*  
	https://www.codewithc.com/breadth-first-search-in-c/
	
	Breath first algorithm : 
	Consider an input graph ‘g’ and its root node ‘v’
	1) Create a queue q
	2) Place v onto ‘q’
	3) Mark the root node ‘v’
	4) while q is not empty:
	5) t ← q.dequeue()
	6) if r is the target or what you are searing: return r
	7) for all edges e in g.adjacentEdges(r) do
	8) o ← g.adjacentVertex(r,e)
	9) if o is not marked: mark o
	10) Place o onto q
	11) return null
	*/

	// State queue, containing the states from one layer of breath first.
	std::queue<State*> state_queue;
	
	// The starting State with nullptr parent.
	State* start_state = new State(getRobotStart(), getCansStart(), nullptr);
	
	// Set static members in State.
	State::s_map             = getMap();
	State::s_clean_map       = getCleanMap();
	State::s_goals           = getGoalPositions();
	State::s_illegal_can_pos = generateIllegalCanPositions();
	
	// Push start_state onto state_queue and insert hash.
	if constexpr (PRINT_DEBUG) std::cout << "Pushing start state to queue....." << std::endl;
	state_queue.push(start_state);
	this->visited_states.insert(start_state->m_hash);
	
	// Current state.
	State* current_state = start_state;
		
	while (not state_queue.empty()) 
	{
		if constexpr (PRINT_DEBUG) std::cin.ignore();
		current_state = state_queue.front();
		state_queue.pop();
		if constexpr (PRINT_DEBUG) std::cout << "\n" << *current_state;

		// Are we done?
		if (current_state->isGoal())
			return getSolution(current_state);

		// Check the moves of all directions and push the states onto the vector.
		if (const auto& up_state = current_state->checkMove(State::MoveDirection::UP))
		{
			if (const auto& [it, success] = this->visited_states.insert(up_state->m_hash); success)
			{
				if constexpr (PRINT_DEBUG) std::cout << "Pushing up state to queue....." << std::endl;
				if constexpr (PRINT_DEBUG) std::cout << "up state hash....." << up_state->m_hash << std::endl;
				state_queue.push(up_state);	
			}
		}
		if (const auto& down_state = current_state->checkMove(State::MoveDirection::DOWN))
		{
			if (const auto& [it, success] = this->visited_states.insert(down_state->m_hash); success)
			{
				if constexpr (PRINT_DEBUG) std::cout << "Pushing down state to queue....." << std::endl;
				if constexpr (PRINT_DEBUG) std::cout << "down state hash....." << down_state->m_hash << std::endl;
				state_queue.push(down_state);	
			}
		}
		if (const auto& left_state = current_state->checkMove(State::MoveDirection::LEFT))
		{
			if (const auto& [it, success] = this->visited_states.insert(left_state->m_hash); success)
			{
				if constexpr (PRINT_DEBUG) std::cout << "Pushing left state to queue....." << std::endl;
				if constexpr (PRINT_DEBUG) std::cout << "left state hash....." << left_state->m_hash << std::endl;
				state_queue.push(left_state);
			}
		}
		if (const auto& right_state = current_state->checkMove(State::MoveDirection::RIGHT))
		{
			if (const auto& [it, success] = this->visited_states.insert(right_state->m_hash); success)
			{
				if constexpr (PRINT_DEBUG) std::cout << "Pushing right state to queue....." << std::endl;
				if constexpr (PRINT_DEBUG) std::cout << "right state hash....." << right_state->m_hash << std::endl;
				state_queue.push(right_state);
			}
		}
		
		if constexpr (PRINT_DEBUG) std::cout << "Current has : " << current_state->m_hash << std::endl;
	}
	
	// no solution found
	return "";
}

std::string SokobanSolver::getSolution(State* solution_state)
{
	
	Position d_pos;
	std::string solution = "";

	for (State* state = solution_state;  state->m_parent != nullptr ; state = state->m_parent) 
	{
		d_pos = state->m_robot - state->m_parent->m_robot;
		
		if (d_pos.x == 0  && d_pos.y == -1)
		{
			// Have we pushed a can?
			if (state->m_can != state->m_parent->m_can)
				solution += "U";
			else
				solution += "u";
		}
		else if (d_pos.x == 0  && d_pos.y == +1)
		{
			if (state->m_can != state->m_parent->m_can)
				solution += "D";
			else
				solution += "d";
		}
		else if (d_pos.x == -1  && d_pos.y == 0)
		{
			if (state->m_can != state->m_parent->m_can)
				solution += "L";
			else
				solution += "l";
		}
		else if (d_pos.x == +1  && d_pos.y == 0)
		{
			if (state->m_can != state->m_parent->m_can)
				solution += "R";
			else
				solution += "r";
		}
		else
		{
			return "[ERROR] : d_pos non valid size...";
		}
	}
	// Return the reversed solution string.
	std::reverse(solution.begin(),solution.end());
	


	for (int i = 0; i < this->m_map_name.length(); i++) {
		if (this->m_map_name[i] == '/')
			this->m_map_name = this->m_map_name.substr(i + 1,this->m_map_name.length());
	}

	std::cout << "solution 1 : " << solution << std::endl;

	solution = cvtAbs2RelActions(solution);

	std::cout << "solution 2 : " << solution << std::endl;

	std::ofstream output_file;
	output_file.open("solutions/" + this->m_map_name);
	output_file << solution;
	output_file.close();

	return solution;
}

std::string SokobanSolver::cvtAbs2RelActions(std::string solution)
{
	
	solution = "u" + solution;
	
	std::string result = "";

	for (size_t i = 0; i < solution.length() - 1; ++i) 
	{

		const std::string pair = {solution[i],solution[i + 1]};
		const std::string pair_lc = {char(std::tolower(pair[0])),char(std::tolower(pair[1]))};

		// orientation correction
		{
			static std::unordered_map<std::string,std::string> lut = 
			{
				{"lr","u"},
				{"lu","r"},
				{"ld","r"},
				{"rl","u"},
				{"ru","l"},
				{"rd","r"},
				{"ul","l"},
				{"ur","r"},
				{"ud","u"},
				{"dl","r"},	
				{"dr","l"},
				{"du","u"}
			};

			if (pair_lc[0] != pair_lc[1])
				result += lut[pair_lc];
		}
		// translation correction
		{
			result += (std::isupper(pair[1])) ? "pb" : "f";
		}
	}

	return result;
}

