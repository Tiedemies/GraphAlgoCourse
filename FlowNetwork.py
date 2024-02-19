# A template for Ford Fulkerson algorithm and min cut

from graph import Graph
from copy import deepcopy as copy
import sys
from icecream import ic


## This code assumes flow is dictionary with keys (u,v) and values flow(u,v)
## Define the sum of two flows
def SumFlow(f1,f2):
  f = {}
  for (u,v) in set(f1.keys()) | set(f2.keys()):
    if not (u,v) in f1:
      f[(u,v)] = f2[(u,v)]
    elif not (u,v) in f2:
      f[(u,v)] = f1[(u,v)]
    else:
      f[(u,v)] = f1[(u,v)] + f2[(u,v)]
  return f




class FlowNetwork:
  def __init__(self,G) -> None:
    self.G = G
    self.FindSource()
    self.FindSink()
  ## Find the source, it is the first vertex with a non-empty adjacency list:
  def FindSource(self):
    for u in range(self.G.n):
      if len(self.G.adj[u]) > 0:
        self.s = u
        return
    
  ## Find the sink. It is the last vertex.
  def FindSink(self):
    self.t = self.G.n-1

  # Define the value of a flow
  def FlowValue(self,f):
    return sum([f[(self.s,u)] for u in G.adj[self.s] if (self.s,u) in f])


  ## Create a residual graph
  def MakeResidual(self, f):
    ## Copy the graph:
    G = copy(self.G)
    for (u,v) in f:
      c = 0
      ## Copy the weight
      if (u,v) in G.w:
        c = G.w[(u,v)]
      #calculate residual capasity
      cf = c - f[(u,v)]
      ## It is an error if the residual capacity is negative
      if cf < 0:
        raise Exception("capacity violation in f")
      ## Add the edge if the residual capacity is positive
      if not v in G.adj[u]:
        G.addEdge(u,v)
      G.w[(u,v)] = cf
    return G

  ## This is not implemented. Implement the augmenting path algorithm here
  def FindAugPath(self,Gr,s=None,t=None):
    if s is None:
      s = self.s
    if t is None:
      t = self.t
    Q = [s]
    dist = {s:0}
    pred = {s:None}
    while Q:
      u = Q.pop(0)
      if u < 0 or u >= len(Gr.adj):
        continue
      if u == t:  
        break
      for v in Gr.adj[u]:
        # Skip if the edge is saturated
        if (u,v) not in Gr.w or Gr.w[(u,v)] == 0:
          continue
        if v not in dist:
          Q.append(v)
          dist[v] = dist[u] + 1
          pred[v] = u
    if t not in dist:
      return []
    path = []
    u = t
    while u is not None:
      path.append(u)
      u = pred[u]
    path.reverse()
    return path  

  ## This is NOT implemented
  def MakeAugFlow(self,path, Gr = None):
    if Gr is None:
      Gr = self.G
    f = {}
    for i in range(len(path)-1):
      u = path[i]
      v = path[i+1]
      if (u,v) not in Gr.w or Gr.w[(u,v)] == 0:
        raise Exception("Edge not in Gr or saturated")
      f[(u,v)] = 0
    cf = min([Gr.w[(u,v)] for (u,v) in f])
    for (u,v) in f:
      f[(u,v)] = cf
    return f

  def FordFulkerson(self):
    f = {}
    G = self.G
    Gr = self.MakeResidual(f)
    ap = self.FindAugPath(G)
    while ap != []:
      fp = self.MakeAugFlow(ap,Gr)
      f = SumFlow(f,fp)
      Gr = self.MakeResidual(f)
      ap = self.FindAugPath(Gr)
    return f

  def MinCutEdges(self):
    f = self.FordFulkerson()
    ic(self.FlowValue(f))
    ## We find all reachable vertices from s in the residual graph, and mark them as S.
    S = set([self.s])
    Edges = []
    G = self.G
    ### Run BFS from s to find all reachable vertices, but stop when weight of the edge is 
    ### equal to the flow, because that edge is saturated. 
    Q = [self.s]
    while Q:
      u = Q.pop(0)
      if u < 0 or u >= len(G.adj):
        continue
      for v in G.adj[u]:
        if v not in S:
          if ((u,v) not in G.w or G.w[(u,v)] == 0) or ((u,v) in f and f[(u,v)] == G.w[(u,v)]):
            continue
          S.add(v)
          Q.append(v)
    Edges = [(u,v) for u in S for v in G.adj[u] if v not in S]
    ### Find the edges that cross the cut (S,T), i.e., they start from S and end in T.
    ### Return these edges.
    return Edges
            
if __name__ == "__main__":
    G = Graph()
    inputgraph = sys.argv[1]
    G.readgraph(inputgraph)
    F = FlowNetwork(G)
    edges = F.MinCutEdges()
    ic(sum([G.w[(u,v)] for (u,v) in edges]))
    ic(edges)

 