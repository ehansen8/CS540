import random


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.max_depth = 4
        self.score_table = self.score_hash()

    def score_hash(self):
        score_dict = {}
        perms = [[' '], ['b'], ['r']]
        perms = self.recursive_line_permutation(perms, 1)

        def count_score(color, cc):
            w = [0, 1, 4, 9, 16, 25]
            if color == ' ':
                sign = 0
            elif color == self.my_piece:
                sign = 1
            else:
                sign = -1

            return sign * w[cc]

        for row in perms:
            score = 0
            prev_cell = ' '
            cc = 0
            for cell in row:
                # if blank, score and move on
                if cell == ' ':
                    if cc != 0:
                        score += count_score(prev_cell, cc)
                    cc = 0

                # if different cell, score and set cc to 1
                elif cell != prev_cell:
                    if cc != 0:
                        score += count_score(prev_cell, cc)
                    cc = 1
                # if same cell, increment cc by 1
                else:
                    cc += 1
                # Change previous cell each iteration
                prev_cell = cell

            # score out of loop to capture anything not yet scored
            score += count_score(prev_cell, cc)
            row_str = ''.join(row)
            score_dict[row_str] = score

        return score_dict

    def recursive_line_permutation(self, perm_list, depth):
        if depth == 5:
            return perm_list
        new_perm_list = []
        vals = [' ', 'b', 'r']
        for perm in perm_list:
            for i in range(3):
                mod_perm = perm[:]
                mod_perm.append(vals[i])
                new_perm_list.append(mod_perm)

        return self.recursive_line_permutation(new_perm_list, depth + 1)

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        move = []

        # [0] contains the new state, [1] contains destination coordinates (r,c), [2] contains source coordinates
        # or 0 if it was on a drop phase
        move_choices = self.generate_succ(state, self.my_piece, self.is_drop_phase(state))
        alpha = float('-inf')
        beta = float('inf')
        max_state = ''
        for m in move_choices:
            alpha_temp = self.min_value(m[0], 1, alpha, beta)
            if alpha_temp > alpha:
                alpha = alpha_temp
                max_state = m

        # ensure the destination (row,col) tuple is at the beginning of the move list
        print(self.heuristic_game_value(m[0]))
        move.append(max_state[1])

        if max_state[2] != 0:
            move.append(max_state[2])
        return move

    # Checks if current state is in drop phase or not
    @staticmethod
    def is_drop_phase(state):
        pieces = 0
        for i in state:
            for j in i:
                if j != ' ':
                    pieces += 1
        if pieces == 8:
            return False
        return True

    def max_value(self, state, depth, alpha, beta):
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal

        # only happens on max depth
        if depth == self.max_depth:
            return self.heuristic_game_value(state)

        for s in self.generate_succ(state, self.my_piece, self.is_drop_phase(state)):
            alpha = max(alpha, self.min_value(s[0], depth + 1, alpha, beta))
            if alpha >= beta:
                return beta
        return alpha

    def min_value(self, state, depth, alpha, beta):
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal

        # only happens on max depth
        if depth == self.max_depth:
            return self.heuristic_game_value(state)

        for s in self.generate_succ(state, self.opp, self.is_drop_phase(state)):
            beta = min(beta, self.max_value(s[0], depth + 1, alpha, beta))
            if alpha >= beta:
                return alpha
        return beta

    # Generates list of possible successors
    @staticmethod
    def generate_succ(state, color, drop_phase):
        succ_list = []

        # Can drop anywhere
        if drop_phase:
            for i, row in enumerate(state):
                for j, cell in enumerate(row):
                    if cell == ' ':
                        new_state = [r[:] for r in state]
                        new_state[i][j] = color
                        succ_list.append((new_state, (i, j), 0))

        # else, loop through all pieces, and generate all adjacent moves for each
        else:
            for i, row in enumerate(state):
                for j, cell in enumerate(row):
                    if cell == color:

                        for x in range(i - 1, i + 2):
                            for y in range(j - 1, j + 2):
                                if not TeekoPlayer.within_board(x, y): continue
                                if (x, y) != (i, j) and state[x][y] == ' ':
                                    new_state = [r[:] for r in state]
                                    # Remove marker to move
                                    new_state[i][j] = ' '
                                    new_state[x][y] = color
                                    succ_list.append((new_state, (x, y), (i, j)))
        return succ_list

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        # starting values
        r = [3, 4, 4]
        c = [0, 0, 1]
        for i in range(3):
            for e in range(2):
                x = r[i] - e
                y = c[i] + e
                # occurs when diagonal is not main diagonal
                if e == 1 and x + y != 4: continue
                if state[x][y] != ' ' and state[x][y] == state[x - 1][y + 1] == state[x - 2][y + 2] == state[x - 3][
                    y + 3]:
                    return 1 if state[x][y] == self.my_piece else -1

        # check / diagonal wins
        # starting values
        r = [1, 0, 0]
        c = [0, 0, 1]
        for i in range(3):
            for e in range(2):
                x = r[i] + e
                y = c[i] + e
                # occurs when diagonal is not main diagonal
                if e == 1 and x - y != 0: continue
                if state[x][y] != ' ' and state[x][y] == state[x + 1][y + 1] == state[x + 2][y + 2] == \
                        state[x + 3][y + 3]:
                    return 1 if state[x][y] == self.my_piece else -1

        # check 2x2 box wins
        # specify box corner then search
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j + 1] == state[i + 1][j + 1] == state[i + 1][j]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet

    # Checks if position is within board bounds
    @staticmethod
    def within_board(r, c):
        if 0 <= r < 5 and 0 <= c < 5:
            return True
        return False

    # Count consecutive tiles along each vertical, horizontal, diagonal, and box
    # more consecutive markers get scored by higher weights given in w weight vector
    # AI score is positive, opponent is negative
    def heuristic_game_value(self, state):
        score = 0
        normalizer = 100

        terminal = self.game_value(state)
        if terminal != 0:
            return terminal

        def count_score(color, cc):
            w = [0, 1, 4, 9]
            if color == ' ':
                sign = 0
            elif color == self.my_piece:
                sign = 1
            else:
                sign = -1

            return sign * w[cc]

        # Horizontal Count
        for row in state:
            key = ''.join(row)
            score += self.score_table[key]

        # Vertical Count
        for col in range(len(state)):
            row = []
            for i in range(len(state)):
                row.append(state[i][col])

            key = ''.join(row)
            score += self.score_table[key]

        # \ Diagonal Count
        r = [3, 4, 4]
        c = [0, 0, 1]
        for i in range(3):
            row = []
            for e in range(5):
                x = r[i] - e
                y = c[i] + e

                # Will only happen at end of off-main diagonals
                if not self.within_board(x, y):
                    row.append(' ')
                    continue
                cell = state[x][y]
                row.append(cell)

            key = ''.join(row)
            score += self.score_table[key]

        # / Diagonal Count
        r = [1, 0, 0]
        c = [0, 0, 1]
        for i in range(3):
            row = []
            for e in range(5):
                x = r[i] + e
                y = c[i] + e

                # Will only happen at end of off-main diagonals
                if not self.within_board(x, y):
                    row.append(' ')
                    continue
                cell = state[x][y]
                row.append(cell)

            key = ''.join(row)
            score += self.score_table[key]

        # Box Count
        for i in range(4):
            for j in range(4):
                s = state[i][j] + state[i][j + 1] + state[i + 1][j + 1] + state[i + 1][j]

                # Counts my score and then opponents score
                score += count_score(self.my_piece, s.count(self.my_piece))
                score += count_score(self.opp, s.count(self.opp))

        return score / normalizer


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

