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
        self.roots.append(newnode)
        if len(self.roots) == 1:
            self.min = newnode
        # update min
        if newnode.get_value_in_node() < self.min.get_value_in_node():
            self.min = newnode
        return newnode

    def delete_min(self) -> None:
        self.remove_min()
        self.roots.remove(self.min)

        # allocate array of size M + 1
        arr = [None] * (math.ceil(math.log2(self.totalNodes)) + 1)

        # all tree roots
        roots = self.roots[:]  # make a copy
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

    def find_min(self) -> FibNode:
        return self.min

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        self.promote(node)
        node.val = new_val
        if node.get_value_in_node() < self.min.get_value_in_node():
            self.min = node

    def promote(self, node: FibNode) -> None:
        # if node is root, just return
        if node.parent is None:
            return

        parent = node.parent
        if node in parent.get_children():
            parent.get_children().remove(node)
        self.roots.append(node)
        node.parent = None
        node.flag = False

        if parent.get_flag() is True and parent.parent is not None:
            self.promote(parent)
        else:
            # if parent not in self.get_roots():
            parent.flag = True

    def remove_min(self):
        for child in self.min.get_children():
            # set flags to False
            child.flag = False
            child.parent = None
            self.roots.append(child)

    def merge(self, firstnode: FibNode, secondnode: FibNode):
        if firstnode.get_value_in_node() < secondnode.get_value_in_node():
            firstnode.get_children().append(secondnode)
            secondnode.parent = firstnode
            return firstnode
        else:
            secondnode.get_children().append(firstnode)
            firstnode.parent = secondnode
            return secondnode

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
