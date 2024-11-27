# Just some test code for optimum swap alogorithms


from collections import defaultdict, deque
    

def swap_sort_transform(A, B):
   
    swaps = []  # Store pairs of swaps for reference

    for left_idx in range(len(A)):

        # skip if already in the correct position
        if A[left_idx] == B[left_idx]:
            continue

        for right_idx in range(left_idx+1,len(A)):
            
            # Swap the current element with the element at its target position
            if B[left_idx] == A[right_idx]:
                A[left_idx], A[right_idx] = A[right_idx], A[left_idx]
                state = A[:]
                swaps.append((left_idx, right_idx))
                break
    
    return A, swaps


def cycle_sort_transform(A, B):
    # Map elements in A to their positions in B
    target_positions = {value: idx for idx, value in enumerate(B)}
    
    # Mark visited positions to avoid processing them multiple times
    visited = [False] * len(A)
    
    swaps = []  # Store pairs of swaps for reference

    for start in range(len(A)):
        # Skip if already visited or already in the correct position
        if visited[start] or A[start] == B[start]:
            continue

        # Start a cycle
        current = start
        print ("cycle: swap ", end = "")
        while not visited[current]:

            visited[current] = True
            target_content_A_current = B[A.index(A[current])]
            #print(f'target content for position {current} is {target_content_A_current}')
            next_pos = A.index(target_content_A_current)
            #print(f'{target_content_A_current} is found at posistion {next_pos}')
            
            # Swap the current element with the element at its target position
            if current != next_pos:
                swaps.append((current, next_pos))
                print (f'({current}, {next_pos}), ', end = "")
                A[current], A[next_pos] = A[next_pos], A[current]
                #print (f" state: {A}", end = "")
            
            # Move to the next position in the cycle
            current = next_pos
        print()
    
    return A, swaps


def cycle_sort_with_duplicates(A, B):

    # Map each value in B to its positions
    target_positions = defaultdict(deque)
    for idx, value in enumerate(B):
        target_positions[value].append(idx)
    print(target_positions)
    
    # Visited positions in A
    visited = [False] * len(A)
    swaps = []  # To record the swaps performed

    for start in range(len(A)):
        # Skip if already visited or in the correct position
        if visited[start] or A[start] == B[start]:
            continue

        # Start a cycle
        current = start
        while not visited[current]:

            print ("cycle: ", end = "")
            visited[current] = True

            target_content_A_current = target_positions[A.index(A[current])]
            print(f'target content for position {current} is {target_content_A_current}')
            target_pos = A.index(target_content_A_current)
            print(f'{target_content_A_current} is first found at posistion {target_pos}')
            # Find the target position for the current value of A
            #target_pos = target_positions[A[current]].popleft()  # Get the first available target position
            
            # Swap elements if necessary
            if current != target_pos:
                swaps.append((current, target_pos))
                print(f'{current}, {target_pos}', end = "")
                A[current], A[target_pos] = A[target_pos], A[current]
            
            # Move to the next position in the cycle
            current = target_pos
            print()
    
    return A, swaps


A = [
        "R",
        "U",
        "E",
        "D",
        "W",
        "E",
        "A",
        "M",
        "O",
        "A",
        "T",
        "A",
        "T",
        "N",
        "Y",
        "A",
        "R",
        "U",
        "O",
        "A",
        "N",
    ]

B = [
        "R",
        "E",
        "N",
        "E",
        "W",
        "A",
        "U",
        "O",
        "D",
        "A",
        "T",
        "U",
        "M",
        "A",
        "T",
        "A",
        "R",
        "A",
        "Y",
        "O",
        "N",
    ]

transformed_list, swap_steps = swap_sort_transform(A[:], B[:])

print("                Start list:", A)
print("               Target list:", B)
print("Swap Sort Transformed List:", transformed_list)
print("Swaps Performed:", len(swap_steps), swap_steps)
print("Success:",transformed_list == B)
print()


transformed_list, swap_steps = cycle_sort_transform(A[:], B[:])

print("                 Start list:", A)
print("                Target list:", B)
print("Cycle Sort Transformed List:", transformed_list)
print("Swaps Performed:", len(swap_steps), swap_steps)
print("Success:",transformed_list == B)
print()


'''
A = [9, 4, 8, 10, 11, 5, 7, 3, 1, 2, 6]
B = [8, 9, 10, 4, 2, 7, 5, 11, 6, 1, 3]

transformed_list, swap_steps = cycle_sort_with_duplicates(A, B)

print("                                Target list:", B)
print("Cycle Sort wuth duplicates Transformed List:", transformed_list)
print("Swaps Performed:", swap_steps)
print("Success:",transformed_list == B)

'''