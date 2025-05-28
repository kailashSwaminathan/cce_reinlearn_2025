# http://incompleteideas.net/book/code/TTT.lisp
# converted to python using perplexity.ai

import numpy as np 
from itertools import combinations

# Magic square positions for Tic-Tac-Toe
# Labelling the locations of the Tic-Tac-Toe board in this way is useful because 
# then we can just add up any three positions, and if the sum is 15, then we 
# know they are three in a row.  The following function then tells us if a list 
# of X or O positions contains any that are three in a row.

magic_square = [2, 9, 4, 7, 5, 3, 6, 1, 8]

# Powers of 2 for bit indexing (index 0 unused for convenience)
powers_of_2 = [None] + [2**i for i in range(9)]
# Global variables for value table and initial state
value_table = None
initial_state = None

# Learning parameters
alpha = 0.5
epsilon = 0.01

def any_n_sum_to_k(n, k, lst):
    """
    Returns True if any n elements in lst sum to k.
    Recursive implementation similar to the Lisp version.
    """
    if n == 0:
        return k == 0
    if k < 0 or not lst:
        return False
    # Include first element
    if any_n_sum_to_k(n - 1, k - lst[0], lst[1:]):
        return True
    # Exclude first element
    if any_n_sum_to_k(n, k, lst[1:]):
        return True
    return False

def show_state(state):
    """
    Prints the Tic-Tac-Toe board state.
    state: tuple (X_moves, O_moves, index)
    """
    X_moves, O_moves, _ = state
    print()
    for i, location in enumerate(magic_square):
        if location in X_moves:
            print(" X", end='')
        elif location in O_moves:
            print(" O", end='')
        else:
            print(" -", end='')
        # Print value at position 5 (index 5)
        if i == 5:
            print(f"  {value(state):6.3f}", end='')
        # New line every 3 cells
        if (i + 1) % 3 == 0:
            print()

def state_index(X_moves, O_moves):
    """
    Compute a unique index for the state based on X and O moves.
    X bits in lower 9 bits, O bits in upper 9 bits.
    """
    x_sum = sum(powers_of_2[pos] for pos in X_moves)
    o_sum = sum(powers_of_2[pos] for pos in O_moves)
    return x_sum + 512 * o_sum

def init():
    """
    Initializes the value table and initial state.
    """
    global value_table, initial_state
    value_table = [None] * (512 * 512) # 2^9 * 2^9 states
    initial_state = ([], [], 0)
    set_value(initial_state, 0.5)


def value(state):
    """
    Returns the value of the given state.
    """
    #global value_table
    return value_table[state[2]]


def set_value(state, val):
    """
    Sets the value of the given state.
    """
    #global value_table
    value_table[state[2]] = val

def next_state(player, state, move):
    """
    Returns new state after making the indicated move by the indicated player.
    """
    X_moves = state[0].copy()
    O_moves = state[1].copy()

    if player == 'X':
        X_moves.append(move)
    else:
        O_moves.append(move)

    idx = state_index(X_moves, O_moves)
    new_state = (X_moves, O_moves, idx)

    if value(new_state) is None:
        if any_n_sum_to_k(3, 15, X_moves):
            set_value(new_state, 0)  # X wins
        elif any_n_sum_to_k(3, 15, O_moves):
            set_value(new_state, 1)  # O wins
        elif len(X_moves) + len(O_moves) == 9:
            set_value(new_state, 0)  # Draw
        else:
            set_value(new_state, 0.5)  # Non-terminal state

    return new_state

def terminal_state_p(state):
    """
    Returns True if the state is terminal (win/loss/draw).
    """
    return isinstance(value(state), (int, float)) and value(state) in (0, 1)

def possible_moves(state):
    """
    Returns a list of unplayed positions.
    """
    played = set(state[0]) | set(state[1])
    return [pos for pos in range(1, 10) if pos not in played]

def random_move(state):
    """
    Returns a random unplayed location.
    """
    moves = possible_moves(state)
    return np.random.choice(moves) if moves else None

def greedy_move(player, state):
    """
    Returns the move that yields the highest valued next state.
    """
    moves = possible_moves(state)
    print(f"Possible moves for {player}: {moves}")
    if not moves:
        return None

    best_value = -1
    best_move = None
    for move in moves:
        next_st = next_state(player, state, move)
        v = value(next_st)
        if v is not None and v > best_value:
            best_value = v
            best_move = move
    return best_move

def update(state, new_state, quiet=False):
    """
    Learning rule: update the value of the old state based on new state's value.
    """
    old_val = value(state)
    new_val = value(new_state)
    if old_val is None or new_val is None:
        return
    updated_val = old_val + alpha * (new_val - old_val)
    set_value(state, updated_val)
    if not quiet:
        print(f"                    {updated_val:.3f}")

def game(quiet=False):
    """
    Plays one game against the random player.
    X moves first and is random.
    O learns and tries to maximize value.
    """
    state = initial_state
    if not quiet:
        show_state(state)

    while True:
        # X's move (random)
        move_x = random_move(state)
        new_state = next_state('X', state, move_x)

        exploratory_move = np.random.random() < epsilon

        if terminal_state_p(new_state):
            if not quiet:
                show_state(new_state)
            update(state, new_state, quiet)
            return value(new_state)

        # O's move (greedy or exploratory)
        if exploratory_move:
            move_o = random_move(new_state)
        else:
            move_o = greedy_move('O', new_state)

        new_state_2 = next_state('O', new_state, move_o)

        if not exploratory_move:
            update(state, new_state_2, quiet)

        if not quiet:
            show_state(new_state_2)

        if terminal_state_p(new_state_2):
            return value(new_state_2)

        state = new_state_2

def run():
    """
    Run 40 games and print average results over 100 games each.
    """
    for _ in range(40):
        total = 0
        for _ in range(100):
            init()
            total += game(quiet=False)
        print(total / 100.0)

def runs(num_runs, num_bins, bin_size):
    """
    Run multiple runs and print average results per bin.
    """
    results = [0.0] * num_bins
    for _ in range(num_runs):
        init()
        for i in range(num_bins):
            s = 0.0
            for _ in range(bin_size):
                s += game(quiet=True)
            results[i] += s
    for i in range(num_bins):
        avg = results[i] / (bin_size * num_runs)
        print(avg)

# Initialize before playing
init()

# Example: play one game with output
if __name__ == "__main__":
    game(quiet=False)
