#pragma once
#include <cstddef>
#include <iostream>
#include <tuple>
#include "Position.hpp"
#include "debug.h"
#include "State.hpp"
#include <optional>
#include <string>
#include <vector>
#include <algorithm>


State::State() {}

State::State(Position robot, std::vector<Position> cans, State* parent, std::vector<std::string> map) 
	: m_robot(robot), m_can(cans), m_parent(parent) 
{ 
	generateHash(); 
	m_map = map;
}

State::~State(){}

void State::generateHash()
{
	std::string rob_pos = std::to_string(m_robot.x) + std::to_string(m_robot.y);
	m_hash             += rob_pos;
	for (auto can : m_can) 
	{
		m_hash += std::to_string(can.x) + std::to_string(can.y);
	}
}

bool State::isWallBlocking(Position desired_position)
{
	return (m_clean_map[desired_position.y][desired_position.x] == 'X'); 
}

size_t State::isCanBlocking(Position desired_position)
{
	size_t can_idx = 0;
	for (; can_idx < this->m_can.size(); can_idx++) {	
		if (this->m_can[can_idx] == desired_position)
			return can_idx;
	}
	return -1;
}

bool State::isCanMovable(size_t can_indx)
{
	Position des_can_pos = this->m_can[can_indx] + (this->m_can[can_indx] - this->m_robot);

	if (isWallBlocking(des_can_pos))
		return false;

	for (auto can : this->m_can) {
		if (can == des_can_pos)
			return false;
	}

	return true;
}

bool State::isCanDeadlocked(Position des_can_pos)
{
	return std::find(this->m_illegal_can_pos.begin(),this->m_illegal_can_pos.end(), des_can_pos) != this->m_illegal_can_pos.end();
}

State* State::checkMove(Position pos)
{

	// 1) if (space is free)              
	// 2) else if (is can move valid)    
	// 3) else nullptr

	// 1) free space V
	// 2) can is present (movable) V
	// 3) can is present (non-movable) V
	// 4) wall is present V
	
	Position d_pos = pos - this->m_robot;

	// Is there a wall
	if ( isWallBlocking(pos) )
	{
		if (PRINT_DEBUG) std::cout << "A wall is blocking..." << std::endl;
		return nullptr; 
	}

	// We move the can.
	if (auto can_indx = isCanBlocking( this->m_robot + d_pos); can_indx != -1) 
	{
		if (PRINT_DEBUG) std::cout << "A can is blocking..." << std::endl;
		if (isCanMovable(can_indx)) {
			// The cans for the new state.
			std::vector<Position> new_cans = this->m_can;
			new_cans[can_indx] += d_pos;
			if (isCanDeadlocked(new_cans[can_indx]))
				return nullptr;
			if (PRINT_DEBUG) std::cout << "We push can to " << new_cans[can_indx] << std::endl;

			return new State( (this->m_robot + d_pos) , new_cans ,this , this->m_map);
		}
		else
		{
			if (PRINT_DEBUG) std::cout << "The can is not movable..." << std::endl;
			return nullptr;
		}
	}
	else
	{
		if (PRINT_DEBUG) std::cout << "Nothing is blocking..." << std::endl;
		return new State( (this->m_robot + d_pos) , this->m_can ,this , this->m_map);
	}
}

State* State::checkMove(MoveDirection dir)
{
	switch (dir) 
	{
		case MoveDirection::UP:
			if (PRINT_DEBUG) std::cout << "\nchecking up.." << std::endl;
			return checkMove( Position(this->m_robot.x, this->m_robot.y - 1) );
		case MoveDirection::DOWN:
			if (PRINT_DEBUG) std::cout << "\nchecking down.." << std::endl;
			return checkMove( Position(this->m_robot.x, this->m_robot.y + 1) );
		case MoveDirection::LEFT:
			if (PRINT_DEBUG) std::cout << "\nchecking left.." << std::endl;
			return checkMove( Position(this->m_robot.x - 1, this->m_robot.y) );
		case MoveDirection::RIGHT:
			if (PRINT_DEBUG) std::cout << "\nchecking right.." << std::endl;
			return checkMove( Position(this->m_robot.x + 1, this->m_robot.y) );
	};
}

bool State::isGoal()
{
	
	bool res = std::all_of(this->m_goal.begin(), this->m_goal.end(), [&]( const auto& g ){ 
		return std::find( this->m_can.begin(), this->m_can.end(), g ) != this->m_can.end(); 
	} );
	return res;
}

std::ostream& operator<<(std::ostream& os, const State& state)
{
	std::vector<std::string> print_map = state.m_clean_map;
	for (auto can : state.m_can) {
		print_map[can.y][can.x] = 'J';
	}
	for (auto goal : state.m_goal) {
		print_map[goal.y][goal.x] = 'G';
	}
	
	print_map[state.m_robot.y][state.m_robot.x] = 'M';

	for (auto line : print_map) {
		os << line << std::endl;
	}


	return os;
}

