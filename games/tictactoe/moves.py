# How to capture the state of the tic-tac-toe board?

# In the from http://incompleteideas.net/book/code/ttt.lisp the states
# are captured as a 18-bit vector with lower 9-bits are used for moves of player 'x'
# and the upper 9-bits are for moves of player 'o'

# Magic squares indices
#   2 9 4
#   7 5 3
#   6 1 8
#
magic_square = [2, 9, 4, 7, 5, 3, 6, 1, 8]
powers_of_2 = [None] + [2**i for i in range(9)]

def state_index(x_moves, o_moves):
    """
    Compute a unique index for the state based on X and O moves.
    X bits in lower 9 bits, O bits in upper 9 bits.
    """
    x_sum = sum(powers_of_2[pos] for pos in x_moves)
    o_sum = sum(powers_of_2[pos] for pos in o_moves)
    return x_sum + 512 * o_sum

def create_board_str(x_moves, o_moves):
    """
    """
    bstr = ""
    for i in magic_square:
        bstr += "x" if i in x_moves else \
                "o" if i in o_moves else \
                "-"
    return bstr

def print_board(bstr):
    #print(" --- --- ---")
    fmtstr = "|"
    count = 0
    for s in bstr:
        fmtstr += "x" if s == "x" else \
                  "o" if s == "o" else \
                  " " if s == "-" else ""
        fmtstr += "|"
        count += 1
        if count % 3 == 0 and count % 9 != 0:
            fmtstr += "\n"
            fmtstr += "|" if count % 9 != 0 else ""
    print(fmtstr)
    #print(" --- --- ---")

def print_board_horz(blist):
    """ Prints board horizontally,
        side by side based on list of 
        board strings
    """
    fmtstr = "|"
    for i,st in enumerate([0,3,6]):
        for j,bstr in enumerate(blist):
            fmtstr += "   |" if j != 0 else ""
            fmtstr +=  "|".join([f"{m}" for m in bstr[st:st+3]]) + "|"
        fmtstr += "\n|" if i != 2 else ""
    print(fmtstr)

def possible_o_moves(x_moves):
    """
    """
    o_moves = []
    for j in range(1,10):
        #if j not in x_moves:
            o_moves.append(j)
    return o_moves
        

if __name__ == "__main__":
    for i in range(1,10):
        blist = []
        stlist = []
        x_moves = [i]
        o_moves = possible_o_moves(x_moves)
        blist.append(create_board_str(x_moves, []))
        stlist.append(state_index(x_moves, []))
        for m in o_moves:
            blist.append(create_board_str(x_moves, [m]))
            stlist.append(state_index(x_moves, [m]))
        print_board_horz(blist)
        print("".join([f"{i:<10}" for i in stlist]))
        print()
