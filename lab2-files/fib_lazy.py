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


class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        # added for log calculation
        self.totalNodes = 0
        # added as pointer to keep track of min node
        self.min = None
        self.roots = []
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

        self.set_min()
        return self.min

    def find_min(self) -> FibNode:
        return self.min

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
        if firstnode.get_value_in_node() < secondnode.get_value_in_node():
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
