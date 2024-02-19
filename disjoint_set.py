## Implement the union-find algorithm.

## An element consists of the value (the item it self), depth (d) and reference. 
## An element with a None- reference is considered the "representative" of its set
class Element:
  def __init__(self,value):
    self.value = value
    self.ref = None
    self.d=0


class Disjoint_set:
  def __init__(self):
    ## Elements themselves are stored in a dictionary
    self.elements = {}
  
  def make_set(self,x):
    ## Making a set of value x:
    ex = Element(x)
    self.elements[x] = ex

  def Find(self,x):
    ## Find the representative of the value x, assuming it is one of the elements: 
    assert(x in self.elements)
    ex = self.elements[x]
    ref = ex.ref
    ## Recursively find the ref, and create shortcut
    if ref is not None:
      ref = self.Find(ref)
      ex.ref = ref
    ## If the ref is None, then this element is the representative, i.e., ex
    else:
      ref = ex
    ## Anyhoo, return the ref
    return ref
  
  ## The union:
  def Union(self,x,y):
    ## Find the elements of x and y:
    ex = self.Find(x)
    ey = self.Find(y)
    assert(ex.ref == None)
    assert(ey.ref == None)
    ## If they are the same, then do nothing
    if ex == ey:
      return
    ## Make the one with deeper tree the ref:
    if ex.d < ey.d:
      ex.ref = ey
    elif ex.d > ey.d:
      ey.ref = ex
    ## If they are equally deep, make ex the ref of y and increase depth.  
    else:
      ex.ref = ey
      ey.d+=1
