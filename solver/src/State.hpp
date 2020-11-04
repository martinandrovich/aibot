#pragma once
#include <cstddef>
#include <iterator>
#include <ostream>
#include <string>
#include <vector>
#include "Position.hpp"
#include <optional>
#include "debug.h"
/*! \class State
 *  \brief Brief class description
 *
 *  Detailed description
 */
class State
{
public:

	enum class MoveDirection{ UP, DOWN, LEFT, RIGHT };

	State(const Position& robot, const std::vector<Position>& cans, State* parent = nullptr);
	~State();

	State*                   checkMove(const Position& desired_position);
	State*                   checkMove(MoveDirection dir);

	void                     generateHash();
	bool                     isWallBlocking(const Position& desired_position);
	bool                     isGoal();
	int                      isCanBlocking(const Position& desired_position);
	bool                     isCanMovable(size_t can_indx);
	bool                     isCanDeadlocked(const Position& des_can_pos);

	inline static std::vector<std::string> s_clean_map;
	inline static std::vector<std::string> s_map;
	inline static std::vector<Position>    s_goals;
	inline static std::vector<Position>    s_illegal_can_pos;

	friend std::ostream& operator<< (std::ostream& os, const State& state);

	std::vector<Position>    m_can;
	Position                 m_robot;
	std::string              m_hash = "";
	State*                   m_parent = nullptr;

};
