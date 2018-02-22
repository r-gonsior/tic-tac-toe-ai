import copy
import random
import math
import time
import warnings


def empty_board(n):
    if n < 1:
        raise Exception("Incorrect board size.")
    return [['.' for i in range(j)] for j in range(n, 0, -1)]


def board_print(board):
    for row in board:
        for field in row:
            print(field, end=' ')
        print()


def random_move(board, k, ox):
    return random.choice(empty_fields(board))


def human_move(board, k, ox):
    """Allows a human player to choose moves."""
    n = len(board)
    while True:
        print("Actual board:")
        board_print(board)
        print(ox + " to move.")
        try:
            row = int(input("Type row number from 0 to " + str(n - 1) + ": "))
        except ValueError:
            print('Invalid field, try again.')
            continue
        if row < 0 or row >= n:
            print("Incorrect row number. Try again. ")
            continue
        try:
            column = int(input("Type column number from 0 to "
                               + str(n - row - 1) + ": "))
        except ValueError:
            print('Invalid field, try again.')
            continue
        if column < 0 or column > n - row:
            print("Incorrect column number. Try again.")
            continue

        if board[row][column] != '.':
            print("Chosen field is already taken. Try again.")
            continue

        return row, column


def make_move(board, field, ox):
    """Changes board by putting ox on the field."""
    board[field[0]][field[1]] = ox


def get_opponent(ox):
    return 'x' if ox == 'o' else 'o'


def allies_number(board, ox, x, y, vx, vy):
    """Returns a number of ox symbols that are continuously located in
    direction (vx, vy) from field (x, y) (not included). Vectors (vx, vy) are
    supposed to be of the form (1/0/-1, 1/0/-1), eg (1, 0) or (1, -1). """
    n = len(board)
    result = 0
    while True:
        x += vx
        y += vy
        if x < 0 or y < 0 or x + y >= n:
            return result
        if board[x][y] == ox:
            result += 1
        else:
            return result


def winner(board, k):
    """Checks if the game is over i.e. one of players has k symbols in one
    line. Returns winner symbol e.g. 'x' or '.' in case of draw. If the game
    is not over, returns None. This function fails if both players has k
    symbols in one line (then it will return one of them), but this should
    not happen in the game. """

    is_any_field_free = False  # necessary to choose to return '.' or None
    for (x, row) in enumerate(board):
        for (y, ox) in enumerate(row):
            if ox == '.':
                is_any_field_free = True
            elif (ox == 'o' or ox == 'x') \
                    and ((allies_number(board, ox, x, y, 0, -1) + 1 >= k)
                         or (allies_number(board, ox, x, y, 1, 0) + 1 >= k)
                         or (allies_number(board, ox, x, y, -1, -1) + 1 >= k)
                         or (allies_number(board, ox, x, y, 1, -1) + 1 >= k)):
                # It's enough to check down, right, downright, downleft
                # because we start from top left.
                return ox
    return None if is_any_field_free else '.'


def is_draw(board, k):
    """Returns True when game is already drawn (even if players can still
    play moves) or False otherwise """
    for ox in 'o', 'x':
        board_cpy = copy.deepcopy(board)
        for row in board_cpy:
            for i, content in enumerate(row):
                if content == '.':
                    row[i] = ox
        if winner(board_cpy, k) != '.':
            return False
    return True


def begin(choose_move_o, choose_move_x, n, k):
    """Plays a game on the board of length n, where k symbols in line are
    needed for victory. Returns tuple: (final board state, winner symbol or
    '.' in case of draw, history as a list of tuples (symbol, move)). """
    board = empty_board(n)
    history = []
    while True:
        for ox in 'ox':
            move = choose_move_o(board, k, 'o') if ox == 'o' \
                else choose_move_x(board, k, 'x')
            make_move(board, move, ox)
            history.append((ox, move))
            result = winner(board, k)
            if result is not None:
                return board, result, history
            if is_draw(board, k):
                # Some positions can be a draw even if there
                # are still empty fields
                return board, '.', history


def history_print(history, n):
    """Perform and print sequence of moves """
    board = empty_board(n)
    for (ox, move) in history:
        make_move(board, move, ox)
        board_print(board)
        print('--' * n)


def fields_with_symbol(board, s):
    """Returns a list of fields (tuples of coordinates) containing symbol s."""
    result = []
    for i, row in enumerate(board):
        for j, symbol in enumerate(row):
            if symbol == s:
                result.append((i, j))
    return result


def empty_fields(board):
    """Returns a list of empty fields i.e. containing '.'."""
    return fields_with_symbol(board, '.')


