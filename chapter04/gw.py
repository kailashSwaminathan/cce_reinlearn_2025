import numpy as np


states_map1 = {
       #   UP  DOWN  RIGHT  LEFT
    1  : [  1,    5,     2,    0 ],
    2  : [  2,    6,     3,    1 ],
    3  : [  3,    7,     3,    2 ],
    4  : [  0,    8,     5,    4 ],
    5  : [  1,    9,     6,    4 ],
    6  : [  2,   10,     7,    5 ],
    7  : [  3,   11,     7,    6 ],
    8  : [  4,   12,     9,    8 ],
    9  : [  5,   13,    10,    8 ],
    10 : [  6,   14,    11,    9 ],
    11 : [  7,    0,    11,   10 ],
    12 : [  8,   12,    13,   12 ],
    13 : [  9,   13,    14,   12 ],
    14 : [ 10,   14,     0,   13 ],
    15 : [ 13,   15,    14,   12 ]
}

states_map2 = {
       #   UP  DOWN  RIGHT  LEFT
    1  : [  1,    5,     2,    0 ],
    2  : [  2,    6,     3,    1 ],
    3  : [  3,    7,     3,    2 ],
    4  : [  0,    8,     5,    4 ],
    5  : [  1,    9,     6,    4 ],
    6  : [  2,   10,     7,    5 ],
    7  : [  3,   11,     7,    6 ],
    8  : [  4,   12,     9,    8 ],
    9  : [  5,   13,    10,    8 ],
    10 : [  6,   14,    11,    9 ],
    11 : [  7,    0,    11,   10 ],
    12 : [  8,   12,    13,   12 ],
    13 : [  9,   15,    14,   12 ],
    14 : [ 10,   14,     0,   13 ],
    15 : [ 13,   15,    14,   12 ]
}

def update(v, states_map):
    """
    """
    new_v = np.zeros(16)
    for i in range(1,16):
        s = states_map[i]
        new_v[i] = np.mean([-1 + v[j] for j in s])
        #v[i] = np.mean([-1 + v[j] for j in s])
    return new_v
    #return v

def print_v(v):
    for i in range(len(v)):
        if i == 15:
            print(f"\n           {v[i]:8.4f}")
        else:
            if i!= 0 and i % 4 == 0:
                print()
            print(f" {v[i]:8.4f} ", end="")
    print()

def print_v(v1, v2):
    fs = "11.6f"
    for i in range(0,len(v1),4):
        if i!= 0 and i % 4 == 0:
            print()
        ei = 4 if i != 12 else 3
        print("".join([f"{v1[j]:{fs}}" for j in range(i,i+ei)]), end="")
        if i == 12:
            print(f"{v1[0]:{fs}}", end="")
        print(" | ", end="")
        print("".join([f"{v2[j]:{fs}}" for j in range(i,i+ei)]), end="")
        if i == 12:
            print(f"{v2[0]:{fs}}", end="")
            print("\n" + " "*int(fs.split('.')[0]) + f"{v1[15]:{fs}}" + " "*2*int(fs.split('.')[0]) + " | " + " "*int(fs.split('.')[0]) + f"{v2[15]:{fs}}")
    print()

def main():
    v1, v2 = np.zeros(16), np.zeros(16)
    for k in range(500):
        if k in [0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,50,60,70,75,80,90,95,100,105,110,125,150,160,170,175,180,190,200,225,250,300]:
            print(f"k={k}")
            print_v(v1,v2)
        v1 = update(v1, states_map1)
        v2 = update(v2, states_map2)


if __name__ == "__main__":
    main()