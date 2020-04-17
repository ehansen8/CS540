''' Evan Hansen
    CS 540
    P3 N-Queens with a Boulder
'''

import random


def succ(state, boulderX, boulderY):
    n = len(state)
    succ_list = []

    # Move each queen everywhere not occupied
    for x in range(n):
        qy = state[x]
        # move to new row
        for y in range(n):
            # if same as current queen - skip
            if y == qy: continue
            # if same as boulder - skip
            if x == boulderX and y == boulderY: continue
            new_s = state[:]
            new_s[x] = y
            succ_list.append(new_s)
            # print(new_s, 'f=', f(new_s,boulderX,boulderY))

    return succ_list


# determines state score: # of queens in conflict
def f(state, boulderX, boulderY):
    n = len(state)
    conflicts = 0

    # list of already interfering queen indices
    # check ones that are counted, but don't increment counter
    # if already counted queen is hit
    already_counted = [0] * n
    # Check each queen
    for qx in range(n):
        qy = state[qx]
        # Check along row for intercepts
        for x in range(qx + 1, n):
            # when boulder is found, goto next queen
            if qy == boulderY and x == boulderX:
                # boulder is found
                break

            # if same y as next and no boulder: conflict
            if qy == state[x]:
                conflicts += inc_conflicts(qx, x, already_counted)
                already_counted[qx] = 1
                already_counted[x] = 1
                # goto upper diagonal
                break

        # Check upper diagonal: move up and over by x each time
        for x in range(1, n):
            tx = qx + x
            ty = qy + x
            # end if tx or ty are >= n
            if tx >= n or ty >= n: break
            # boulder check
            if tx == boulderX and ty == boulderY:
                # goto lower diagonal
                break
            # if targetY matches y of queen in column: conflict
            if ty == state[tx]:
                conflicts += inc_conflicts(qx, tx, already_counted)
                already_counted[qx] = 1
                already_counted[tx] = 1
                # goto lower diagonal
                break

        # Check lower diagonal: down and over by x each increment
        for x in range(1, n):
            tx = qx + x
            ty = qy - x
            # end if tx >= n or ty < 0
            if tx >= n or ty < 0: break
            # boulder check
            if tx == boulderX and ty == boulderY:
                # goto next queen
                break
            # if targetY matches y of queen in column: conflict
            if ty == state[tx]:
                conflicts += inc_conflicts(qx, tx, already_counted)
                already_counted[qx] = 1
                already_counted[tx] = 1
                # goto lower diagonal
                break

    return conflicts


def inc_conflicts(qx, tx, already_counted):
    conflicts = 2
    return conflicts - already_counted[qx] - already_counted[tx]


def choose_next(curr, boulderX, boulderY):
    succ_list = succ(curr, boulderX, boulderY)
    succ_list.append(curr)

    # First sort by ascending order
    succ_list.sort()
    # Then sort by lowest f()
    succ_list.sort(key=lambda x: f(x, boulderX, boulderY))

    lowest_succ = succ_list[0]
    if lowest_succ == curr:
        return None

    return lowest_succ


def nqueens(initial_state, boulderX, boulderY):
    curr = initial_state
    print_state(curr, boulderX, boulderY)
    while True:
        next = choose_next(curr, boulderX, boulderY)
        if next is None:
            return curr

        curr = next
        print_state(curr, boulderX, boulderY)


def print_state(s, bX, bY):
    f_val = f(s, bX, bY)
    print(s, '- f=' + str(f_val))


def nqueens_restart(n, k, boulderX, boulderY):
    attempt_list = []
    for attempt in range(k):
        state = random_setup(n, boulderX, boulderY)

        sol = nqueens(state, boulderX, boulderY)
        # if goal state achieved: print goal state
        if f(sol, boulderX, boulderY) == 0:
            print_state(sol, boulderX, boulderY)
            return
        # if goal not achieved, add state to list of attempts
        attempt_list.append(sol)

    # No goal achieved, so print out best solutions in sorted order

    # First sort by ascending order
    attempt_list.sort()
    # Then sort by lowest f()
    attempt_list.sort(key=lambda x: f(x, boulderX, boulderY))

    for a in attempt_list:
        print_state(a, boulderX, boulderY)


def random_setup(n, bX, bY):
    invalid_setup = True
    # if loops completes without hitting a boulder, return state
    while invalid_setup:
        invalid_setup = False
        state = []
        for qx in range(n):
            qy = random.randint(0, n - 1)
            # if queen lands on boulder, restart while loop
            if qx == bX and qy == bY:
                invalid_setup = True
                break

            state.append(qy)

    return state

nqueens_restart(12,5,4,4)