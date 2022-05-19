#!/usr/bin/python3
"""
Linked list in python
"""

class Linked_list():
    """
    Class to define the linked list
    """

    def __init__(self):
        """Initialize the linked list"""
        self.head_node = None
    
    def print_list(self):
        """Print values of the linked list"""
        traverse = self.head_node
        while traverse:
            print(traverse.value)
            traverse = traverse.next_node

    def list_len(self):
        """Get length of a linked list"""
        i = 0
        traverse = self.head_node
        while traverse:
            i += 1
            traverse = traverse.next_node
        return i

    def add_node(self, index, value=None):
        """Add a node to a linked list"""
        if index < 0:
            print("Invalid index")
        if index == 0:
            new_node = Node(value)
            new_node.next_node = self.head_node
            self.head_node = new_node
        else:
            i = 0
            traverse = self.head_node
            while traverse:
                if i == index - 1:
                    new_node = Node(value)
                    temp = traverse.next_node
                    traverse.next_node = new_node
                    new_node.next_node = temp
                    return
                traverse = traverse.next_node
                i += 1
            print("Invalid index")

    def del_node(self, index):
        """Delete a node"""
        if index < 0:
            return "invalid index"
        traverse = self.head_node
        i = 0
        while traverse:
            if i == index - 1:
                new_next = traverse.next_node.next_node
                traverse.next_node = new_next

class Node():
    """
    Class to define a node in the linked list
    """

    def __init__(self, value):
        self.value = value
        self.next_node = None

list_a = Linked_list()
node_a = Node(1)
node_b = Node(2)
node_c = Node(3)
list_a.head_node = node_a
node_a.next_node = node_b
node_b.next_node = node_c
list_a.add_node(list_a.list_len() + 1, "mid")
list_a.print_list()