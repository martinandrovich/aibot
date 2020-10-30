#pragma once
#include <cstddef>
#include <iostream>
#include <tuple>
#include "Position.hpp"

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

bool State::isSpaceFree(Position desired_position)
{
	return (m_map[desired_position.y][desired_position.x] == '.' or m_map[desired_position.y][desired_position.x] == 'G'); 
}

bool State::isCanBlocking(Position desired_position)
{
	for (auto can : this->m_can) {
		if (can == desired_position)
			return true;
	}
	return false;
}

size_t State::isCanBlockingAndMovable(Position desired_position)
{	
	bool is_can_blocking  = false;
	bool is_can_movable   = false;
	Position d_pos        = desired_position - this->m_robot;
	Position desired_can_position = desired_position + d_pos;

	// Is a can blocking?
	size_t can_indx = 0;
	for (;can_indx < m_can.size();can_indx++) {	
		if (m_can[can_indx] == desired_position)
		{
			std::cout << "I have found a can in my way!" << std::endl;
			is_can_blocking = true;
			break;
		}
	}
	// is no can blocking
	if (not is_can_blocking)
		return -1;
	// can we move the blocking can, return index if true.
	if (m_map[desired_can_position.y][desired_can_position.x] != 'X' and m_map[desired_can_position.y][desired_can_position.x] != 'J')
		return can_indx;
	return -1;
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

	// We go up.
	if ( isSpaceFree(pos) )
		return new State( (this->m_robot + d_pos) , this->m_can, this, this->m_map );
	// We move the can.
	if (auto can_indx = isCanBlockingAndMovable( this->m_robot + d_pos); can_indx != -1) 
	{
		// The cans for the new state.
		std::vector<Position> new_cans = this->m_can;
		new_cans[can_indx]            += d_pos;
		std::cout << "We push can to " << new_cans[can_indx] << std::endl;
		return new State( (this->m_robot + d_pos) , new_cans ,this , this->m_map);
	}
	// There must be either a wall or a unmovable can.
	else
	{
		std::cout << "Cannot go this way..." << std::endl;
		return nullptr; 
	}
}

State* State::checkMove(MoveDirection dir)
{
	switch (dir) 
	{
		case MoveDirection::UP:
			std::cout << "\nchecking up.." << std::endl;
			return checkMove( Position(this->m_robot.x, this->m_robot.y - 1) );
		case MoveDirection::DOWN:
			std::cout << "\nchecking down.." << std::endl;
			return checkMove( Position(this->m_robot.x, this->m_robot.y + 1) );
		case MoveDirection::LEFT:
			std::cout << "\nchecking left.." << std::endl;
			return checkMove( Position(this->m_robot.x - 1, this->m_robot.y) );
		case MoveDirection::RIGHT:
			std::cout << "\nchecking right.." << std::endl;
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

