# USC - CSCI561 - Foundations Of Artificial Intelligence Course Programming Assignments

This repository has all of the programming assignments in the Foundations of Artificial Intelligence class at the University of Southern California in the Fall 2021 semester.

## [Homework 1](https://github.com/ParsaHejabi/USC-CSCI561-FoundationsOfArtificialIntelligence/tree/main/HW1)

This is a programming assignment in which you will apply AI search techniques to lead an exploration team to explore an underground cave system such as the one shown in picture below.

![Cave Illustration](/images/HW1-1.jpg "Cave Illustration")

Conceptually speaking, each cave system is like a sophisticated 3D maze, as shown in above image, which consists of a grid of points (not cells) with (x, y, z) locations in which your agent may use one of the 18 elementary actions (see their definitions below), named X+, X-, Y+, Y-, Z+, Z-; X+Y+, X-Y+, X+Y-, X-Y-, X+Z+, X+Z-, X-Z+, X-Z-, Y+Z+, Y+Z-, Y- +, Y-Z-; to move to one of the 18 neighboring grid point locations. At each grid point, your agent is given a list of actions that are available for the current point your agent is at. Your agent can select and execute one of these available actions to move inside the 3D maze. For example, in above image, there is a “path” from (0,0,0) to (10,0,0) and to travel this path starting from (0,0,0), your agent would make ten actions: X+, X+, X+, X+, X+, X+, X+, X+, X+, X+, and visit the following list of grid points: (0,0,0), (1,0,0), (2,0,0), (3,0,0), (4,0,0), (5,0,0), (6,0,0), (7,0,0), (8,0,0), (9,0,0), (10,0,0). At each grid point, your agent is given a list of available actions to select and execute. For example, in the above image, at the grid point (60,45,30) there are two actions for your agent: Z+ for going up, and Y- for going backwards. At the grid point (60,103,97), the available actions are X+ and Y-. At (60,45,97), the three available actions are Y+, Z-, and X-Y+. If a grid point has no actions available, then that means such a point has nowhere to go. For example, the point (24,86,31) (not shown in above image) has nowhere to go and is not accessible.

![Movements](/images/HW1-2.png "Movements")

The 18 actions are defined as follows. They are roughly divided as “straight-move” and “diagonal-move” actions. As shown in above image, the six straight-move actions are X+, X-, Y+, Y-, Z+, Z-, and they allow your agent to move in a straight-line to the next grid point. The diagonal-move actions are further defined on xy, xz, and yz planes, respectively.

Your programming task is as follows. Given as inputs:

1. A list of grid points with their available
   actions
2. An entrance grid location, e.g., (0,0,0) in first image, and
3. An exit grid location, e.g., (100,103,97) , your program must search in the maze configuration and find the optimal shortest path from the entrance to the exit, using a list of actions that are available along the way. Conceptually, the specification of a grid location and its associated actions is given as a grid location with a list of actions. For example (Note: The exact input format will be given in section 5 and 6 below),

```
   INPUT LINE: (60 45 97), Y+, Z-, X-Y+
   INPUT LINE: (60 46 97), Y-, Y+
   INPUT LINE: (60 45 96), Z+, Z-
   INPUT LINE: (59 46 97), X+Y-, X-Y+
```

is a specification, for first image example, that at the grid location (60,45,97), the available actions are Y+, Z-,
and X-Y+. At the grid (60,46,97), the available actions are Y- and Y+, and at the grid (60,45,96),
the available actions are Z+ and Z-, and at the grid (59,46,97), the available actions are X+Y- and
X-Y+ for moving diagonally on the xy plane.
Once your agent finds an optimal path from the entrance to the exit, your agent should output a
list of points that have been visited along the path. For example, if the entrance and exit would
be changed at (60,103,97) and (64,103,97) respectively, then the correct output path would be:

```
OUTPUT: (60,103,97), (61,103,97), (62,103,97), (63,103,97), (64,103,97).
```

To find the solution you will use the following algorithms:

- Breadth-first search (BFS)
- Uniform-cost search (UCS)
- A\* search (A\*).

### Breadth-first search (BFS)

In BFS, each move from one location to any of its neighbors counts for a unit path cost of 1. You do not need to worry about the fact that moving diagonally actually is a bit longer than moving along the North/South, East/West, and Up/Down directions. So, any allowed move from one location to an adjacent location costs 1.

### Uniform-cost search (UCS)

When running UCS, you should compute unit path costs in any of the 2D plane XY, XZ, YZ, on which you are moving. Let us assume that a grid location’s center coordinates projected to a 2D plane are spaced by a 2D distance of 10 units on X and Z plane respectively. That is, on the XZ plane, move from a grid location to one of its 4-connected straight neighbors incurs a unit path cost of 10, while a diagonal move to a neighbor incurs a unit path cost of 14 as an approximation to 10√𝟐 when running UCS.

### A\* search (A\*)

