# explanations for member functions are provided in requirements.py
from __future__ import annotations
import math


class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val


class FibHeapLazy:
    def __init__(self):
        # you may define any additional member variables you need
        # added for log calculation
        self.totalNodes = 0
        # added as pointer to keep track of min node
        self.min = None
        self.roots = [] # list of FibNode
        # pass

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        self.totalNodes += 1
        newnode = FibNode(val)
        self.roots.append(FibNode(val))
        if len(self.roots) == 1:
            self.min = newnode
        # update min
        if newnode.get_value_in_node() < self.min.get_value_in_node():
            self.min = newnode
        return newnode

    def delete_min(self) -> None:
        self.min.val = None

    def find_min(self) -> FibNode:
        if self.min.get_value_in_node() is None:
            self.remove_vacant_nodes(self.min)
        
        # allocate array of size M + 1
        arr = [None] * (math.ceil(math.log(self.totalNodes)) + 1)

        # all tree roots
        roots = self.roots
        while roots:
            root = roots.pop()
            degree = len(root.get_children())
            if arr[degree] is None:
                arr[degree] = root
            else:
                # merge
                newroot = self.merge(root, arr[degree])
                roots.append(newroot)
                arr[degree] = None

        # my own embellishment, reinstantiate self.roots - can counteract by making roots a deep copy
        for a in arr:
            if a is not None:
                self.roots.append(a)

        self.set_min()
        return self.min
    
    def remove_vacant_nodes(self, min: FibNode):
        for child in min.get_children():
            self.roots.append(child)
            if child.get_value_in_node() is None:
                self.remove_vacant_nodes(child)
        self.roots.remove(min)


    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        self.promote(node)
        if node.get_value_in_node() < self.min.get_value_in_node():
            self.min = node

    def promote(self, node: FibNode) -> None:
        # if node is root, just return
        if node.parent is None:
            return

        parent = node.parent
        parent.get_children().remove(node)
        self.roots.append(node)
        node.parent = None
        node.get_flag = False

        if parent.get_flag() is True:
            self.promote(parent)
        else:
            if parent not in self.get_roots():
                parent.get_flag = True

    def remove_min(self):
        for child in self.min.get_children():
            # set flags to False
            child.get_flag = False
            self.roots.append(child)

    def merge(self, firstnode: FibNode, secondnode: FibNode):
        newroot = firstnode
        # need to check for vacant node
        if firstnode.get_value_in_node() is None:
            newroot = firstnode
            firstnode.get_children().append(secondnode)
        elif secondnode.get_value_in_node() is None:
            newroot = secondnode
            secondnode.get_children().append(firstnode)
        elif firstnode.get_value_in_node() < secondnode.get_value_in_node():
            newroot = firstnode
            firstnode.get_children().append(secondnode)
        else:
            newroot = secondnode
            secondnode.get_children().append(firstnode)

        # return the node
        return newroot

    def set_min(self):
        minroot = self.roots[0]
        for root in self.roots:
            if root.get_value_in_node() < minroot.get_value_in_node():
                minroot = root
        self.min = minroot
        return minroot

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