def minimax(board, k, ox, depth, is_maximazing):
    """Evaluate board value in case of ox's move now. Applies minimax
    algorithm checking moves up to depth. Parameter is_maximizing tells if
    moves' values should be maxi- or minimized. """
    warnings.warn("shouldn't use this anymore. Use negamax - it works better.",
                  DeprecationWarning)
    result = winner(board, k)
    if result == '.':
        return 0
    opponent = 'o' if ox == 'x' else 'x'
    if result == opponent:
        return -math.inf if is_maximazing else math.inf
    # The case in which ox has won now is
    # impossible, because the last move was performed by opponent. That's why
    #  we don't check result == kk.

    # If we are now in a leaf of the game tree there is still no winner.
    if depth == 0:
        return 0

    if is_maximazing:
        # Looking for move with the greatest value.
        best_value = -math.inf
        for move in empty_fields(board):
            make_move(board, move, ox)
            move_value = minimax(board, k, opponent, depth - 1,
                                 not is_maximazing)
            make_move(board, move, '.')  # undo move
            if move_value == math.inf:
                return move_value
            if move_value > best_value:
                best_value = move_value
        return best_value
    else:
        # Looking for move with the smallest value.
        best_value = math.inf
        for move in empty_fields(board):
            make_move(board, move, ox)
            move_value = minimax(board, k, opponent, depth - 1,
                                 not is_maximazing)
            make_move(board, move, '.')  # undo move
            if move_value == -math.inf:
                return move_value
            if move_value < best_value:
                best_value = move_value
        return best_value


def minimax_move(board, k, ox, depth=4):
    """Finds the move applying minimax algorithm  for ox symbol. Parameter
    depth is a depth of search in minimax. """
    warnings.warn("shouldn't use this anymore. Use negamax_move - it works "
                  "better.", DeprecationWarning)
    moves = empty_fields(board)
    random.shuffle(moves)
    best_move = moves[0]
    best_value = -math.inf
    opponent = 'o' if ox == 'x' else 'x'
    # Searching for the best move.
    for move in moves:
        make_move(board, move, ox)
        move_value = minimax(board, k, opponent, depth - 1, False)
        make_move(board, move, '.')  # undo move
        if move_value == math.inf:
            return move
        if move_value > best_value:
            best_move = move
            best_value = move_value
    return best_move


def minimax_upg_1(board, k, ox, depth, is_maximazing):
    """Evaluate board value in case of ox's move now. Applies minimax
    algorithm checking moves up to depth. Parameter is_maximizing tells if
    moves' values should be maxi- or minimized. """
    warnings.warn("shouldn't use this anymore. Use negamax - it works better.",
                  DeprecationWarning)
    result = winner(board, k)
    if result == '.':
        return 0
    opponent = 'o' if ox == 'x' else 'x'
    if result == opponent:
        return -100 - depth if is_maximazing else 100 + depth
    # The case in which ox has won now is
    # impossible, because the last move was performed by opponent. That's why
    #  we don't check result == kk.

    # If we are now in a leaf of the game tree there is still no winner.
    if depth == 0:
        return 0

    if is_maximazing:
        # Looking for move with the greatest value.
        best_value = -100
        for move in empty_fields(board):
            make_move(board, move, ox)
            move_value = minimax(board, k, opponent, depth - 1,
                                 not is_maximazing) + depth
            # Substract depth because faster win is better that slower.
            make_move(board, move, '.')  # undo move
            if move_value > best_value:
                best_value = move_value
        return best_value
    else:
        # Looking for move with the smallest value.
        best_value = 100
        for move in empty_fields(board):
            make_move(board, move, ox)
            move_value = minimax(board, k, opponent, depth - 1,
                                 not is_maximazing) - depth
            make_move(board, move, '.')  # undo move
            if move_value < best_value:
                best_value = move_value
        return best_value


def minimax_move_upg_1(board, k, ox, depth=4):
    """Finds the move applying minimax algorithm  for ox symbol. Parameter
    depth is a depth of search in minimax. """
    warnings.warn("shouldn't use this anymore. Use negamax_move - it works "
                  "better.", DeprecationWarning)
    moves = empty_fields(board)
    random.shuffle(moves)
    best_move = moves[0]
    best_value = -100
    opponent = 'o' if ox == 'x' else 'x'
    # Searching for the best move.
    for move in moves:
        make_move(board, move, ox)
        move_value = minimax_upg_1(board, k, opponent, depth - 1, False)
        make_move(board, move, '.')  # undo move
        if move_value == 100 + depth:
            return move
        if move_value > best_value:
            best_move = move
            best_value = move_value
    return best_move