When running A*, you should compute an approximate integer unit path cost of each move as in the UCS case (unit cost of 10 when moving straight on a plane, and unit cost of 14 when moving diagonally . Notice for A*, you need to design an admissible heuristic for A\* for this problem.

### Example input

```
A*
100 200 100
0 0 0
3 3 0
4
0 0 0 7
1 1 0 7 10
2 2 0 7 10
3 3 0 10
```

### Example output

```
42
4
0 0 0 0
1 1 0 14
2 2 0 14
3 3 0 14
```

## [Homework 2](https://github.com/ParsaHejabi/USC-CSCI561-FoundationsOfArtificialIntelligence/tree/main/HW2)

![Go](/images/HW2-1.jpg "Go Game")

In this programming assignment, you will develop your own AI agents based on some of the AI techniques for Search, Game Playing, and Reinforcement Learning that you have learnt in class to play a small version of the Go game, called Go-5x5 or Little-Go, that has a reduced board size of 5x5. Your agent will play this Little-Go game against some basic as well as more advanced AI agents. Your agents will be graded based on their performance in these online game “tournaments” on Vocareum.com. Your objective is to develop and train your AI agents to play this Little-Go game as best as possible.

Go is an abstract strategy board game for two players, in which the aim is to surround more territory than the opponent. The basic concepts of Go (Little-Go) are very simple:

- Players: Go is played by two players, called Black and White.
- Board: The Go board is a grid of horizontal and vertical lines. The standard size of the board is 19x19, but in this homework, the board size will be 5x5.
- Point: The lines of the board have intersections wherever they cross or touch each other. Each intersection is called a point. Intersections at the four corners and the edges of the board are also called points. Go is played on the points of the board, not on the squares.
- Stones: Black uses black stones. White uses white stones.

The basic process of playing the Go (Little-Go) game is also very simple:

- It starts with an empty board,
- Two players take turns placing stones on the board, one stone at a time,
- The players may choose any unoccupied point to play on (except for those forbidden by the “KO” and “no-suicide” rules).
- Once played, a stone can never be moved and can be taken off the board only if it is captured.

The entire game of Go (Little-Go) is played based on two simple rules: Liberty (No-Suicide) and KO.

Image below shows the basic program structure. There is one game host and two players in each game. The Game Host keeps track of the game process, gets the next moves from the players in turn, judges if the proposed moves are valid, wipes out the dead stones, and finally judges the winner. Each of the two Players must output its next move in an exact given format (in a file called `output.txt`) with the intended
point (row and column) coordinates to the Game Host. The job of a player is very simple: take the previous and current states of the board (in a file called `input.txt`

Image below shows the basic program structure. There is one game host and two players in each game. The Game Host keeps track of the game process, gets the next moves from the players in turn, judges if the proposed moves are valid, wipes out the dead stones, and finally judges the winner. Each of the two Players must output its next move in an exact given format (in a file called `output.txt`) with the intended point (row and column) coordinates to the Game Host. The job of a player is very simple: take the previous and current states of the board (in a file called `input.txt`) from the host, and then output the next move back to the host.input) from the host, and then output the next move back to the host.

![Program Structure](/images/HW2-2.jpg "Program Structure")

The host keeps track of the game board while the two players make moves in turn. We will use a zero-based, vertical-first, start at the top-left indexing in the game board. So, location [0,0] is the top-left corner of the board, location [0,4] is the top-right corner, location [4,0] is the bottom-left corner, and location [4,4] is the bottom-right corner. An example of game state is shown in Figure 2, in which "1" denotes black stones, "2" denotes white stones, and "0" denotes empty positions. For manual players, we visualize the board as in the image on the right where X denotes the black stones and O denotes the white stones.

![Board](/images/HW2-3.png "Board")

### AI Players

Different AI Players are available for your agent to play against for the purpose of testing and/or grading.
Examples of these existing AI players include:

- Random Player: Moves randomly.
- Greedy Player: Places the stone that captures the maximum number of enemy stones
- Aggressive Player: Looks at the next two possible moves and tries to capture the maximum number of enemy stones.
- Alphabeta Player: Uses the Minimax algorithm (Depth<=2; Branching factor<=10) with alpha-beta pruning.
- QLearningPlayer: Uses Q-Learning to learn Q values from practice games and make moves intelligently under different game conditions.
- Championship Player: This is an excellent Little-Go player adapted from top-performing agents in previous iterations of this class.

### My Approach

I have used Minimax algorithm with Alpha-Beta pruning and I have beaten Random, Greedy, Aggressive, Alphabeta, QLearning player completely and playing 10 matches with the Championship player my agent won 5 times and lost 5 times.

## [Homework 3](https://github.com/ParsaHejabi/USC-CSCI561-FoundationsOfArtificialIntelligence/tree/main/HW3)

In this programming homework, you will implement a multi-layer perceptron (MLP) neural network and use it to classify hand-written digits shown in image below. You can use numerical libraries such as Numpy/Scipy, but machine learning libraries are NOT allowed (including
tensorflow (v1&v2), caffe, pytorch, torch, cxxnet, and mxnet). You need to implement feedforward/backpropagation as well as training process by yourselves.

![MNIST](/images/HW3-1.jpg "MNIST")

Built an MLP with 2 hidden layers and these configs:

```python
h1_layer_size = 256
h2_layer_size = 64
learning_rate = 0.1
epochs = 10
```

Achived `88.92%` accuracy.
