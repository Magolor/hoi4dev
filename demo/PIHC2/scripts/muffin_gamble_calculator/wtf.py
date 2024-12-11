# %%
import itertools
import numpy as np
np.random.seed(42)
import matplotlib.pyplot as plt

def plot_distribution(numbers):
    plt.hist(numbers, bins='auto', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.5)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Distribution Plot')
    plt.show()

def f(l, P=0.8):
    p = np.random.rand()
    if l >= 0:
        if p < P:
            return True
        else:
            return False
    else:
        if p < P:
            return False
        else:
            return True

def evaluate(strat, P, N, p, n, T=500, F=200):
    K = P+N; G = 0; C = 0
    for _ in range(10000):
        for indexes in itertools.combinations(range(K), P):
            boxes = [p if i in indexes else n for i in range(K)]
            G += strat(boxes, T, F); C += 1
    return G/C - T

def variance_evaluate(strat, P, N, p, n, T=500, F=200, batch=1):
    K = P+N; Gs = list()
    perms = list(itertools.combinations(range(K), P))
    for _ in range(100000):
        G = 0
        for b in range(batch):
            perm = perms[np.random.choice(range(len(perms)))]
            boxes = [p if i in perm else n for i in range(K)]
            G += strat(boxes, T, F) - T
        Gs.append(G)
    print(max(Gs))
    print(sum(Gs)/len(Gs))
    print(sum([g>0 for g in Gs])/len(Gs))
    plot_distribution(Gs)

# v1: greedy in terms of probability
def v1(L, T=500, F=200):
    S = [sum(L[i:]) for i in range(len(L))]; g = 0
    for l, s in zip(L, S):
        if s >= 0:
            g += l
    return g

# v2: greedy in terms of probability with fortune teller
def v2(L, T=500, F=200):
    S = [sum(L[i:]) for i in range(len(L))]; g = 0
    for i, (l, s) in enumerate(zip(L, S)):
        if i==0:
            if f(l):
                g += l; g -= F
        elif s >= 0:
            g += l
    return g

# v3: all fortune teller
def v3(L, T=500, F=200):
    S = [sum(L[i:]) for i in range(len(L))]; g = 0
    for i, (l, s) in enumerate(zip(L, S)):
        if -F <= s <= F:
            if f(l):
                g += l; g -= F
        elif s >= 0:
            g += l
    return g

# v4: greedy + double
def v4(L, T=500, F=200):
    S = [sum(L[i:]) for i in range(len(L))]; g = 0
    for i, (l, s) in enumerate(zip(L, S)):
        if i==len(L)-1 and s>=0:
            g += 2*l
        elif s >= 0:
            g += l
    return g

if __name__=="__main__":
    P = 5
    N = 4
    p = 1050
    n = -1050
    T = 500
    F = 200
    
    # # Enumerate all the orderings
    # print(evaluate(v1, P, N, p, n, T, F))
    # print(evaluate(v2, P, N, p, n, T, F))
    # print(evaluate(v3, P, N, p, n, T, F))
    
    variance_evaluate(v4, P, N, p, n, T, F, batch=20)
# %%
