import numpy as np


# Transform an adjacency list into a anjacency matrix (numpy array)
def AdjacencyMatrix(adj_list: list[list[int]]) -> np.array:
    n = len(adj_list)
    adj_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in adj_list[i]:
            adj_matrix[i, j] = 1
    return adj_matrix
   
# Transform an adjacency list into a laplacian matrix (numpy array)
def Laplacian(adj: list[int]) -> np.array:
    n = len(adj)
    laplacian = np.zeros((n, n), dtype=int)
    for i in range(n):
        laplacian[i, i] = len(adj[i])
        for j in adj[i]:
            laplacian[i, j] = -1
    return laplacian


## Testcode:
if __name__  == "__main__":
    import graph
    g = graph.Graph(8)
    g.addEdge(0, 1)
    g.addEdge(1,2)
    g.addEdge(2,3)
    g.addEdge(3,4)
    g.addEdge(4,1)
    g.addEdge(3,5)
    g.addEdge(5,6)
    g.addEdge(6,7)
    g.addEdge(7,5)

    A = AdjacencyMatrix(g.adj)
    print(A)
    L = Laplacian(g.adj)
    print(L)
    

    x0 = np.array([0, 1, 1, 1, 1, 0, 0, 0])
    print(np.dot(L,x0))