import sys

values = [18, 6, 16, 6, 5, 7, 1, 16, 16, 5, 10, 2]
  
def make_move(node, maximizing):
  if node.terminal:
    return 0
  var = -1
  if maximizing:
    bestValue = -sys.maxint - 1
    next_bestValue = -sys.maxint - 1
    for i in range(0, len(node.leaves)):
     if node.leaves[i].value > bestValue:
       var = i
       bestValue = node.leaves[i].value
       next_bestValue = node.leaves[i].next_value
     if node.leaves[i].value == bestValue:
       if node.leaves[i].next_value > next_bestValue:
	 var = i
	 bestValue = node.leaves[i].value
	 next_bestValue = node.leaves[i].next_value
  else:
    bestValue = sys.maxint
    next_bestValue = sys.maxint
    for i in range(0, len(node.leaves)):
      if node.leaves[i].value < bestValue:
	var = i
	bestValue = node.leaves[i].value
	next_bestValue = node.leaves[i].next_value
      if node.leaves[i].value == bestValue:
	if node.leaves[i].next_value < next_bestValue:
	  var = i
	  bestValue = node.leaves[i].value
	  next_bestValue = node.leaves[i].next_value
  print var
  make_move(node.leaves[var], not maximizing)
	  
    

class Node:
  def __init__(self):
    self.leaves = []
    self.value = 0
    self.terminal = False
    self.next_value = 0
   
      
def minimax(node, depth, playerMax):
  if depth == 0 or node.terminal:
    return node.value
  if playerMax:
    bestValue = -sys.maxint - 1
    next_bestValue = sys.maxint
    for x in range(0, len(node.leaves)):
      val = minimax(node.leaves[x], depth-1, False)
      bestValue = max(bestValue, val)
      next_bestValue = min(next_bestValue, val)
    node.next_value = next_bestValue
    node.value = bestValue
    return bestValue
  else:
    bestValue = sys.maxint
    next_bestValue = -sys.maxint - 1
    for x in range(0, len(node.leaves)):
      val = minimax(node.leaves[x], depth-1, True)
      bestValue = min(bestValue, val)
      next_bestValue = max(next_bestValue, val)
    node.value = bestValue
    node.next_value = next_bestValue
    return bestValue

if __name__ == '__main__':
  root = Node()
  for i in range(0, 4):
    new_node = Node()
    root.leaves.append(new_node)
  for i in range(0, 5):
    new_node = Node()
    new_node.value = new_node.next_value = values[i]
    new_node.terminal = True
    root.leaves[0].leaves.append(new_node)
  for i in range(0, 2):
    new_node = Node()
    new_node.value = new_node.next_value = values[5 + i]
    new_node.terminal = True
    root.leaves[1].leaves.append(new_node)
  for i in range(0, 3):
    new_node = Node()
    new_node.value = new_node.next_value = values[7 + i]
    new_node.terminal = True
    root.leaves[2].leaves.append(new_node)
  for i in range(0, 2):
    new_node = Node()
    new_node.value = new_node.next_value = values[10 + i]
    new_node.terminal = True
    root.leaves[3].leaves.append(new_node)
  minimax(root, 2, True)
  make_move(root, True)