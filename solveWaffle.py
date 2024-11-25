from collections import Counter
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from readWaffle import readWaffle
from makeAnimation import *

# The waffle is represented as an ordered list of 21 letters.
# 6 five-letter words must be fitted to the waffle grid.

# map of word positions to list index; WORDMAP[0-2] map the rows and WORDMAP[3-5] map the columns
WORDMAP=[[0,1,2,3,4], [8,9,10,11,12], [16,17,18,19,20], [0,5,8,13,16], [2,6,10,14,18], [4,7,12,15,20]]

def main():
    # Check usage. Optionally provide an integer argumeht to read a puzzle from the archive
    if len(sys.argv) not in [1, 2]:
        sys.exit("Usage: python solveWaffle.py [puzzle] \nUse puzzle = 0 to run without scraping wafflegame.net (this is quicker for testing)")

    if len(sys.argv) == 2:  
        try:
            puzzle = int(sys.argv[1])
            if puzzle < 0:
                raise ValueError
        except ValueError:
            sys.exit("Error: puzzle must be a positive integer.")
    else:
        puzzle = None 

    # if no argument is provided, read today's waffle from web; unless puzzle value=0 in which case run a test case without reading from web
    if puzzle != 0:
        tiles, gameNumber = readWaffle(puzzle)
    else:
        # test case
        tiles= [('A', 'green'), ('R', 'yellow'), ('R', 'grey'), ('O', 'yellow'), ('N', 'green'), ('S', 'grey'), ('U', 'green'), ('O', 'grey'), ('M', 'yellow'), ('O', 'yellow'), ('T', 'green'), ('T', 'yellow'), ('E', 'yellow'), ('E', 'grey'), ('D', 'grey'), ('G', 'grey'), ('G', 'green'), ('U', 'grey'), ('R', 'green'), ('N', 'grey'), ('E', 'green')]
        gameNumber = 0
        
    # set original state and colors of the 21 letter tiles
    originalState, originalColors = getStateAndColors(tiles)

    # Import word list and filter it, keeping only words which can be made with the letters available
    with open('sortedWordList.txt','r') as file:
        wordlist = [line.strip().upper() for line in file]
    filteredWordlist = [word for word in wordlist if canMakeWord(word, originalState)]

    # Define starting arrangement with green tiles fixed, and swappable letters represented as "?"
    state = []
    swappableLetters = []
    for i in range(len(originalState)):
        if originalColors[i]=='green':
            state.append(originalState[i])
        else:
            state.append('?')
            swappableLetters.append(originalState[i])

    # Find all word arrangements that fit (without considering yellow tiles - can code this later if needed)
    validWordArrangements=[]
    for validWordArrangement in fitWords(filteredWordlist, state, swappableLetters):
        validWordArrangements.append(validWordArrangement)
    if not validWordArrangements:
        sys.exit("No valid word arrangements")
    elif len(validWordArrangements)>1:
        sys.exit(f'There are {len(validWordArrangements)} valid word arrangments so will need to consider yellow and grey tiles also (not yet coded)')
    else:
        targetState = validWordArrangements[0]
    
    # perform all swaps which result in both elements being correctly placed
    baseState, sequence = presolve(originalState.copy(), targetState)

    # find all solutions with depth-blimited recursive search
    min_swaps = math.inf
    for solution, state in solve(baseState, targetState, sequence, depth = 11-len(sequence)):
        if len(solution)<min_swaps:
            min_swaps = len(solution)
            swaps = solution
    if swaps:
        animationFilename = f'waffle{gameNumber}.gif'
        makeAnimation(originalState, targetState, swaps, animationFilename)
        sys.exit(f'Waffle solved and saved as {animationFilename}')
    else:
        sys.exit('no valid sequence of swaps')

# Function to get state and color from scraped list of tiles
def getStateAndColors(tiles):
    originalState = [tile[0] for tile in tiles]
    originalColors = [tile[1] for tile in tiles]
    return originalState, originalColors
    
# Function to check if a word can be made from the available letters
def canMakeWord(word, A):
    letterCount = Counter(A)
    wordCount = Counter(word)
    for letter, count in wordCount.items():
        if count > letterCount.get(letter, 0):
            return False
    return True

# Recursive function to find an arrangement of words that satifies the waffle grid constraints
def fitWords(filteredWordlist, state, swappableLetters, position = 0):
    if position == 6:  # Base case: all positions filled
        yield(state)
        return

    for word in filteredWordlist:
        tilesUsed = fits(state, word, position, swappableLetters)
        if tilesUsed:
            # Place word in the list
            newState = placeWord(state, word, position)

            # update available letters
            countAvailable = Counter(swappableLetters)
            countUsed = Counter(tilesUsed)
            updated_counts = countAvailable - countUsed
            newSwappableLetters = list(updated_counts.elements())

            # Recursive call; yield all valid solutions
            yield from fitWords(filteredWordlist, newState, newSwappableLetters, position + 1)

# Check if a word fits in the grid with current constraints
def fits(state, word, position, swappableLetters):
    tilesUsed = []
    for i, letterToFit in enumerate(word):
        existingLetter = state[WORDMAP[position][i]]
        if existingLetter != "?" and existingLetter != letterToFit:
            return False
        if existingLetter == "?":
            tilesUsed.append(letterToFit)

    #check if the fitting word can be formed from available tiles
    countAvailable = Counter(swappableLetters)
    countUsed =Counter(tilesUsed)       
    if all(countAvailable[letter] >= countUsed[letter] for letter in tilesUsed):
        return tilesUsed
    else:
        return False

# function to place a word in the grid
def placeWord(state, word, position):
    newState = state.copy()
    for i, letter in enumerate(word):
        newState[WORDMAP[position][i]] = letter
    return newState

# simplify the original permutation.
# Only keep letters that are in the wrong place
def presolve(A,B):
    sequence = []
    state = A
    c = [idx for idx in range(len(state)) if state[idx] != B[idx]]  # Find mismatched indices
    # iterate through this list and perform any swaps that will correctly place both elements
    for i in range(len(c)):
        for j in range (i+1,len(c)):
            if A[c[i]]==B[c[j]] and A[c[j]]==B[c[i]]:
                sequence.append((c[i],c[j]))
                state[c[i]],state[c[j]]=state[c[j]],state[c[i]]
    return state, sequence

# depth limited recursive search to find sequences of swaps which will result in the target arrangement
def solve(state, B, sequence, depth=10):
    if depth <= 0:  # Stop recursion if depth limit is reached
        return
    
    newstate = state[:]  # Create a new copy of state
    c = [idx for idx in range(len(state)) if newstate[idx] != B[idx]]  # Find mismatched indices
    
    if not c:  # If there are no mismatched indices
        yield sequence[:], state  # Yield a copy of the sequence
        return

    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            if B[c[j]] == newstate[c[i]]:
                # Create a copy of the current state and sequence
                newstate_copy = newstate[:]
                sequence_copy = sequence[:]
                
                # Swap the elements in the copied state
                newstate_copy[c[i]], newstate_copy[c[j]] = newstate_copy[c[j]], newstate_copy[c[i]]
                
                # Add the swap to the sequence
                sequence_copy.append((c[i], c[j]))
                
                # Recurse with a decremented depth
                yield from solve(newstate_copy, B, sequence_copy, depth - 1)

if __name__ == "__main__":
    main()
