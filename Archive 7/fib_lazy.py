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
        self.roots = []  # list of FibNode
        # pass

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        self.totalNodes += 1
        newnode = FibNode(val)
        self.roots.append(newnode)
        # if len(self.roots) == 1:
        #     self.min = newnode
        # update min
        #
        if (
            self.min is None
            or self.min.get_value_in_node() is None
            or newnode.get_value_in_node() < self.min.get_value_in_node()
        ):
            self.min = newnode
        return newnode

    def delete_min_lazy(self) -> None:
        if self.min is not None and self.min.get_value_in_node() is not None:
            self.min.val = None
            self.totalNodes -= 1

    def find_min_lazy(self) -> FibNode:
        if self.min is None:
            return None

        if self.min.get_value_in_node() is None:
            # clean ALL vacant roots across the entire root list, not just self.min
            new_roots = []
            roots_to_process = self.roots[:]
            
            while roots_to_process:
                curr = roots_to_process.pop()
                if curr.get_value_in_node() is None:
                    # vacant
                    for child in curr.get_children():
                        child.parent = None
                        child.flag = False
                        roots_to_process.append(child)
                else:
                    new_roots.append(curr)
            
            self.roots = new_roots
            
            arr = []
            roots = self.roots[:]
            self.roots = []

            while roots:
                root = roots.pop()
                degree = len(root.get_children())
                
                while True:
                    # add more room if needed
                    while degree >= len(arr):
                        arr.append(None)
                        
                    if arr[degree] is None:
                        break
                        
                    other = arr[degree]
                    arr[degree] = None
                    root = self.merge(root, other)
                    degree = len(root.get_children())
                    
                arr[degree] = root

            # my own embellishment, reinstantiate self.roots - can counteract by making roots a deep copy
            for a in arr:
                if a is not None:
                    self.roots.append(a)

        self.set_min()
        return self.min

    """ def find_min_lazy(self) -> FibNode:
        if self.min is None:
            return None

        if self.min.get_value_in_node() is None:
            self.remove_vacant_nodes(self.min)

            if self.totalNodes <= 1:
                max_degree = 2
            else:
                max_degree = int(1.5 * math.log2(self.totalNodes)) + 2

            arr = [None] * max_degree
            roots = self.roots[:]  # make a copy!
            self.roots = []

            while roots:
                root = roots.pop()
                degree = len(root.get_children())

                while arr[degree] is not None:
                    other = arr[degree]
                    arr[degree] = None
                    root = self.merge(root, other)
                    degree = len(root.get_children())

                arr[degree] = root

            # my own embellishment, reinstantiate self.roots - can counteract by making roots a deep copy
            for a in arr:
                if a is not None:
                    self.roots.append(a)

        self.set_min()
        return self.min """

    """ def remove_vacant_nodes(self, min: FibNode):
        children = list(min.get_children())
        min.children = []
        for child in children:
            child.parent = None
            if child.get_value_in_node() is None:
                self.remove_vacant_nodes(child)
            else:
                child.flag = False
                self.roots.append(child)

        if min in self.roots:
            self.roots.remove(min)   """

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        self.promote(node)
        node.val = new_val
        if (
            self.min is None
            or self.min.get_value_in_node() is None
            or node.get_value_in_node() < self.min.get_value_in_node()
        ):
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

        if parent.get_flag() is True:
            self.promote(parent)
        else:
            if parent not in self.get_roots():
                parent.flag = True

    def remove_min(self):
        for child in self.min.get_children():
            # set flags to False
            child.flag = False
            child.parent = None
            self.roots.append(child)

    def merge(self, firstnode: FibNode, secondnode: FibNode):
        # need to check for vacant node
        if firstnode.get_value_in_node() is None:
            firstnode.get_children().append(secondnode)
            secondnode.parent = firstnode
            return firstnode
        elif secondnode.get_value_in_node() is None:
            secondnode.get_children().append(firstnode)
            firstnode.parent = secondnode
            return secondnode
        elif firstnode.get_value_in_node() < secondnode.get_value_in_node():
            firstnode.get_children().append(secondnode)
            secondnode.parent = firstnode
            return firstnode
        else:
            secondnode.get_children().append(firstnode)
            firstnode.parent = secondnode
            return secondnode
    
    def set_min(self):
        valid_roots = [r for r in self.roots if r.get_value_in_node() is not None]
        if not valid_roots:
            self.min = None
            return None
        minroot = valid_roots[0]
        for root in valid_roots:
            if root.get_value_in_node() < minroot.get_value_in_node():
                minroot = root
        self.min = minroot
        return minroot

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
