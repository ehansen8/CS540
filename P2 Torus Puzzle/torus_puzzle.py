''' Evan Hansen
    CS 540
    P2 Torus 8-Puzzle
'''

import numpy as np
import pq


# Prints successors to a given state along with h() values
def print_succ(state):
    # Transforms state as list to matrix
    state = create_state(state)
    succs = generate_succ(state)
    print_list = []
    for s in succs:
        print_list.append(to_list(s))

    print_list = sorted(print_list)
    for s in print_list:
        print(s, 'h=' + str(heuristic(s)))


# Returns a list of possible successor states
def generate_succ(state):
    res = np.where(state == 0)

    # row and column of hole (0)
    coords = [res[0][0], res[1][0]]
    succ_list = []
    r = coords[0]
    c = coords[1]

    row = state[r, :]
    col = state[:, c]

    # Modify Row
    for i in range(3):
        if i == c: continue

        z = np.copy(state)
        z[r, i] = 0
        z[r, c] = row[i]

        succ_list.append(z)

    # Modify Column
    for i in range(3):
        if i == r: continue

        z = np.copy(state)
        z[i, c] = 0
        z[r, c] = col[i]

        succ_list.append(z)
    return succ_list


# Converts numpy array to list
def to_list(state):
    return list(state.reshape(1, 9)[0])


# Heuristic is # of tiles out of place
def heuristic(state):
    # Allows the heuristic to be performed on 2D arrays or lists
    if not isinstance(state, list):
        state = to_list(state)
    max = 8
    correct = 0
    for i, v in enumerate(state):
        if i + 1 == v:
            correct += 1
    h = max - correct
    return h


# Creates a numpy matrix representation of state from a list
def create_state(state_list):
    state = np.array(state_list)
    return state.reshape((3, 3))


# Performs A* search and prints optimal path
def solve(state):
    state = create_state(state)
    node = astar(state)

    move_list = []
    parent = ''
    while parent is not None:
        parent = node['parent']
        string = str(to_list(node['state'])) + ' h=' + str(node['h']) + ' moves: ' + str(node['g'])
        move_list.append(string)
        node = parent

    move_list = move_list[::-1]
    for move in move_list:
        print(move)


# A* algorithm
def astar(state):
    open = pq.PriorityQueue()
    closed = []
    s = create_dict(state, None, 0)
    open.enqueue(s)

    # A* loop
    while True:
        if open.is_empty():
            print("Failed to Find a Path")
            return

        n = open.pop()
        closed.append(n)

        # Goal Found when h=0 is popped from pq
        if n['h'] == 0:
            print('Max Queue Length: ', open.max_len)
            return n

        children = child_dict_list(n)

        for child in children:
            # If neither contain child, add to open
            if contains(closed, child) == 0 and open.__contains__(child) == 0:
                open.enqueue(child)
                continue

            # If either open or closed contains node, but has a higher g(), add node with
            # lower g() back to open
            if open.__contains__(child) == 2:
                open.enqueue(child)
            elif contains(closed, child) == 2:
                print("RQ")
                open.requeue(child)


# 0: doesn't contain, 1: contains but larger g(), 2: contains and smaller g()
def contains(closed, target):
    for c in closed:
        if (c['state'] == target['state']).all():
            if c['g'] > target['g']:
                print("contained it bro")
                closed.remove(c)
                return 2
            return 1

    return 0


# Creates list of children nodes from parent node
def child_dict_list(parent_dict):
    child_state_list = generate_succ(parent_dict['state'])
    dict_list = []

    # Cost from parent to child is 1
    child_g = parent_dict['g'] + 1

    for state in child_state_list:
        dict_list.append(create_dict(state, parent_dict, child_g))

    return dict_list


# Creates a node (dictionary) from a state, parent node, and g value (moves to this state)
def create_dict(state, parent, g):
    h = heuristic(state);
    f = h + g
    d = {'state': state, 'parent': parent, 'h': h, 'g': g, 'f': f}
    return d


# Test for internal state creation
s = [4,3,8,5,1,6,7,2,0]
# print_succ(s)
solve(s)
