#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools

def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))


    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------------------
    | > |2| |9| | |6| |
    | |4| | | |1| | |8|
    | |7| <4|2| | | |3|
    |5| | | | | |3| | |
    | | |1| |6| |5| | |
    | | <3| | | | | |6|
    |1| | | |5|7| |4| |
    |6> | |9| < | |2| |
    | |2| | |8| <1| | |
    -------------------
    would be represented by the list of lists

    [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',4,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [6,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]


    This routine returns Model_1 which consists of a variable for each cell of
    the board, with domain equal to [1,...,n] if the board has a 0 at that
    position, and domain equal [i] if the board has a fixed number i at that
    cell.

    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between all relevant
    variables (e.g., all pairs of variables in the same row, etc.).

    All of the constraints of Model_1 MUST BE binary constraints (i.e.,
    constraints whose scope includes two and only two variables).
    '''
    
    n = len(initial_futoshiki_board)
    if n <= 1 or len(initial_futoshiki_board[0]) == 0:
        return None, []
        
    variables_list = []
    domain = [i for i in range(1,n+1)]
    csp = CSP('futoshiki_csp_model_1')
    for i in range(n):
        variables = [0]*n
        inequality_pos = []
        k = 0
        for j in range(len(initial_futoshiki_board[0])):
            val = initial_futoshiki_board[i][j]
            name = str(tuple((i,j-k)))
            if type(val) == str:
                if val == '<' or val == '>':
                    inequality_pos.append((j-k, j+1-k, val))
            else:
                newVar = Variable(name, domain)
                if val <=n and val >= 1:
                    newVar= Variable(name, [val])
                variables[j-k] = newVar
                csp.add_var(newVar)
                k = k + 1
        for pos in inequality_pos:
            variable1 = variables[pos[0]]
            variable2 = variables[pos[1]]
            cons = construct_constraint(variable1, variable2, pos[2])
            csp.add_constraint(cons)
        # add row distct constraint
        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                cons = construct_constraint(variables[i], variables[j], '!=')
                csp.add_constraint(cons)
                    
        variables_list.append(variables)
    
    # add col distict constriant
    for i in range(len(variables_list)):
        col_variables = []
        for j in range(len(variables_list[0])):
            col_variables.append(variables_list[j][i])
        for i in range(len(col_variables)):
            for j in range(i+1, len(col_variables)):
                cons = construct_constraint(col_variables[i], col_variables[j], '!=')
                csp.add_constraint(cons)
    
    return csp, variables_list
    
    
def construct_constraint(variable1, variable2, symbol):
    name = variable1.name + symbol + variable2.name
    sati_tuples = []
    # can optimize
    for val1 in variable1.domain():
        for val2 in variable2.domain():
            if [val1, val2] not in sati_tuples:
                if symbol == '<':
                    if val1 < val2:
                        sati_tuples.append([val1, val2])
                elif symbol == '>':
                    if val1 > val2:
                        sati_tuples.append([val1, val2])
                elif symbol == '!=':
                    if val1 != val2:
                        sati_tuples.append([val1, val2])

    cons = Constraint(name, [variable1, variable2])
    cons.add_satisfying_tuples(sati_tuples)

    return cons
            
#IMPLEMENT

##############################

def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))

    The input board takes the same input format (a list of n lists of size 2n-1
    specifying the board) as futoshiki_csp_model_1.

    The variables of Model_2 are the same as for Model_1: a variable for each
    cell of the board, with domain equal to [1,...,n] if the board has a 0 at
    that position, and domain equal [n] if the board has a fixed number i at
    that cell.

    However, Model_2 has different constraints. In particular, instead of
    binary non-equals constaints Model_2 has 2*n all-different constraints:
    all-different constraints for the variables in each of the n rows, and n
    columns. Each of these constraints is over n-variables (some of these
    variables will have a single value in their domain). Model_2 should create
    these all-different constraints between the relevant variables, and then
    separately generate the appropriate binary inequality constraints as
    required by the board. There should be j of these constraints, where j is
    the number of inequality symbols found on the board.  
    '''
    n = len(initial_futoshiki_board)
    if n <= 1 or len(initial_futoshiki_board[0]) == 0:
        return None, []
        
    variables_list = []
    domain = [i for i in range(1,n+1)]
    csp = CSP('futoshiki_csp_model_2')
    for i in range(n):
        variables = [0]*n
        inequality_pos = []
        k = 0
        for j in range(len(initial_futoshiki_board[0])):
            val = initial_futoshiki_board[i][j]
            name = str(tuple((i,j-k)))
            if type(val) == str:
                if val == '<' or val == '>':
                    inequality_pos.append((j-k, j+1-k, val))
            else:
                newVar = Variable(name, domain)
                if val <=n and val >= 1:
                    newVar= Variable(name, [val])
                variables[j-k] = newVar
                csp.add_var(newVar)
                k = k + 1
        for pos in inequality_pos:
            variable1 = variables[pos[0]]
            variable2 = variables[pos[1]]
            cons = construct_constraint(variable1, variable2, pos[2])
            csp.add_constraint(cons)
        # add row distct constraint
        cons = construct_constraint_by_list(variables, n)
        csp.add_constraint(cons)
                    
        variables_list.append(variables)
    
    # add col distict constriant
    for i in range(len(variables_list)):
        col_variables = []
        for j in range(len(variables_list[0])):
            col_variables.append(variables_list[j][i])
        cons = construct_constraint_by_list(col_variables, n)
        csp.add_constraint(cons)
    
    return csp, variables_list


#IMPLEMENT
def construct_constraint_by_list(variables, n):

    name = str(variables) + '!='
    constraint = Constraint(name, variables)
    permu_domain = [i for i in range(1, n+1)]
    preAssigned_index = []
    for i in range(len(variables)):
        var = variables[i]
        if len(var.domain()) == 1:
            preAssigned_index.append(i)
            permu_domain.remove(var.domain()[0])
    sati_tuples = []
    for permu in itertools.permutations(permu_domain):
        permu_list = list(permu)
        for i in preAssigned_index:
            permu_list.insert(i, variables[i].domain()[0])
        
        sati_tuples.append(permu_list)


    constraint.add_satisfying_tuples(sati_tuples)
    return constraint

    
    
