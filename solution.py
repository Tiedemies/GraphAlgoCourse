import graph

def algorithm(g: graph.Graph, B, s:int, t:int) -> int:
  Q = [s]
  dist = {s:0}
  count = {s:1 if s in B else 0}
  while Q:
    u = Q.pop(0)
    if u < 0 or u >= len(g.adj):
      continue
    if u == t:
      return count[t]
    for v in g.adj[u]:
      if v not in dist:
        Q.append(v)
        dist[v] = dist[u] + 1
        count[v] = 0
      if dist[v] == dist[u] + 1:
        isB = 1 if v in B else 0
        count[v] = max(count[v], count[u] + isB)
  return 0
