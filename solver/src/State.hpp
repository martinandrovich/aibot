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

	State();
	State(Position robot, std::vector<Position> cans, State* parent,std::vector<std::string> map);
	~State();

	State*                  checkMove(Position desired_position);
	State*                  checkMove(MoveDirection dir);
	State*                  up();
	State*                  down();
	State*                  left();
	State*                  right();

	void                     generateHash();
	std::vector<std::string> generateStateMap();
	bool                     isWallBlocking(Position desired_position);
	bool                     isGoal();
	size_t                   isCanBlocking(Position desired_position);
	bool                     isCanMovable(size_t can_indx);

	size_t                   isCanBlockingAndMovable(Position desired_position);

	inline static std::vector<std::string> m_clean_map = {};
	inline static std::vector<std::string> m_map = {};
	inline static std::vector<Position> m_goal = {};

	friend std::ostream& operator<<(std::ostream& os, const State& state);

	std::vector<Position>    m_can;
	Position                 m_robot;
	std::string              m_hash = "";
	State*                   m_parent = nullptr;
private:
	bool                     isValid();
};
