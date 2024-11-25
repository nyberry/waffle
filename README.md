# Waffle Solver
My attempt to use python to find an optimal solution to this addictive little puzzle.

![example](https://github.com/nyberry/waffle/blob/main/waffle1039.gif)

## Description

- **`readWaffle.py`**: This script reads the day's Waffle puzzle from [https://wafflegame.net](https://wafflegame.net). The `readWaffle()` function returns an ordered list of tuples, each representing one of the puzzle's 21 tiles with its letter and color.

- **`sortedWordList`**: A list of 5-letter English words (5,792 words in total). By filtering this list to only include words that can be formed from the given letters, the subsequent recursive algorithm becomes more efficient.

- **`fitWords`**: A recursive constraint-satisfaction function that attempts to fill the Waffle grid by placing words from the filtered word list. It takes into account overlaps and green tiles (which have fixed positions).

- **`solve`**: This function uses a depth-limited recursive search to find a sequence of letter-pair swaps that transform the initial grid into the target grid. The recursion depth is limited to 10 because the creators of the Waffle game have confirmed that any puzzle can be solved in 10 moves or fewer. The `preSolve` function optimizes this search by first removing tiles that are already in the correct position or pairs that can be swapped into place in a single move.

- The recursion depth is limited to **10** because the creators of the Waffle game have confirmed that any puzzle can be solved in 10 moves or fewer.

- **`makeAnimation.py`**: This script generates a GIF (`waffle{n}.gif` where `n` is the puzzle number) to visually render one of the optimal solutions.

## Features

- Solve Waffle puzzles by determining optimal word placements.
- Efficient search using recursive algorithms with constraint satisfaction.
- Generate an animated GIF of the solution.
