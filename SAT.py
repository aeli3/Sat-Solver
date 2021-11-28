import random
import csv
import re
import sys
import numpy as np
from collections import defaultdict

def parse_dimacs(file):
    with open(file, 'r') as f:
        clauses = [lines.split()[:-1] for lines in f][1:]
        clauses = [ list(np.array(clause, dtype=int)) for clause in clauses]
    return clauses

def output_dimacs(filename, solution):
    with open(f'{filename}.out', 'w', newline='') as f:
        filewriter = csv.writer(f, delimiter=" ")
        filewriter.writerow(['p', 'cnf', len(solution), len(solution)])
        for literal in solution:
            filewriter.writerow([literal[0], 0])
    f.close()   
    return

def next_literal(f, assignment, literals, heuristic='random'):
    if heuristic == 'random':
        return random.choice(np.setdiff1d(literals, [[abs(x[0])] for x in assignment]))
    
    if heuristic == 'jw':                
        jw_values = []
        jw = 0
        free_literals = np.setdiff1d(literals, [[abs(x[0])] for x in assignment])
        for literal in free_literals: # loop over the literals
            # for each clause 
            for clause in f:
                if literal in clause:
                    jw += 2.**(-len(clause)) # append jw formula
            jw_values.append(jw)
            jw = 0
        # return the literal with heighest jw value
        return free_literals[np.argmax(np.array(jw_values))]
    
    if heuristic == 'rc':
        free_literals = np.setdiff1d(literals, [[abs(x[0])] for x in assignment])
        literal_dct = defaultdict(int)
        row_dct = defaultdict(int)
        col_dct = defaultdict(int)
        for literal in free_literals:
            row_dct[int(str(literal)[0])] += 1
            col_dct[int(str(literal)[1])] += 1
        for literal in free_literals:
            literal_dct[literal] = row_dct[int(str(literal)[0])] + col_dct[int(str(literal)[1])]

        return min(literal_dct, key=literal_dct.get)

def propagate(f, unit_clause):
    modified = []
    for clause in f:
        if unit_clause in clause:
            continue
        if -unit_clause in clause:
            new_clause = [x for x in clause if x != -unit_clause]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified

def unit_propagation(f):
    assignment = []
    unit_clauses = []  
    unit_clauses = [clause for clause in f if len(clause) == 1]
    while len(unit_clauses) > 0:
        unit_clause = unit_clauses[0]
        f = propagate(f, unit_clause[0])
        assignment += [[unit_clause[0]]]
        if f == -1:
            return -1, []
        if not f:
            return f, assignment
        unit_clauses = [clause for clause in f if len(clause) == 1]
    return f, assignment

def backtracking(formula, assignment, literals, heuristic):
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment 
    if formula == - 1:
        return []
    if not formula:
        return assignment
    variable = next_literal(formula, assignment, literals, heuristic)
    solution = backtracking(propagate(formula, variable), assignment + [[variable]], literals, heuristic)
    if not solution:
        solution = backtracking(propagate(formula, -variable), assignment + [[-variable]], literals, heuristic)
        
    return solution

if __name__ == '__main__':
    # initialize comandline arguments
    heuristics = ['random','jw','rc']
    heuristic = 'random'
    input_file = False
    if len(sys.argv) > 1:
        heuristic = heuristics[int(re.findall(r'\d+', sys.argv[1])[0]) - 1]
        if len(sys.argv) > 2:
                input_file = sys.argv[2]
        else:
            print('No input file detected!')
    
    # run when inputs detected
    if heuristic and input_file:
        clauses = parse_dimacs(input_file)
        literals = [[x+y+z] for x in range(100,1000, 100) for y in range(10,100,10) for z in range(1,10)]
        solution = backtracking(clauses, [], literals, heuristic)
        output_dimacs(input_file, solution)