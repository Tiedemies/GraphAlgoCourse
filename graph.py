### This is a graph class that is used to represent a directed graph
### It is meant as an example for use in the course Graph Algorithms.
### It uses an adjacency list representation.
## TESTED on python 3.9.12
# from icecream import ic

class Graph:
  """ initialize a graph with n vertices and no edges """
  def __init__(self, n=None) -> None:
    if n is None:
      self.n = 0
    else:
      self.n = n
    self.adj = [[] for i in range(self.n)]
    self.w = {}

  """ A method of checking if two graphs are the same """
  def __eq__(self, other) -> bool:
    if self.n != other.n:
      return False
    for u in range(self.n):
      if self.adj[u] != other.adj[u]:
        return False
    return True

  """ add an edge from vertex u to vertex v """
  def addEdge(self, u: int, v: int, w = None) -> None:
    nn = self.n
    self.n = max(u+1,v+1, self.n)
    self.adj.extend([[] for i in range(self.n - nn)])
    if v not in self.adj[u]:
      self.adj[u].append(v)
    if w is not None:
      self.w[(u,v)] = w
  
  """ An input file format for a graph is as follows:"""
  """ Each line contains a vertex u, followed by ":" and a list of vertices separated by semicolons """
  """ If the graph is weighted, the vertices are given as pairs  (v,w) """
  def readgraph(self, filename: str) -> None:
    f = open(filename, 'r')
    for line in f:
      line = line.split(":")
      u = int(line[0])
      if u >= self.n:
        self.adj.extend([ [] for i in range(u+1-self.n)])
        self.n = u+1
      if len(line) > 1:
        edges = line[1]
        if ';' in edges:
          delim = ';'
        else:
          delim = ' '
        for v in edges.split(delim):
          try: 
            if len(v.split(",")) > 1:
              v = v.strip('()')
              vv,w = v.split(",")              
              self.addEdge(u,int(vv),int(w))
            else:                 
              v.strip()             
              self.addEdge(u,int(v))
          except:
            #ic(v)
            pass
    f.close()

  """ Output file in the same format as input file """
  def writegraph(self, filename: str) -> None:
    f = open(filename, 'w')
    for u in range(self.n):
      f.write(str(u)+":")
      for v in self.adj[u]:
        if (u,v) in self.w:
          f.write(str(v)+","+str(self.w[(u,v)])+";")
        else:
          f.write(str(v)+";")
      f.write("\n")

### Test code which inputs the graph manually, then outputs, then reads it.
if __name__ == "__main__":
  G = Graph(5)
  G.addEdge(0,1)
  G.addEdge(0,2)
  G.addEdge(1,3)
  G.addEdge(2,3,5)
  G.writegraph("testgraph.txt")
  
  U = Graph()
  U.readgraph("testgraph.txt")

  print(G == U)