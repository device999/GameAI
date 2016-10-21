from TreeNode import TreeNode

if __name__ == '__main__':

    # build custom tree
    root = TreeNode(0, None)
    node1 = TreeNode(1, None)
    node2 = TreeNode(2, None)
    node3 = TreeNode(3, None)
    node4 = TreeNode(4, None)
    node5 = TreeNode(5, None)
    node6 = TreeNode(6, 15)
    node7 = TreeNode(7, 20)
    node8 = TreeNode(8, 1)
    node9 = TreeNode(9, 3)
    node10 = TreeNode(10, 3)
    node11 = TreeNode(11, 4)
    node12 = TreeNode(12, 15)
    node13 = TreeNode(13, 10)
    node14 = TreeNode(14, 16)
    node15 = TreeNode(15, 4)
    node16 = TreeNode(16, 12)
    node17 = TreeNode(17, 15)
    node18 = TreeNode(18, 12)
    node19 = TreeNode(19, 8)

    root.insertChildren(root, [node1, node2, node3, node4, node5])
    node1.insertChildren(node1, [node6, node7, node8, node9])
    node2.insertChildren(node2, [node10, node11])
    node3.insertChildren(node3, [node12, node13])
    node4.insertChildren(node4, [node14, node15, node16])
    node5.insertChildren(node5, [node17, node18, node19])

    #root.printTree(root)

    # run minmax algorithm from n0
    root.maxStep(root)

    root.printTree(root)

    print("mmv for n0: ", root.mmv)
