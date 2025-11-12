"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """


    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        #Dictionary for variable assignments
        assignments = {}

        #Copy of the list of clauses
        clauses_copy = [clause[:] for clause in clauses]

        #Loop flag
        changed = True

        while changed:
            changed = False
            #Look for unit clauses
            for clause in clauses_copy:
                if len(clause) == 1:
                    literal = clause[0]
                    variable = abs(literal)
                
                if variable not in assignments:
                    assignments[variable] = (literal > 0)
                    changed = True
            
            #Simplify other clauses based on current assignments
            new_clauses = []
            for clause in clauses_copy:
                is_satisfied = False
                new_clause = []

                for literal in clause:
                    variable = abs(literal)
                    if variable in assignments:
                        if (literal > 0 and assignments[variable]) or (literal < 0 and not assignments[variable]):
                            is_satisfied = True
                            break
                    else:
                        new_clause.append(literal)

                if not is_satisfied:
                    #Empty clause means all literals were false
                    if not new_clause:
                        return False, {}
                    new_clauses.append(new_clause)

            #Update the clauses
            clauses_copy = new_clauses

        #If no clauses remain, everything is satisfied
        if not clauses_copy:
            return True, assignments
        
        #Find the first unassigned variable for branching
        unassigned = None
        for i in range(1, n_vars+1):
            if i not in assignments:
                unassigned = i
                break

        #Try assigning true to the variable
        satisfiable, assignment = self.sat_backtracking(n_vars, clauses_copy + [[unassigned]])
        if satisfiable:
            return True, assignment
        
        #Try false if True does not work
        return self.sat_backtracking(n_vars, clauses_copy + [[-unassigned]])
        


            

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass