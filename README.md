# Waffle Solver
My attempt to use python to find an optimal solution to this addictive little puzzle.

![example](https://github.com/nyberry/waffle/blob/main/waffle1039.gif)


The first thing is to read the day's Waffle from htpps://wafflegame.net. This is handled by readWaffle() which returns an ordered list of tuples representing each of the puzzle's 21 tiles letter and color.

sortedWordList is a list of English 5-letter words. 5792 of them. Filtering the list, keeping only the words which can be formed from the given letter, makes the following recursive algorith faster.

fitWords() is a recursive constraint-satisfaction function. Calling it will ultimately yield any arrangement of words from the list which will fit in the grid, taking into account overlaps and the green tiles which have known fixed positions.

solve() uses a depth limited recursive search to find any sequence of letter-pair swaps to transform the initial permutation to the target permutation. PreSolve() first trims this list by removing any tiles which are already in the correct position, or pairs where both elements can be put in the correct position after a simple swap. This makes the recursive function solve() faster.

The recursion depth is limited to 10, because the makers of the Waffle game have told us that the puzzle can always be solved in 10 turns or less.

The optimum solutions will be the sequences of swaps of the minimum length.

makeAnimation() renders one of the optimal solutions as waffle{n}.gif where n is the puzzle number.
