#!/usr/bin/python

import copy
import itertools

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())
        print assignment
        # Call backtrack with the partial assignment 'assignment'
        #return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        # TODO: IMPLEMENT THIS

        #Check if assignment is complete: -> check if all elements in assigment
        # is of length 1.
        '''
        if assignment_is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        # order the values in var by how few values they rule out for the others.
        var = self.order_domain_values(var, assignment)
        for value in var:
            if value is consistent with assignemnt:
                add {var = value} to assignemnt
                inferences = self.inference(assignment, queue)
                if inferences fail:
                    add inferences to assignment
                    result = self.backtrack(assignment)
                    if result fails:
                        return result
            remove {var = value} and inferences from assignment
        return False
        '''
        pass

    def assigment_is_complete(assignment):
        for i in assignment:
            if len(i) != 1:
                return False
        return True
        
    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # TODO: IMPLEMENT THIS
        # Chose the one that has the fewest legal actions
        # return the key name that has the shortest list of legal actions 
        # Special case for the first choice?
        # Tie breaker: If we have a tie in the fewest legal actions, pick the one with the most constraints

        #Pseudocode
        #Sort the list from least elements to most
        #If there are more than one variable with the least amount:
        #   return the one with the longest constraint-list
        #else:
        #   return the variable with the least amount
        pass

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        # TODO: IMPLEMENT THIS
        while len(queue):
            (i,j) = queue.pop()
            print 'Checking arc-consistency of {} and {}'.format(i,j)            
            if self.revise(assignment, i, j):
                print 'Did some revising'
                if len(assignment.domains[i]) == 0:
                    return False
                for k in assigment.constraints[i] - j :
                    print 'Adding the arc ({},{}) to the queue'.format(k, i)
                    queue.append((k,i))
            else:
                print 'No need to revise this'    
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        # TODO: IMPLEMENT THIS
        revised = False
        toBeRemoved = []
        for value_i in assignment[i]:
            satisfies_constraint = False
            for value_j in assignment[j]:
                if (value_i, value_j) in self.constraints[i][j]:
                    print '({},{}) exists in constraints'.format(value_i, value_j)
                    satisfies_constraint = True
            if not satisfies_constraint:
                toBeRemoved.append(value_i)
                revised = True
        for value in toBeRemoved:
            assignment[i].remove(value)
        print 'Revised is {}, removed values are: {}'.format(revised, toBeRemoved)
        return revised

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'


if __name__ == '__main__':
    csp = create_map_coloring_csp()
    #csp.inference(csp.domains, csp.get_all_arcs())
    #csp.revise(csp.domains, 'WA', 'SA')
    csp.backtracking_search()
    print len(csp.constraints)






    #    print 'Variables: {}'.format(csp.variables)
#    print 'Domains: {}'.format(csp.domains)
#    print 'Constraints: {}'.format(csp.constraints['WA']['SA'])




'''
    x = {'red', 'woff', 'hei'}
    
    print csp.domains['WA']
    toBeRemoved = []
    for value1 in csp.domains['WA']:
        found = False
        print 'Current value is: {}'.format(value1)
        for value2 in x:
            print 'Checking if ({}, {}) is in WA/SA cons'.format(value1, value2)
            if (value1, value2) in csp.constraints['WA']['SA']:
                print '({},{}) is a legal assignment'.format(value1, value2)
                found = True
        if not found:
            print 'could not find any legal actions with {} and ({})'.format(value1, x)
            print 'Removing value: {}'.format(value1)
            toBeRemoved.append(value1)
    print "To be removed: {}".format(toBeRemoved)
    for v in toBeRemoved:
        csp.domains['WA'].remove(v)
    print csp.domains['WA']

'''


