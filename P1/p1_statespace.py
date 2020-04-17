# Evan Hansen
# CS 540
# P1


def fill(state, max, which):
    update = state[:]
    update[which] = max[which]
    return update


def empty(state, max, which):
    update = state[:]
    update[which] = 0
    return update


def xfer(state, max, source, dest):
    update = state[:]

    canTake = max[dest] - state[dest]
    canGive = state[source]

    transfer = min(canTake, canGive)

    update[dest] += transfer
    update[source] -= transfer
    return update


def succ(state, max):
    # Uses a set to avoid duplicate states
    sList = set()
    for i in [0, 1]:
        sList.add(tuple(fill(state, max, i)))
        sList.add(tuple(empty(state, max, i)))

    sList.add(tuple(xfer(state, max, 0, 1)))
    sList.add(tuple(xfer(state, max, 1, 0)))
    for e in sList:
        print(list(e))
