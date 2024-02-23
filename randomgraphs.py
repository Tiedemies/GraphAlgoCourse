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

def make_connected(G: graph.Graph) -> graph.Graph:
  ## Make the graph connected by adding edges
  n = G.n
  avg_w = 0
  std_w = 0
  if G.w:
    avg_w = sum(G.w.values())/len(G.w)
    std_w = (sum([(G.w[(u,v)] - avg_w)**2 for (u,v) in G.w])/len(G.w))**0.5
  for u in range(n):
    if len(G.adj[u]) == 0:
      v = random.randint(0,n-1)
      if G.w:
        w = random.gauss(avg_w, std_w)
        G.addEdge(u,v,w)
      else:
        G.addEdge(u,v)
      
  return G

if __name__ == "__main__":
  G = BarabasiAlbert(100, 10, 5)
  G = make_connected(G)
  G.writegraph("example1.txt")


