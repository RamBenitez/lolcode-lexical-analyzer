# File node.py

# This module defines the Node class used to represent elements
#of the LOLCODE syntax tree (parse tree).

class Node:

    #initializes a node instance
    def __init__(self, type, value=None, children=None):
        self.type = type  # The role of this node.
        self.value = value # The literal value or identifier 
        self.children = children or []  #
    
    #append new child node to the nodes list of children
    def add_child(self, node):
        self.children.append(node)
    
    #returns a string rep of the noe and subtrees
    def __repr__(self, level=0):
        indent = "│   " * level
        #begin with the current type
        ret = f"{indent}├── {self.type}"

        if self.value is not None:
            ret += f":{self.value}"

        #add a newline for readaility
        ret += "\n"

        #recursively add children
        for child in self.children:
            ret += child.__repr__(level + 1)

        return ret



