#include "SokobanSolver.hpp"
#include <iostream>
#include <cstddef>
#include <fstream>
#include <queue>
#include <string>
#include <vector>

SokobanSolver::SokobanSolver() {}

SokobanSolver::SokobanSolver(std::string map)
{
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
	for (int y = 0; y < this->m_orig_map.size(); y++) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); x++) 
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
	for (int y = 0; y < this->m_orig_map.size(); y++) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); x++) 
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
	for (int y = 0; y < this->m_orig_map.size(); y++) 
	{
		for (int x = 0; x < this->m_orig_map[y].length(); x++) 
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
	for (auto line : this->m_orig_map)
		hash += line;
	return hash;
}
std::string SokobanSolver::solve()
{
/*  https://www.codewithc.com/breadth-first-search-in-c/
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
	
	// The starting State
	State* start_state = new State(getRobotStart(),getCansStart(),NULL,getMap());
	start_state->m_goal = getGoalPositions();
	start_state->m_clean_map = getCleanMap();

	// Push start_state onto state_queue and insert hash.
	std::cout << "Pushing start state to queue....." << std::endl;
	state_queue.push(start_state);
	this->visited_states.insert(start_state->m_hash);
	
	// Current state.
	State* current_state = start_state;
	
	// Layer counter.
	size_t layer = 0;
		
	while (not state_queue.empty())  
	{
		current_state = state_queue.front();
		state_queue.pop();
		std::cout << "\n" << *current_state;
		std::cin.get();
		
		auto [it,success] = this->visited_states.insert(current_state->m_hash);
		
		// Check the moves of all directions and push the states onto the vector.
		if (auto up_state = current_state->checkMove(State::MoveDirection::UP))
		{
			if (auto [it,success] = this->visited_states.insert(up_state->m_hash);success){
				std::cout << "Pushing up state to queue....." << std::endl;
				state_queue.push(up_state);	
			}
		}
		if (auto down_state = current_state->checkMove(State::MoveDirection::DOWN))
		{
			if (auto [it,success] = this->visited_states.insert(down_state->m_hash);success){
				std::cout << "Pushing down state to queue....." << std::endl;
				state_queue.push(down_state);	
			}
		}
		if (auto left_state = current_state->checkMove(State::MoveDirection::LEFT))
		{
			if (auto [it,success] = this->visited_states.insert(left_state->m_hash);success){
				std::cout << "Pushing left state to queue....." << std::endl;
				state_queue.push(left_state);
			}
		}
		if (auto right_state = current_state->checkMove(State::MoveDirection::RIGHT))
		{
			if (auto [it,success] = this->visited_states.insert(right_state->m_hash);success){
				std::cout << "Pushing right state to queue....." << std::endl;
				state_queue.push(right_state);
			}
		}
		// Now state vector contains all the states in a breath first search layer.

		// If the goal State is found as the first element of the queue, return it as success and stop.
		if (current_state->isGoal())
		{
			return "[INFO] : Solution found.";
		}
		layer++;
		
	}
	return "[ERROR] : No solution was found.";
}

