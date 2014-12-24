2048: An AI Agent
-----------------

This package provides an artificially intelligent solver for the popular puzzle game, 2048 (http://gabrielecirulli.github.io/2048/). 

The game 2048 is a great strategy game to which AI principles can be applied. It is straight- forward to emulate gameplay and quantify results. Further, as it is a very difficult game for humans to win, we are interested in noting how much better a computer can perform against humans. All utility is received at the point when a 2048 tile is achieved, and there are no intermediary rewards. Further, as the computer only adds a random element, it is not adversarial. As this is not a classic two-player zero sum game, it is again more novel.

The player is based off of the expectimax algorithm and employs precomputation of states and variable search depth to allow quick solving. When run in the normal state, the agent is able to achieve a nearly 75% success rate and an average completion time (time to end state - a full board with no possible moves) of 69 seconds. 

For a full description and analysis of the agent, please read the attached Agent Summary Report pdf.

