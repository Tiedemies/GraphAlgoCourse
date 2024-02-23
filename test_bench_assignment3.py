## This file contains the test bench for the assignment 3
## It generates the "ground truth" for token race and tattle tale for the given graph.
## Include your own code to test the correctness of the implementation.

## NOTE: you are in no way allowed to use this code or similar code in your submission.
## This is only for testing purposes, and your analysis must be purely structural, and not based on the results of this code.

from graph import Graph
from random import randint, random


### test_token simulates the token game and returns the top 10 nodes with the highest token count
def test_token(G: Graph, nrounds: int = 1000) -> list[int]:
    d: float = 0.01 # Jump probability
    p: float = 0.0009 # termination probability
    n: int = G.n
    token_count: list[int] = [0 for _ in range(n)]
    for _ in range(nrounds):
        current = randint(0, n-1)
        while random() > p:
            ## Pick a random neighbor of G[current]
            neighbors = G.adj[current]
            ## Make the random neighbour if it exists and jump with probability 1-d
            if len(neighbors) > 0 and random() > d:
                current = neighbors[randint(0, len(neighbors)-1)] 
            ## otherwise jump to a random node
            else:
                current = randint(0, n-1)
        token_count[current] += 1 
    ## X contains the top 10 indices according to the token count
    X = sorted(range(len(token_count)), key=lambda i: token_count[i], reverse=True)[:10]
    return X

## test_tattle_tale simulates the tattle tale game and returns the top 10 nodes with the highest tattle tale count
def test_tattle_tale(G: Graph, nrounds: int = 1000) -> list[int]:
    tattle_tale_count: list[int] = [0 for _ in range(G.n)]
    for i in range(nrounds):
        ## Pick pick two nodes at random:
        u = -1
        v = -1
        while u == v:
            u = randint(0, G.n-1)
            v = randint(0, G.n-1)
        ## Start broadcasting from u:
        Q = [u]
        m_count = [0 for _ in range(G.n)]
        m_count[u] = 1
        msg = {u: {u: 1}}
        passive = [False for _ in range(G.n)]
        in_Q = [False for _ in range(G.n)]
        while Q:
            current = Q.pop(0)
            in_Q[current] = False
            passive[current] = True
            if current == v:
                break
            for neighbor in G.adj[current]:
                if not passive[neighbor]:
                    m_count[neighbor] += m_count[current]
                    if not in_Q[neighbor]:
                        Q.append(neighbor)
                        in_Q[neighbor] = True
                    if neighbor not in msg:
                        msg[neighbor] = {current: m_count[current]}
                    else:
                        msg[neighbor][current] = m_count[current]
                    M = msg[neighbor]
                    for x in msg[current]:
                        if x not in M:
                            M[x] = msg[current][x]
                        else:
                            M[x] += msg[current][x]
        ## Update the tattle tale count
        if not passive[v]:
            continue
        for j in range(G.n):
            if j in msg[v]:
                tattle_tale_count[j] += msg[v][j] / m_count[v]
    ## Return top ten nodes with the highest tattle tale count
    X = sorted(range(len(tattle_tale_count)), key=lambda i: tattle_tale_count[i], reverse=True)[:10]
    return X


if __name__ == "__main__":
    G = Graph()
    G.readgraph("example1.txt")
    X = test_token(G,nrounds=10000)
    Y = test_tattle_tale(G, nrounds=10000)
    print("token top 10:", X)
    print("tattle tale top 10:", Y)
    ## Add your own code to test the correctness of the implementation, to make sure that the results are similar
    ## to the ground truth. Remember, they may be some differences due to the randomness in the simulation.