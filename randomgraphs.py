### Generate random graphs by two different method.

import graph
from icecream import ic
import random

### Method 1: Erdos-Renyi random graph, n vertices and probability p for each edge to appear
def ErdosRenyi(n: int, p: float) -> graph.Graph:
  G = graph.Graph(n)
  for u in range(n):
    for v in range(n):
      if (u == v):
        continue
      if random.random() < p:
        G.addEdge(u, v)
  return G

### Method 2: Barabasi-Albert random graph, n final vertices, m0 initial vertices and m edges for each new vertex
def BarabasiAlbert(n: int, m0: int, m: int) -> graph.Graph:
  assert(m0 <= n)
  assert(m <= m0)
  G = graph.Graph(n)
  for u in range(m0):
    for v in range(m0):
      if (u == v):
        continue
      G.addEdge(u, v)
  for u in range(m0, n):
    # Take a random sample of m vertices from the vertices 0 to u-1, with probabilities proportional to their degrees
    # The sample is returned as a list of vertices
    sample = random.choices(range(u), weights=[len(G.adj[i]) for i in range(u)], k=m)
    for v in sample:
      G.addEdge(u, v)
  return G

## Create testpairs
def create_test_pairs():
  for i in range(10):
    n = (i+1)*10
    ic(n)
    filename = "testpair_" + str(i+1)
    f = open(filename,'w')
    f.write("1 " + str(n) + "\n")
    f.close()

def create_efficiency_test(n:int) -> graph.Graph:
  ## Generate a hard case for network flow. n is the number of diamonds.
  ## The graph has 3n vertices 5n edges
  ## The source is 0, the sink is 2n+1.
  G = graph.Graph(3*n+1)
  for i in range(n):
    G.addEdge(3*i,3*i+1, 100)
    G.addEdge(3*i,3*i+2, 100)
    G.addEdge(3*i+1,3*i+2, 1)
    G.addEdge(3*i+1,3*i+3, 99)
    G.addEdge(3*i+2,3*i+3, 101)
  return G
  

if __name__ == "__main__":
  G = create_efficiency_test(100)
  G.writegraph("efficiency_test.txt")


