# aibot

Sokoban is a puzzle game in which an actor can push objects (in this case tomato cans) around within a map. The objective is to move all objects onto goal positions; the puzzle is considered solved when each object is uniquely placed on a goal position. In this project, a LEGO® MINDSTORMS® EV3-based mobile robot (the `aibot`) is used to navigate a physical Sokoban map with real tomato cans.

![aibot][img-aibot]

The objective is to: (a) solve the Sokoban puzzle by computing a sequence of actions (planned solution), and (b) design and build a mobile robot that can physically execute the solver’s planned solution by moving the cans onto the goal positions on the physical map. The overall problem is decomposed into two main components:

- Designing and programming a mobile robot that can robustly navigate the physical Sokoban map with the ability to push cans; the robot must be interfaced using a sequence of actions.

- Implementing a Sokoban solver which can solve an arbitrary map with a maximum size of 50×50 tiles within a reasonable time span and produce a sequence of actions for the robot to execute.

The mobile robot is controlled in `Python` using the [python-ev3dev2] library, and the solver is written `C++` using a breadth-first search algorithm. The full project is [documented here][project-pdf].

<!-- LINKS -->

[project-pdf]: /assets/rb-aibot-report.pdf
[python-ev3dev2]: https://github.com/ev3dev/ev3dev-lang-python
[img-aibot]: /assets/img/robot-overview.pdf
