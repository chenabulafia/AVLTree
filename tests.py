from AVLTree import AVLTree


def tests():
    errors = []
    t_root = AVLTree()
    for i in [7,5,3,6,9,4,12,8,11,30,64,2,1]:
        t_root.insert(i, "", "root")

    t_max = AVLTree()
    for i in [7,5,3,6,9,4,12,8,11,30,64,2,1]:
        t_max.insert(i, "", "max")

    t_empty = AVLTree()
		
    if t_max.get_root().key != 9:
        errors.append("max tree root is wrong")

    if t_root.get_root().key != 9:
        errors.append("root tree root is wrong")

    if t_max.max_node.key != 64:
        errors.append("max tree max node is wrong")   

    if t_root.max_node.key != 64:
        errors.append("root tree max node is wrong")

    if t_root.search(15) is not None:
        errors.append("search for non existing node doesnt return None") 

    leaf = t_root.search(6)
    if leaf is None or leaf.left.is_real_node() or leaf.right.is_real_node() or leaf.key != 6:
        errors.append("search for leaf is wrong")

    mid_node = t_root.search(3)
    if mid_node is None or mid_node.left.key != 2 or mid_node.right.key != 4 or mid_node.key != 3:
        errors.append("search for mid node is wrong")

    root = t_root.search(9)
    if root is None or root.left.key != 5 or root.right.key != 12 or root.key != 9:
        errors.append("search for root node is wrong")

    t_root.delete(t_root.search(1))
    if t_root.search(1) is not None:
        errors.append("search for deleted node doesnt return None")

    if t_empty.search(5) is not None:
        errors.append("search on empty tree wrong")

    if t_empty.avl_to_array() != []:
        errors.append("array for empty tree is broken")

    if t_root.avl_to_array() !=[(2, ""),(3, ""),(4,""),(5,""),(6,""),(7,"") ,(8,""),(9,""),(11,""),(12, ""),(30, ""),(64,"")]:
        errors.append("array for tree with deleted node is broken")
    
    if t_max.avl_to_array() !=[(1,""),(2, ""),(3, ""),(4,""),(5,""),(6,""),(7,"") ,(8,""),(9,""),(11,""),(12, ""),(30, ""),(64,"")]:
        errors.append("array for tree is broken")
    
    if t_empty.size() != 0:
        errors.append("size on empty tree is broken")

    if t_max.size() != 13:
        errors.append("size on tree is broken")

    if t_root.size() != 12:
        errors.append("size on tree with deleted node is broken")

    t_root.print_tree()

    print("\n".join(errors))

    
def test_delete():
    t_root = AVLTree()
    for i in [7,5,3,6,9,4,12,8,11,30,64,2,1]:
        c = t_root.insert(i, "", "root")
        print("_____________________________________________________")
        print(f"changes: {c}")
        t_root.print_tree()
        print("_____________________________________________________")

    r = t_root.delete(t_root.search(9))
    print(f"root: {t_root.root.key}, bf0: {t_root.bf0_count}, max: {t_root.max_node.key}, fixes: {r}")
    t_root.print_tree()


tests()
test_delete()
print("finised!")