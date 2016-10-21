import sys

values = [15, 20, 1, 3, 3, 4, 15, 10, 16, 4, 12, 15, 12, 8]
  

class Node:
  def __init__(self):
    self.leaves = []
    self.value = 0
    self.terminal = False
      
def minimax(node, depth, playerMax):
  if depth == 0 or node.terminal:
    return node.value
  if playerMax:
    bestValue = -sys.maxint - 1
    for x in range(0, len(node.leaves)):
      val = minimax(node.leaves[x], depth-1, False)
      bestValue = max(bestValue, val)
    node.value = bestValue
    return bestValue
  else:
    bestValue = sys.maxint
    for x in range(0, len(node.leaves)):
      val = minimax(node.leaves[x], depth-1, True)
      bestValue = min(bestValue, val)
    node.value = bestValue
    return bestValue

if __name__ == '__main__':
  root = Node()
  for i in range(0, 5):
    new_node = Node()
    root.leaves.append(new_node)
  for i in range(0, 4):
    new_node = Node()
    new_node.value = values[i]
    new_node.terminal = True
    root.leaves[0].leaves.append(new_node)
  for i in range(0, 2):
    new_node = Node()
    new_node.value = values[4 + i]
    new_node.terminal = True
    root.leaves[1].leaves.append(new_node)
  for i in range(0, 2):
    new_node = Node()
    new_node.value = values[6 + i]
    new_node.terminal = True
    root.leaves[2].leaves.append(new_node)
  for i in range(0, 3):
    new_node = Node()
    new_node.value = values[8 + i]
    new_node.terminal = True
    root.leaves[3].leaves.append(new_node)
  for i in range(0, 3):
    new_node = Node()
    new_node.value = values[11 + i]
    new_node.terminal = True
    root.leaves[4].leaves.append(new_node)
  minimax(root, 2, True)
  print root.value
  for i in range(0, 5):
    print root.leaves[i].value