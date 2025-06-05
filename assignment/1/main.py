import numpy as np
import matplotlib.pyplot as plt

class MultiArmedBandit:
    """ Class for the Multi-Armed Bandit slot machine
    """
    def __init__(self, narm=10):
        self.narm = narm
        self.avalue = [0] * narm # action-value
        self.acount = [0] * narm # action-count
        self.laction = []        # list of actions
        self.lreward = []        # list of rewards
        self.gmean = np.random.normal(0,1,narm)

    def select_action(self, a):
        """
        """
        self.laction.append(a)
        self.acount[a] += 1
        r = np.random.normal(self.gmean[a],1)
        self.lreward.append(r)
        self.avalue[a] = self.avalue[a] + (r - self.avalue[a])/self.acount[a]
        return r

    @property
    def opact(self):
        """ Optimal action
        """
        return int(np.argmax(self.gmean))

def run_mab_ucb(mab, c, nsteps=1000):
    """ Executes Multi-Armed Bandit for
        nsteps. Uses Upper Confidence Bound (UCM)
        method for action selection with 
        parameter c.
    """
    avalue, acount = mab.avalue, mab.acount
    for s in range(nsteps):
        if acount.count(0) != 0:
            # if count is zero, then a is considered as 
            # maximizing action
            a = acount.index(0)
        else:
            av = [avalue[i] + c*np.sqrt(np.log(s)/acount[i]) for i in range(mab.narm)]
            a = int(np.argmax(av))
        r = mab.select_action(a)

def run_mab_egreedy(mab, efunc, nsteps=1000):
    """ Executes Multi-Armed Bandit for nsteps. Uses ε-greedy method
        for action selection with efunc method to generate epsilon 
        based on the current step
    """
    avalue, acount = mab.avalue, mab.acount
    for s in range(nsteps):
        epsilon = efunc(s)
        if np.random.rand() < epsilon:
            # Choose an exploratory action
            a = np.random.randint(mab.narm)
        else:
            # Choose a greedy action
            a = int(np.argmax(avalue))
        r = mab.select_action(a)


def setup_plot():
    """
    """
    fig, axes = plt.subplots(2,1)
    axes[0].set_xlabel('Steps')
    axes[0].set_ylabel('Average\nreward')
    axes[1].set_xlabel('Steps')
    axes[1].set_ylabel('Optimal\naction')
    axes[0].grid(True)
    axes[1].grid(True)
    return fig, axes

def var_e(s):
    """ Function to give a decreasing value of epsilon based on the 
        current step s using the formula
        ε = 1/(n+1), for the steps ∈ [50n, 50(n+1)), n>=0
    """
    q = s // 50
    return (1/(q + 1))

# Configuration for the different experiments
expt_config = [
    [run_mab_egreedy, lambda x: 0.1, 'ε=0.1', 'ε-greedy, ε=0.1'],
    [run_mab_egreedy, lambda x: 0.2, 'ε=0.2', 'ε-greedy, ε=0.2'],
    [run_mab_egreedy, var_e, 'ε=1.0,0.5,0.33,...', 'ε-greedy, ε=1.0,0.5,...'],
    [run_mab_ucb, 1, 'UCB, c=1', 'UCB, c=1'],
    [run_mab_ucb, 10, 'UCB, c=10', 'UCB, c=10'],
]

def main():
    """
    """
    #np.random.seed(42)
    narm, nsteps, nrun = 10, 1000, 2000
    fig,axes = setup_plot()
    for rfunc, param, lbl, desc in expt_config:
        print(f"Executing run {desc} ...")
        treward = np.zeros(nsteps)    # total reward
        optal = np.zeros(nsteps)      # list of optimal actions
        for i in range(nrun):
            mab = MultiArmedBandit()
            rfunc(mab, param, nsteps)
            treward = np.add(treward, mab.lreward)
            optal = np.add(optal,[i == mab.opact for i in mab.laction])
        treward /= nrun
        optal = (optal / nrun) * 100
        axes[0].plot(treward,label=f'{lbl}')
        axes[1].plot(optal,label=f'{lbl}')
        print(optal[9:20])
    axes[0].legend()
    axes[1].legend()
    plt.show()

if __name__ == "__main__":
    main()