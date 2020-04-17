'''
Evan Hansen
CS 540
P4: Math and AI
'''

import random


def pick_envelope(switch, verbose):
    envelopes = [['b', 'b'], ['b', 'b']]

    red_e = random.randint(0, 1)
    red_b = random.randint(0, 1)

    envelopes[red_e][red_b] = 'r'

    pick_e = random.randint(0, 1)
    pick_b = random.randint(0, 1)

    draw = envelopes[pick_e][pick_b]

    if verbose:
        print('Envelope 0:', envelopes[0])
        print('Envelope 1:', envelopes[1])
        print('I picked envelope', pick_e)
        print('and drew a', draw)
        if switch and draw != 'r':
            print('Switch to envelope', 0 if pick_e == 1 else 1)

    if switch and draw != 'r':
        pick_e = 0 if pick_e == 1 else 1

    if pick_e == red_e:
        return True

    return False


def run_simulation(n):
    switch_correct = 0
    no_switch_correct = 0

    for i in range(n):
        if pick_envelope(True, verbose=False):
            switch_correct += 1

        if pick_envelope(False, verbose=False):
            no_switch_correct += 1

    print('After', n, 'simulations:')
    print('\t Switch successful: {:.2%}'.format(switch_correct / n))
    print('\t No-Switch successful: {:.2%}'.format(no_switch_correct / n))
