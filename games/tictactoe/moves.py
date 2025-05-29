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

def gen_moves(nat):
    """
    """
    moves = [([],[])]
    for nm in range(1,nat+1):
        new_moves = []
        for xm, om in moves:
            bstr = create_board_str(xm, om)
            r,ws = is_linked(bstr)
            if r:
                #print(f"Finished {xm}  {om}")
                continue
            for i in range(1,10):
                if i in xm or i in om:
                    continue
                newx = xm + [i]
                if nm >= 3:
                    bstr = create_board_str(newx, om)
                    r,ws = is_linked(bstr)
                    if r:
                        #print(f"Finished {newx}  {om}")
                        new_moves.append((newx, om))
                        continue
                if nm == 5:
                    new_moves.append((newx, om))
                for j in range(1,10):
                    if j in om or j in newx:
                        continue
                    newo = om + [j]
                    new_moves.append((newx, newo))
        yield new_moves
        moves = new_moves
        
def is_linked(board):
    """ Checks whether 3 x's or o's are
        present in the board
    """ 
    wonsym = '-'
    if (board[0] != '-' and board[0] == board[1] and board[0] == board[2]) or \
       (board[0] != '-' and board[0] == board[3] and board[0] == board[6]) or \
       (board[0] != '-' and board[0] == board[4] and board[0] == board[8]):
        wonsym = board[0]
    elif (board[1] != '-' and board[1] == board[4] and board[1] == board[7]):
        wonsym = board[1]
    elif (board[2] != '-' and board[2] == board[4] and board[2] == board[6]) or \
        (board[2] != '-' and board[2] == board[5] and board[2] == board[8]) :
        wonsym = board[2]
    elif (board[3] != '-' and board[3] == board[4] and board[3] == board[5]):
        wonsym = board[3]
    elif board[6] != '-' and board[6] == board[7] and board[6] == board[8]:
        wonsym = board[6] 
    return (True if wonsym != '-' else False, wonsym)

#if __name__ == "__main__":
#    st = {}
#    for moves in gen_moves(5):
#        print(f"moves: {len(moves)}")
#        for xm, om in moves:
#            sti = state_index(xm, om)
#            if sti in st:
#                st[sti].append((xm,om))
#            else:
#                st[sti] = [(xm,om)]
#    print(f"state-index: {len(st)}")
#    for k,v in st.items():
#        print(f"{k}: {len(v)}")
#        #if len(v) > 1:
#        #    print(v)

if __name__ == "__hhsjjs__":
    blist = [create_board_str([], [i]) for i in range(1,10)]
    blist.insert(0, create_board_str([], []))
    stlist = [state_index([], [i]) for i in range(1,10)]
    stlist.insert(0,0)
    print_board_horz(blist)
    print("".join([f"{i:<10}" for i in stlist]))
    for i in range(1,10):
        blist = []
        stlist = []
        x_moves = [i]
        o_moves = possible_o_moves(x_moves)
        blist.append(create_board_str(x_moves, []))
        stlist.append(state_index(x_moves, []))
        for j in range(1,10):
            if j in x_moves:
                blist.append(create_board_str([], []))
            else:
                blist.append(create_board_str(x_moves, [j]))
            stlist.append(state_index(x_moves, [j]))
        print_board_horz(blist)
        print("".join([f"{i:<10}" for i in stlist]))
