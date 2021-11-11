# read dimacs input

# encode sudoku rules as clauses in DIMACS

# inplement david putnam v3
# look at the variations sections

import random
import numpy as np
# tree



class Node:
    def __init__(self, parent, literal, bool=-1):
        self.parent = parent
        self.children = {'L':None, 'R':None}
        self.literal = literal
        self.bool = -1  # -1 for false, 1 for true
    

class Tree:
    def __init__(self, root, available_literals):
        self.root = root  
        self.current_node = root
        self.literals = [] # gives the treenodes as a list of literals (-) is false (+) is True
        self.available_literals = available_literals

    def add_node(self):
        # chose random literal
        literal = random.choice(self.available_literals)
        self.available_literals.remove(literal)
        next_node = Node(self.current_node, literal, bool=-1)
        self.literals.append(next_node.bool * next_node.literal)
        print("literals after node added", self.literals)
        return self.literals

    def back_prop(self):
        self.current_node = self.current_node.parent
        if all(val !=None for x in current_node.children.values()): # if there is no free node, backprop again recursively
            back_prop()
            return

        for key in current_node.children:
            if current_node.children[key] == None:  # if one is none, add node and traverse
                current_node.children[key] = add_node(node)
                if key == 'L': # set current bool to negative
                   current_node.bool = -1
                if key == 'R': # set current bool to positive
                    current_node.bool = 1
                return

    def traverse(self):
        pass

# algo 
clauses =  [[1, 2, 3], [1, -2], [-1, 3]]

1 2 3 0
1 -2 0
-1 3



literals = [1, 2, 3] # a list containing all the literals as positive values, 


# depth first search 
# pick rootnode and assign false
root = Node(random.choice(literals), False)
tree = Tree(root, literals)

def check_SAT(literals):
    print("clauses", clauses)
    print("literals", literals)
    '''returns true if satisfied, else false'''
    for clause in clauses:
        # 3 parts of logic, returns true if one literal occurs in clause, 0 or more returns false
        if np.sum(literals == clause) == 0: # another node needs to be constructed
            return 2
        if np.sum(literals == clause) != 1:
            return 0
    return 1

sat = check_SAT(tree.literals)

while sat != 1:
    print('loop')
    sat = check_SAT(tree.literals)
    if sat == 2: # add node
        print("add_node")
        tree.add_node()

    elif sat == 0:
        print("backprop")
        tree.back_prop()
        
    elif sat == 1:
        print("satisfied")

