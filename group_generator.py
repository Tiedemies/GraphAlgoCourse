## Generates a random four team communication graph, given parameters n, p, q, r, b
## n is the number of vertices in the graph, p is the intra grop communication probability and q is the 
## inter group communication probability. r is the number of rounds of communication.
## b is the balance parameter, with b = 0 meaning that the graph is balanced and b = 1 meaning that the group sizes are
## random.

from graph import Graph
from random import randint, random, shuffle

def four_team_communication(n: int, p: float = 0.2, q: float = 0.05, r: int = 1, b: float = 0) -> Graph:
    G = Graph(n)
    ## First create the four groups:
    ## Random permutation of the vertices:
    perm = list(range(n))
    shuffle(perm)
    ## Divide the vertices into four groups, b is the balance parameter
    even_limits = [int(n/4), int(n/2), int(3*n/4)]
    ## Pick three random numbers between 0 and n-1
    rand_limits = [randint(0, n-1) for _ in range(3)]
    rand_limits.sort()
    ## Then the limits as linear combinations of the even limits and the random limits:
    limits = [int((1-b)*even_limits[i] + b*rand_limits[i]) for i in range(3)]
    ## Now make sure no two limits are the same:
    for i in range(2):
        while limits[i] == limits[i+1]:
            limits[i+1] += 1
    limits.sort()
    ## Now create the groups:
    groups = {}
    for u in range(n):
        if u < limits[0]:
            groups[u] = 0
        elif u < limits[1]:
            groups[u] = 1
        elif u < limits[2]:
            groups[u] = 2
        else:
            groups[u] = 3
    ## Now create the edges:
    for i in range(r):
        for u in range(n):
            for v in range(n):
                if u == v:
                    continue
                ## If u and v are in the same group, add an edge with probability p
                if groups[u] == groups[v] and random() < p:
                    G.addEdge(u, v)
                elif groups[u] != groups[v] and random() < q:
                    G.addEdge(u, v)
    return G

if __name__ == "__main__":
    G = four_team_communication(100)
    G.writegraph("four_team_communication_100")
    