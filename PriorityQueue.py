### A priority queue implementation using a heap

class PriorityQueue:
  def __init__(self) -> None:
      self.index = {}
      self.heap = [] # A list of (priority, value) pairs
      self.size = 0
  def __len__(self):
    return self.size 
  def __str__(self):
    return str(self.heap)
  def __repr__(self):
    return str(self.heap)
  
  def heapify(self, i=0):
    if i >= self.size:
      return
    left = 2*i+1
    right = 2*i+2
    smallest = i
    if left < self.size and self.heap[left][0] < self.heap[smallest][0]:
      smallest = left
    if right < self.size and self.heap[right][0] < self.heap[smallest][0]:
      smallest = right
    if smallest != i:
      self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
      self.index[self.heap[i][1]] = i
      self.index[self.heap[smallest][1]] = smallest
      self.heapify(smallest)

  def fix_heap(self, i):
    ## When key is too small, we need to fix the heap
    if i < 0 or i >= self.size:
      return
    parent = (i-1)//2
    if parent >= 0 and self.heap[parent][0] > self.heap[i][0]:
      self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
      self.index[self.heap[i][1]] = i
      self.index[self.heap[parent][1]] = parent
      self.fix_heap(parent)
    else:
      self.heapify(i)
  
  def build_heap(self):
    for i in range(self.size//2,-1,-1):
      self.heapify(i)
  
  def extract_min(self):
    if self.size == 0:
      return None
    min = self.heap[0]
    self.heap[0] = self.heap[self.size-1]
    self.size-=1
    self.heapify()
    return min

  def insert(self, priority, value):
    self.heap.append((priority,value))
    self.index[value] = self.size
    self.size+=1
    self.fix_heap(self.size-1)


  def update(self, priority, value):
    i = self.index[value]
    self.heap[i] = (priority,value)
    self.fix_heap(i)
  