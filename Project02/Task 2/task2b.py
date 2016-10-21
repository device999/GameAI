from TreeNode import TreeNode

if __name__ == '__main__':

    # build custom tree
    root = TreeNode(0, None)
    node1 = TreeNode(1, None)
    node2 = TreeNode(2, None)
    node3 = TreeNode(3, None)
    node4 = TreeNode(4, None)
    node5 = TreeNode(5, 18)
    node6 = TreeNode(6, 6)
    node7 = TreeNode(7, 16)
    node8 = TreeNode(8, 6)
    node9 = TreeNode(9, 5)
    node10 = TreeNode(10, 7)
    node11 = TreeNode(11, 1)
    node12 = TreeNode(12, 16)
    node13 = TreeNode(13, 16)
    node14 = TreeNode(14, 5)
    node15 = TreeNode(15, 10)
    node16 = TreeNode(16, 2)

    root.insertChildren(root, [node1, node2, node3, node4])
    node1.insertChildren(node1, [node5, node6, node7, node8, node9])
    node2.insertChildren(node2, [node10, node11])
    node3.insertChildren(node3, [node12, node13, node14])
    node4.insertChildren(node4, [node15, node16])

    # run minmax algorithm from n0
    root.maxStep(root)

    root.printTree(root)

    print("mmv for n0: ", root.mmv, root.getMaxutil())

    print("Printing the path of the best MAX strategy")
    root.bestMaxStrategy(root)
