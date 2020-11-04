#include <cstddef>
#include <iostream>
#include <tuple>
#include <optional>
#include <string>
#include <vector>
#include <algorithm>

#include "Position.hpp"
#include "debug.h"
#include "State.hpp"

State::State(const Position& robot, const std::vector<Position>& cans, State* parent)
	: m_robot(robot), m_can(cans), m_parent(parent)
{
	generateHash();
}

State::~State() {}

void State::generateHash()
{
	// static std::string rob_pos;
	// rob_pos = std::to_string(m_robot.x) + std::to_string(m_robot.y);

	m_hash += (std::to_string(m_robot.x) + std::to_string(m_robot.y));
	for (const auto& can : m_can)
	{
		m_hash += std::to_string(can.x) + std::to_string(can.y);
	}
}

bool State::isWallBlocking(const Position& desired_position)
{
	return (s_clean_map[desired_position.y][desired_position.x] == 'X');
}

int State::isCanBlocking(const Position& desired_position)
{
	static int can_idx;
	for (can_idx = 0; can_idx < this->m_can.size(); ++can_idx)
	{
		if (this->m_can[can_idx] == desired_position)
			return can_idx;
	}

	return -1;
}

bool State::isCanMovable(size_t can_indx)
{
	static Position des_can_pos;
	des_can_pos = this->m_can[can_indx] + (this->m_can[can_indx] - this->m_robot);

	if constexpr (PRINT_DEBUG) std::cout << "Desired can position, in isCanMoveable() : " << des_can_pos << std::endl;

	if (isWallBlocking(des_can_pos))
		return false;

	// Is there a goal on the other side?
	for (const auto& goal : s_goals)
	{
		if (goal == des_can_pos)
			return true;
	}

	for (const auto& can : this->m_can)
	{
		if (can == des_can_pos)
			return false;
	}

	return true;
}

bool State::isCanDeadlocked(const Position& des_can_pos)
{
	return std::find(this->s_illegal_can_pos.begin(),this->s_illegal_can_pos.end(), des_can_pos) != this->s_illegal_can_pos.end();
}

State* State::checkMove(const Position& desired_position)
{
	static Position d_pos;
	d_pos = desired_position - this->m_robot;

	// Is there a wall
	if (isWallBlocking(desired_position))
	{
		if constexpr (PRINT_DEBUG) std::cout << "A wall is blocking..." << std::endl;
		return nullptr;
	}

	// We move the can.
	if (const auto& can_indx = isCanBlocking(this->m_robot + d_pos); can_indx != -1)
	{
		if constexpr (PRINT_DEBUG) std::cout << "A can is blocking..." << std::endl;
		if (isCanMovable(can_indx))
		{
			// The cans for the new state.
			static std::vector<Position> new_cans;
			new_cans = this->m_can;

			new_cans[can_indx] += d_pos;

			if (isCanDeadlocked(new_cans[can_indx]))
				return nullptr;

			if constexpr (PRINT_DEBUG) std::cout << "We push can to " << new_cans[can_indx] << std::endl;

			return new State((this->m_robot + d_pos), new_cans, this);
		}
		else
		{
			if constexpr (PRINT_DEBUG) std::cout << "The can is not movable..." << std::endl;
			return nullptr;
		}
	}
	else
	{
		if constexpr (PRINT_DEBUG) std::cout << "Nothing is blocking..." << std::endl;
		return new State((this->m_robot + d_pos), this->m_can, this);
	}
}

State* State::checkMove(MoveDirection dir)
{
	switch (dir)
	{
		case MoveDirection::UP:
			if constexpr (PRINT_DEBUG) std::cout << "\nchecking up.." << std::endl;
			return checkMove(Position(this->m_robot.x, this->m_robot.y - 1));

		case MoveDirection::DOWN:
			if constexpr (PRINT_DEBUG) std::cout << "\nchecking down.." << std::endl;
			return checkMove(Position(this->m_robot.x, this->m_robot.y + 1));

		case MoveDirection::LEFT:
			if constexpr (PRINT_DEBUG) std::cout << "\nchecking left.." << std::endl;
			return checkMove(Position(this->m_robot.x - 1, this->m_robot.y));

		case MoveDirection::RIGHT:
			if constexpr (PRINT_DEBUG) std::cout << "\nchecking right.." << std::endl;
			return checkMove(Position(this->m_robot.x + 1, this->m_robot.y));
	};

	return nullptr;
}

bool State::isGoal()
{
	return std::all_of(this->s_goals.begin(), this->s_goals.end(), [&](const auto& g){
		return std::find(this->m_can.begin(), this->m_can.end(), g) != this->m_can.end();
	});
}

std::ostream& operator<< (std::ostream& os, const State& state)
{
	static std::vector<std::string> print_map;
	print_map = state.s_clean_map;

	for (const auto& can : state.m_can)
		print_map[can.y][can.x] = 'J';

	for (const auto& goal : state.s_goals)
		print_map[goal.y][goal.x] = 'G';

	print_map[state.m_robot.y][state.m_robot.x] = 'M';

	for (const auto& line : print_map)
		os << line << std::endl;

	return os;
}

