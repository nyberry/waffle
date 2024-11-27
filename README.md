# Waffle Solver
Find an optimal solution to this tricky little puzzle.

![example]https://github.com/nyberry/waffle/blob/main/animations/waffle1040.gif

## Description

- **`readWaffle.py`**: This script reads the day's Waffle puzzle from [https://wafflegame.net](https://wafflegame.net). The `readWaffle()` function returns an ordered list of tuples, each representing one of the puzzle's 21 tiles with its letter and color.

- **`sortedWordList`**: A list of 5-letter English words (5,792 words in total). Filtering this list to only include words that can be formed from the given letters makes the subsequent recursive algorithm more efficient.

- **`fitWords`**: A recursive constraint-satisfaction function that attempts to fill the Waffle grid by placing words from the filtered word list. It takes into account overlaps and green tiles (which have fixed positions).

- **`solve`**: A depth-limited recursive search function to find sequences of letter-pair swaps that transform the initial grid into the target grid. The recursion depth is limited to 10 because the creators of the Waffle game have confirmed that any puzzle can be solved in 10 moves or fewer. The search will yield all sequences which solve the puzzle in 10 swaps or fewer. The `preSolve` function optimizes this search by first removing tiles that are already in the correct position, and swaps any pairs where both letters can be swapped into their correct place in a single move.

- **`makeAnimation.py`**: This script generates a GIF (`waffle{n}.gif` where `n` is the puzzle number) to visually render a minimum-length solutions.

## Features

- Solve the Waffle puzzle by determining correct word placement.
- Search for the shortest sequence of swaps to solve the puzzle.
- Generate an animated GIF of the solution.
