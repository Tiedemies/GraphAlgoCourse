## Generates a random four team communication graph, given parameters n, p, q, r, b
## n is the number of vertices in the graph, p is the intra group communication probability and q is the
## inter group communication probability. r is the number of rounds of communication.
## b is the balance parameter, with b = 0 meaning that the graph is balanced and b = 1 meaning that the group sizes are
## random.

from graph import Graph
from random import randint, random, shuffle
import sys

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

    return G, groups

if __name__ == "__main__":

    cmdArgN = len(sys.argv)

    if cmdArgN != 6:

        print("Usage:\n\n  python3 group_generator.py n:int p:float q:float r:float b:float\n")

    assert cmdArgN == 6, f"The number of command line arguments must be 5. Received {cmdArgN - 1}"

    nStr = sys.argv[1]

    try:

        n = int(nStr)

    except ValueError:

        print(f"Invalid command line argument 1 \"{nStr}\": cannot convert to number of vertices.")

        exit(-1)

    assert n > 0, f"Received a graph size of {n}, but graph sizes cannot be non-positive."

    pStr = sys.argv[2]

    try:

        p = float(pStr)

    except ValueError:

        print(f"\nInvalid command line argument 2 \"{pStr}\": cannot convert to float.")

        exit(-2)

    assert 0 <= p <= 1, f"The given communication probability p was not between 0 and 1."

    qStr = sys.argv[3]

    try:

        q = float(qStr)

    except ValueError:

        print(f"\nInvalid command line argument 3 \"{qStr}\": cannot convert to float.")

        exit(-3)

    assert 0 <= q <= 1, f"The given communication probability q was not between 0 and 1."

    rStr = sys.argv[4]

    try:

        r = int(rStr)

    except ValueError:

        print(f"\nInvalid command line argument 4 \"{rStr}\": cannot convert to number of communication rounds.")

        exit(-4)

    assert n > 0, f"Received a graph size of {n}, but graph sizes cannot be non-positive."

    bStr = sys.argv[5]

    try:

        b = float(bStr)

    except ValueError:

        print(f"Invalid command line argument 5 \"{bStr}\": cannot convert to float.")

        exit(-5)

    assert 0 <= b <= 1, f"The given balancing parameter b was not between 0 and 1."

    G, groups = four_team_communication(n,p,q,r,b)

    G.writegraph(f"four_team_communication_{n}")

    groupIDs = set(groups.values())

    groupLists = []

    for id in groupIDs:

        groupLists.append([])

    for vertex, groupID in groups.items():

        groupLists[groupID].append(vertex)

    for id in groupIDs:

        print(f"{id} ↦ {groupLists[id]}")
