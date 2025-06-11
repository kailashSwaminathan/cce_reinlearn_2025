import numpy as np

# Initialization
gamma = 1.0
rows, columns = 4, 4
states = rows * columns
terminals = [0, 15]
V = np.zeros(states)
V_ = np.zeros(states)
VV = np.zeros((rows, columns))
Vk = np.zeros((1000, rows, columns))

def greedy_policy(state):
    if state in terminals:
        return None
    best_q = -10000.0
    best_actions = []
    
    for a in range(4):
        q = full_backup(state, a)
        if q > best_q:
            best_q = q
            best_actions = [a]
        elif q == best_q:
            best_actions.append(a)
    
    return best_actions

def setup():
    global V, V_, VV, Vk
    V.fill(0.0)
    V_.fill(0.0)
    VV.fill(0.0)
    Vk.fill(0.0)

def compute_V():
    global V, V_, Vk
    V.fill(0.0)
    
    for k in range(1000):
        for state in range(1, states-1):
            V_[state] = np.mean([full_backup(state, a) for a in range(4)])
            x, y = xy_from_state(state)
            Vk[k, x, y] = V[state]
        
        V, V_ = V_, V  # Swap references
        
    for state in range(states):
        x, y = xy_from_state(state)
        VV[y, x] = V[state]

def compute_V_star():
    global V, V_, Vk
    V.fill(0.0)
    
    for k in range(1000):
        for state in range(1, states-1):
            V_[state] = max(full_backup(state, a) for a in range(4))
            x, y = xy_from_state(state)
            Vk[k, x, y] = V[state]
        
        V, V_ = V_, V  # Swap references
    
    for state in range(states):
        x, y = xy_from_state(state)
        VV[y, x] = V[state]

def full_backup(state, action):
    if off_grid(state, action):
        reward = -1
        next_state = state
    else:
        reward = -1
        next_state = next_state_func(state, action)
    
    return reward + gamma * V[next_state]

def off_grid(state, action):
    x, y = xy_from_state(state)
    if action == 0: return y + 1 >= rows
    if action == 1: return x + 1 >= columns
    if action == 2: return y - 1 < 0
    if action == 3: return x - 1 < 0
    return False

def next_state_func(state, action):
    x, y = xy_from_state(state)
    if action == 0: y += 1
    elif action == 1: x += 1
    elif action == 2: y -= 1
    elif action == 3: x -= 1
    return state_from_xy(x, y)

def state_from_xy(x, y):
    return y + x * columns

def xy_from_state(state):
    return divmod(state, columns)

def compute_V_steps(steps):
    global V, V_, Vk
    V.fill(0.0)
    
    for k in range(steps):
        for state in range(1, states-1):
            V_[state] = np.mean([full_backup(state, a) for a in range(4)])
            print(V_[state])
            x, y = xy_from_state(state)
            Vk[k, x, y] = V[state]
        
        print(V_)
        V, V_ = V_, V  # Swap references
    
    for state in range(states):
        x, y = xy_from_state(state)
        VV[y, x] = V[state]

setup()
compute_V_steps(3)