def heuristics(board, k, ox):
    """Returns heuristic value of the board from ox's viewpoint. It is
    computed as follows. For each row, column, diagonal count in how many
    ways a player can still score k symbols in a line. For each successful way
    add how many symbols already have. Then subtract from this opponent's
    result. Example:
    >>> b = [['x', '.', '.'], ['.', 'o'], ['.']]
    >>> heuristics(b, 3, 'x')  # 1 'x' horizontal + 1 'x' vertical - 1 'o' diagonal
    1
    >>> b = [['x', 'x', '.'], ['.', '.'], ['.']]
    >>> heuristics(b, 3, 'x')  # 2 horizontal + 1 vertical
    3
    """
    n = len(board)  # board size
    result = 0
    for (i, row) in enumerate(board):
        for (j, content) in enumerate(row):
            # Scanning board in four directions:
            for (x, y) in (0, 1), (-1, 0), (-1, 1), (-1, -1):
                who = None if content == '.' else content
                partial_result = 0
                i_last, j_last = i + (k - 1) * x, j + (k - 1) * y
                if i_last + j_last >= n or i_last < 0 or j_last < 0:
                    # Continue when it is impossible to get k symbols in a line
                    continue
                for m in range(k):
                    i_next, j_next = i + m * x, j + m * y
                    next_content = board[i_next][j_next]
                    # next_content is a content of the field which
                    # may form a line together with (i, j) field
                    if next_content != '.':
                        if who == next_content:
                            partial_result += 1
                        elif who is None:
                            who = next_content
                            partial_result += 1
                        else:
                            # Opponent interrupts our line and thus we zero
                            # the result. It is impossible to score k symbols
                            # in a line now, so break
                            partial_result = 0
                            break
                if partial_result == k:  # End of game
                    return math.inf if content == ox else -math.inf
                if who == ox:
                    result += partial_result
                elif who == get_opponent(ox):
                    result -= partial_result
    return result


def field_values(n, k):
    """Prints heuristic values of each field on the board of size n,
    when k symbols in a line win the game """
    board = empty_board(n)
    result = empty_board(n)
    for i in range(n):
        for j in range(0, n - i):
            make_move(board, (i, j), 'o')
            result[i][j] = heuristics(board, k, 'o')
            make_move(board, (i, j), '.')  # undo move
    board_print(result)


class TimeOut(Exception):
    pass


def negamax(board, k, ox, depth, alpha, beta, start_time, time_limit):
    if time.time() - start_time > time_limit:
        raise TimeOut
    if depth == 0 or winner(board, k) is not None:
        return heuristics(board, k, ox)
    opponent = 'o' if ox == 'x' else 'x'
    best_val = -math.inf
    for move in empty_fields(board):
        make_move(board, move, ox)
        move_val = -negamax(board, k, opponent, depth - 1, -beta, -alpha,
                            start_time, time_limit)
        make_move(board, move, '.')  # undo move
        if move_val > best_val:
            best_val = move_val
        if best_val > alpha:
            alpha = best_val
        if alpha > beta:
            return alpha
    return best_val


def negamax_move(board, k, ox, time_limit=10):
    """Negamax move choosing with alpha-beta pruning performing iterative
    deepening in given time limit. """
    start_time = time.time()
    board_cpy = copy.deepcopy(board)
    # We need a copy of the board, because exception TimeOut can sometimes be
    # raised before we undo move.
    opponent = get_opponent(ox)
    # Prepare list containing pairs: moves and their values. Initially moves
    # have no values
    moves_vals = list(map(lambda move: [move, None], empty_fields(board_cpy)))
    random.shuffle(moves_vals)
    # Iterative deepening:
    for depth in range(1, 1 + len(empty_fields(board_cpy))):
        best_move = moves_vals[0][0]  # because the list is sorted by values
        try:
            local_best_val = -math.inf
            for move_and_val in moves_vals:
                make_move(board_cpy, move_and_val[0], ox)
                local_val = \
                    -negamax(board_cpy, k, opponent, depth - 1, -math.inf,
                             -local_best_val, start_time, time_limit)
                make_move(board_cpy, move_and_val[0], '.')  # undo move
                # check if it is a winning move and return it if this case:
                if local_val == math.inf:
                    return move_and_val[0]
                # update move value for use in next iteration:
                move_and_val[1] = local_val
                if local_val > local_best_val:
                    local_best_val = local_val
            # sort by move value from the most powerful to the weakest:
            moves_vals.sort(key=lambda x: x[1], reverse=True)
            if moves_vals[0][1] == -math.inf:
                # even best move is losing. It makes no sense to analyze deeper
                return moves_vals[0][0]
            else:
                # drop losing moves. Sometimes moves that are obviously
                # losing moves aren't dropped, because of alpha beta
                # algorithm, which prunnes them before it realizes that they
                # are immediately losing
                moves_vals = [mv for mv in moves_vals if mv[1] > -math.inf]
                # print('number of considered moves: ' + str(len(moves_vals)))
                if len(moves_vals) == 1:  # the only move
                    return moves_vals[0][0]
        except TimeOut:
            # print('depth: %i' % (depth - 1))  # see how deep AI analyzed
            return best_move
    return moves_vals[0][0]  # return best move, when analyzed whole game.
    # This can happen if the algorithm solves the game before time elapses


################################################################################
def main():

    # human vs computer
    n = 7
    k = 4

    # # AI with more time to think (by default 10 seconds):
    # def negamax_move20(board, k, ox):
    #     return negamax_move(board, k, ox, 20)
    # board, result, history = begin(negamax_move20, human_move, n, k)

    print('AI vs human, board size = %i, number of symbols to win = %i. AI '
          'time limit = 10 s.' % (n, k))
    board, result, history = begin(negamax_move, human_move, n, k)
    board_print(board)
    # history_print(history, n)
    print('Result: ' + result)


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(heuristics, globals())

    main()