# Random selection for random opponent
def randomPlayer(state, drop_phase, color):
    if drop_phase:
        (row, col) = (random.randint(0, 4), random.randint(0, 4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0, 4), random.randint(0, 4))
        let = 'ABCDE'
        return (let[col] + str(row), 0)

    else:
        (row, col) = (random.randint(0, 4), random.randint(0, 4))
        while not state[row][col] == color:
            (row, col) = (random.randint(0, 4), random.randint(0, 4))

        # Gets Random Adjacent Cell to move to
        move_list = []
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if not TeekoPlayer.within_board(x, y): continue
                if (x, y) != (row, col) and state[x][y] == ' ':
                    move_list.append((x, y))

        move_to_row = random.choice(move_list)[0]
        move_to_col = random.choice(move_list)[1]

        let = 'ABCDE'
        return (let[col] + str(row), let[move_to_col] + str(move_to_row))


ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            #player_move = randomPlayer(ai.board, True, ai.opp)[0]
            player_move = input('Move e.g. B3')
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
        print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            #player_move = randomPlayer(ai.board, False, ai.opp)
            print(player_move)
            #move_from = player_move[0]
            move_from = input('Move From e.g. B3')
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            #move_to = player_move[1]
            move_to = input('Move To e.g. B4')
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                  (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
