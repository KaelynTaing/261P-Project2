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
        pass

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
        # be able to reference minnode
        minnode = self.find_min()
        # print(minnode.val)
        # print(minnode.get_children())

        # if it has no children, nothing to merge up
        # merge children to root list
        for child in minnode.get_children():
            print(minnode.get_children())
            # set flags to False
            child.get_flag = False
            self.roots.append(child)

        # remove minnode from roots
        self.roots.remove(minnode)

        # array to hold nodes' number of children
        arr = [None] * (math.ceil(math.log(self.totalNodes)) + 1)

        # merge step between trees
        for root in self.get_roots():
            print(root.get_value_in_node())
            # make index number of children
            idx = len(root.get_children())

            # appendedNode default as root
            appendedNode = root
            while arr[idx] is not None:
                # combine root at that arr[idx] and this root and check again
                if appendedNode.get_value_in_node() < arr[idx].get_value_in_node():
                    appendedNode = root
                    # make root child of arr[idx]
                    arr[idx].get_children().append(root)
                else:
                    appendedNode = arr[idx]
                    # make arr[idx] child of root
                    root.get_children().append(arr[idx])

                # set combined to correct idx based off root
                # remove node at this current index
                arr[idx] = None
                # update idx
                idx = len(appendedNode.get_children())
                # set new tree to that point in the array, if its None, if not go back in this while loop
                arr[idx] = appendedNode

            # arr[idx] = appendedNode

        for a in arr:
            if a is not None:
                print("check")
                print(a.get_value_in_node())

        # set min
        minroot = self.get_roots()[0]
        for root in self.get_roots():
            if root.get_value_in_node() < minroot.get_value_in_node():
                minroot = root
        self.min = minroot
        # set new pointer for min to roots?

    def find_min(self) -> FibNode:
        # minroot = self.roots[0]
        # for root in self.roots:
        #     if minroot.get_value_in_node() >= root.get_value_in_node():
        #         minroot = root

        # return minroot
        return self.min

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        # make sure node is a root node
        if node.get_children == []:
            node.get_value_in_node = new_val
        else:
            parentnode = node.parent
            while parentnode not in self.get_roots:
                if parentnode.get_flag is False:
                    parentnode.get_flag = True
                else:
                    grandparentnode = parentnode.parent
                    parentnode.insert(parentnode.get_value_in_node)
                    parentnode = grandparentnode

            # move node up
            node.insert(new_val)

        # also have to update min here

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
