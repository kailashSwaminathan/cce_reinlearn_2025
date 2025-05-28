import numpy as np 

def print_board(board):
    """
    """
    print(" --- --- ---")
    bstr = "|" + "".join([f" {i if i else ' '} |" for i in board])
    bstr = bstr[:13] + "\n|" + bstr[13:25] + "\n|" + bstr[25:] 
    print(bstr)
    print(" --- --- ---")

def print_boards(boardl):
    """
    """
    for i,b in enumerate(boardl,1):
        print(f"{i}.")
        print_board(b)

def main():
    """
    """
    print("Board positions")
    boardpos = dict([(1,list(['1','2','3'])),(2,list(['4','5','6'])),(3,list(['7','8','9']))])
    print_board(boardpos)
    board = dict([(1,list(['x','x','x'])),(2,list(['o','o','o'])),(3,list(['','','']))])
    c = ''
    while c != 'c':
        c = input('Enter (c - close| <pos> <x|o>): ')
        print(c)
        
    print_board()

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

def generate_game(debug=False):
    """ Generates valid boards
    """
    board = "-" * 9
    sym = ''
    gover = False
    posl = []
    while board.count('-') != 0 and not gover:
        sym = 'x' if sym == 'o' else 'o'
        pos = np.random.randint(0,9)
        while board[pos] != '-':
            pos = np.random.randint(0,9)
        if debug:
            print(f"sym: {sym} at pos: {pos}")
        posl.append(pos)
        newboard = board[:pos] + sym
        if pos < len(board) - 1:
            newboard = newboard + board[pos+1:]
        if debug:
            print(newboard)
        board = newboard
        gover, wonsym = is_linked(board)
    return (board,posl,'Won' if gover else 'Draw',wonsym)
    

def generate_draw():
    """ Generate draw configurations
    """
    gdraw = []
    count = 0
    while count < 10000:
        count += 1
        b,pl,r,sym = generate_game()
        if r == 'Draw':
            if b not in gdraw:
                gdraw.append(b)
            else:
                print(f"Duplicate game: {b}")
    print(f"Number of drawn games: {len(gdraw)}")
    print_boards(gdraw)

def generate_won():
    """
    """
    games = []
    count = 0
    while count < 10000:
        count += 1
        b,pl,r,sym = generate_game()
        if r == 'Won' and b.count('-') == 0:
            if b not in games:
                games.append(b)
            else:
                print(f"Duplicate game: {b}")
    print(f"Number of games won: {len(games)}")
    print_boards(games)

def generate_board():
    """
    """
    blist = []
    board = 'o' * 9
    blist.append(board)
    for nt in range(1,10):
        posl = gen_pos(nt)
        for indx in posl:
            newb = board
            for j in indx:
                if j == len(newb) - 1:
                    newb = newb[:j] + 'x'
                else:
                    newb = newb[:j] + 'x' + newb[j+1:]
            blist.append(newb)
    print(f"Number of boards: {len(blist)}")
    print_boards(blist)
    

def gen_pos(nt):
    """ Generate positions from 1 to 9
    """
    posl = [[0], [1], [2], [3], [4], [5], [6], [7], [8]]
    for i in range(1,nt):
        newl = []
        for j in range(len(posl)):
            for k in range(posl[j][-1]+1,9):
                newl.append(posl[j] + [k])
        posl = newl
    return posl

def train_model(numcount=10000):
    """
    """
    mstate_o = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    mstate_x = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    reward_o = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    reward_x = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    count = 0
    while count < numcount:
        count += 1
        b,pl,r,sym = generate_game()
        print(b,pl,r,sym)
        plo = pl[::2]
        plx = pl[1::2]
        ro = r == 'Won' and sym == 'o'
        rx = r == 'Won' and sym == 'x'
        rwd_o = 1 if r == 'Draw' else \
                10 if r == 'Won' and sym == 'o' else \
                -10 if r == "Won" and sym == 'x' else \
                0
        rwd_x = 1 if r == 'Draw' else \
                10 if r == 'Won' and sym == 'x' else \
                -10 if r == "Won" and sym == 'o' else \
                0
        prevp = -1
        for p in plo:
            if prevp == -1:
                prevp = p
            else:
                mstate_o[prevp][p] += 1
                reward_o[prevp][p] += rwd_o
                prevp = p
        prevp = -1
        for p in plx:
            if prevp == -1:
                prevp = p
                continue
            mstate_x[prevp][p] += 1
            reward_x[prevp][p] += rwd_x
            prevp = p
    return mstate_o, reward_o, mstate_x, reward_x


if __name__ == "__main__":
    main()