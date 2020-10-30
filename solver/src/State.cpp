#pragma once
#include <iostream>
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
	std::cout << "generate hash a State...." << std::endl;
	generateHash(); 
	m_map = map;
	std::cout << "Making a State...." << std::endl;
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
	// Is a wall blocking?
	return (m_map[desired_position.y][desired_position.x] == 'X');
}

std::optional<Position> State::isCanMoveValid(Position desired_position)
{	
	bool is_can_blocking  = false;
	bool is_can_movable   = false;
	Position d_pos = this->m_robot - desired_position;
	Position can_above_me;
	// Is a can blocking?
	for (auto can : m_can) 
	{
		if (can == m_robot + d_pos)
		{
			is_can_blocking = true;
			can_above_me    = can;
		}
	}	
	// Can I move the can?
	if (m_map[desired_position.y][desired_position.x] != 'X')
		is_can_movable = true;

	// If I can move the can, we choose to do so.
	if (is_can_blocking and is_can_movable)
		return desired_position;
	else
		return std::nullopt;
}

State* State::checkMove(Position pos)
{
	Position d_pos = pos - this->m_robot;
	std::cout << "----" << std::endl;
	std::cout << "this->m_robot : " << this->m_robot << std::endl;
	std::cout << "d_pos : " << d_pos << std::endl;
	std::cout << "pos : " << pos << std::endl;
	std::cout << "----" << std::endl;
	

	// First we check if a wall is blocking.
	bool is_wall_blocking = isWallBlocking(this->m_robot + d_pos);
	if (is_wall_blocking)
	{
		std::cout << "Wall is blocking" << std::endl;
		return nullptr;
	}
	// Is there a can in the way, and if so, can we move it.
	else if (auto can_pos = isCanMoveValid( this->m_robot + d_pos)) 
	{
		std::cout << "I have found a can in my way!" << std::endl;
		// The cans for the new state.
		std::vector<Position> new_cans = this->m_can;
		
		// Determine the can we are moving
		for (int i = 0; i < m_can.size(); i++) 
		{
			// Update the new_cans array to the new state.
			if (this->m_can[i] + d_pos == Position(can_pos->x + d_pos.x,can_pos->y + d_pos.y) )
			{
				new_cans[i] += d_pos;
			}
		}
		std::cout << "We push can" << std::endl;
		return new State( (this->m_robot + d_pos) , new_cans ,this , this->m_map);
	}
	// No can or wall was in the way, so we simply just go up.
	else
	{
		std::cout << "No obsticales" << std::endl;
		return new State( (this->m_robot + d_pos) , this->m_can, this, this->m_map );
	}
}

State* State::checkMove(MoveDirection dir)
{
	switch (dir) 
	{
		case MoveDirection::UP:
			return checkMove( Position(this->m_robot.x, this->m_robot.y - 1) );
		case MoveDirection::DOWN:
			return checkMove( Position(this->m_robot.x, this->m_robot.y + 1) );
		case MoveDirection::LEFT:
			return checkMove( Position(this->m_robot.x - 1, this->m_robot.y) );
		case MoveDirection::RIGHT:
			return checkMove( Position(this->m_robot.x + 1, this->m_robot.y) );
	};
}

bool State::isGoal()
{
	std::cout << "isGoal initiated....." << std::endl;
	std::cout << "m_can.size() : " << m_can.size() << std::endl;
	std::cout << "m_goal.size() : " << m_goal.size() << std::endl;
	std::cout << "m_robot " << m_robot << std::endl;
	std::cout << "m_hash" << m_hash << std::endl;

	for (auto can : this->m_can) {
		std::cout << "can : " << can << std::endl;
	}
	for (auto goal : this->m_goal) {
		std::cout << "goal : " << goal << std::endl; 
	}

	bool res = std::all_of(this->m_goal.begin(), this->m_goal.end(), [&]( const auto& g ){ 
		return std::find( this->m_can.begin(), this->m_can.end(), g ) != this->m_can.end(); 
	} );
	std::cout << "res : " << res << std::endl;
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

