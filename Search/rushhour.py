#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################
class vehicle:
    def __init__(self,  vehicle_properties_list):
        self.name = vehicle_properties_list[0]
        self.loc = vehicle_properties_list[1]
        self.length = vehicle_properties_list[2]
        self.is_horizontal = vehicle_properties_list[3]
        self.is_goal = vehicle_properties_list[4]
    
    def move_forward(self, board_size):
        '''
        move a vehicle forward, ignore potential blocks
        '''
        
        self.loc = self.possible_moves(board_size)[0][0]
    
    def move_backward(self, board_size):
        '''
        move a vehicle backward, ignore potential blocks
        '''
        
        self.loc = self.possible_moves(board_size)[1][0]
    
    def possible_moves(self, board_size):
        '''
        return possible forward/ backward moves(new loc) of a vehicle
        '''
        
        col = board_size[0]
        row = board_size[1]
        if self.is_horizontal:
            new_loc1 = ((self.loc[0] + 1) % col, self.loc[1])
            new_loc2 = ((self.loc[0] - 1) % col, self.loc[1])
            possible_move_backward = (new_loc1, 'E')
            possible_move_forward = (new_loc2, 'W')
        else:
            new_loc1 = (self.loc[0], (self.loc[1] + 1) % row)
            new_loc2 = (self.loc[0], (self.loc[1] - 1) % row)
            possible_move_backward = (new_loc1, 'S')
            possible_move_forward = (new_loc2, 'N')
        
        return (possible_move_forward, possible_move_backward)
            
    def actual_moves(self, board_size, occupied_dict):
        '''
        return actual forward / backward moves a vehicle can move, None if there is a block
        '''
        possible_move_forward, possible_move_backward = self.possible_moves(board_size)
        # check if possbile moves are blocked by other vehicles
        head = possible_move_forward[0]
        if head in occupied_dict and self.name != occupied_dict[head]:
            possible_move_forward = None
        
        # need to deal with tail when moving backwards
        tail = self.get_tail_loc(board_size, possible_move_backward[0])
        if  tail in occupied_dict and self.name != occupied_dict[tail]:
            possible_move_backward = None

        return possible_move_forward, possible_move_backward
    
    def get_tail_loc(self, board_size, loc = None):
        ''' return tail location '''
        
        col = board_size[0]
        row = board_size[1]
        if loc == None:
            loc = self.loc
        if self.is_horizontal:
            tail = ((loc[0]+self.length - 1) % col, loc[1])
        else:
            tail = (loc[0], (loc[1] +self.length - 1) % row)
        return tail

    def occupied_space(self, board_size):
        '''
        return spaces a vehicle occupied as a list of (x,y)
        '''
        
        col = board_size[0]
        row = board_size[1]
        
        loc_list = []
        for i in range(self.length):
            if self.is_horizontal:
                loc_list.append(((self.loc[0] + i) % col, self.loc[1]))
            else:
                loc_list.append((self.loc[0], (self.loc[1] + i) % row))
        return loc_list
    
    def toList(self):
        '''
        return vehicle properties as a list
        '''
        
        return [self.name, self.loc, self.length, self.is_horizontal, self.is_goal]
        
class rushhour(StateSpace):
    def __init__(self, action, gval, parent, vehicle_list, board_properties):
#IMPLEMENT
        """Initialize a rushhour search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.vehicle_list = vehicle_list
        self.board_properties = board_properties

    def successors(self):
#IMPLEMENT
        '''Return list of rushhour objects that are the successors of the current object'''
        States = list()
        board_size = self.board_properties[0]
        occupied_dict =  {}
        # store all vehicles' occupied spaces as a dictionary
        for i in range(len(self.vehicle_list)):
            vehicle_i = vehicle(self.vehicle_list[i])
            loc_list = vehicle_i.occupied_space(board_size)
            for loc in loc_list:
                occupied_dict[loc] = vehicle_i.name
        
        for i in range(len(self.vehicle_list)):
            vehicle_i = vehicle(self.vehicle_list[i])
            actual_move_forward, actual_move_backward = vehicle_i.actual_moves(board_size, occupied_dict)
            for actual_move in (actual_move_forward, actual_move_backward):
                if actual_move != None:
                    action = 'move_vehicle('+vehicle_i.name+','+actual_move[1] + ')'
                    vehicle_i.loc = actual_move[0]
                    new_vehicle_list = self.vehicle_list[:]
                    new_vehicle_list[i] = vehicle_i.toList()
                    new_rushhour = rushhour(action, self.gval+1, self, new_vehicle_list, self.board_properties)
                    States.append(new_rushhour)
        return States
            
            
    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        
        return tuple(tuple(x) for x in self.vehicle_list)
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
#IMPLEMENT
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        
        return self.vehicle_list
        
    def get_board_properties(self):
#IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        
        return self.board_properties

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
#IMPLEMENT
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    
    gv = find_goal_vehicle(state)
    move_forward_gv = vehicle(gv.toList())
    move_backward_gv = vehicle(gv.toList())
    move_forward_count = 0
    move_backward_count = 0
    board_size = state.get_board_properties()[0]
    goal_entrance = state.get_board_properties()[1]
    goal_direction = state.get_board_properties()[2]
    
    # goal vehicle can never reach goal state thus return -1
    if rushhour_goal_gv(gv, board_size, goal_entrance, goal_direction) == -1:
        return -1
    
    while (not rushhour_goal_gv(move_forward_gv, board_size, goal_entrance, goal_direction)):
        move_forward_count += 1
        move_forward_gv.move_forward(board_size)
    
    while (not rushhour_goal_gv(move_backward_gv, board_size, goal_entrance, goal_direction)):
        move_backward_count += 1
        move_backward_gv.move_backward(board_size)
    
    return min(move_forward_count, move_backward_count)

def find_goal_vehicle(state):
    '''
    return goal vehile of the state
    '''
    
    gv = None
    for i in range(len(state.vehicle_list)):
        vehicle_i = vehicle(state.vehicle_list[i])
        if vehicle_i.is_goal:
            gv = vehicle_i
            break
    return gv
    
def rushhour_goal_fn(state):
#IMPLEMENT
    '''Have we reached a goal state'''
    
    board_size = state.get_board_properties()[0]
    goal_entrance = state.get_board_properties()[1]
    goal_direction = state.get_board_properties()[2]
    gv = find_goal_vehicle(state)
    result = rushhour_goal_gv(gv, board_size, goal_entrance, goal_direction)
    if result == -1:
        return False
    return result

def rushhour_goal_gv(gv, board_size, goal_entrance, goal_direction):
    '''
    check if goal vehicle's head or tail matches the goal entrance based on goal's orientation. 
    return -1 if gv is None or gv can never get to goal entrance    
    '''
    # cannot find goal vechicle    
    if gv == None:
        return -1
    
    if gv.is_horizontal and (goal_direction == 'E' or goal_direction == 'W'):
        # check if in same row
        if gv.loc[1] != goal_entrance[1]:
            return -1
        if goal_direction == 'W': 
            return gv.loc == goal_entrance
        else: 
            return gv.get_tail_loc(board_size) == goal_entrance
    elif (not gv.is_horizontal) and (goal_direction == 'N' or goal_direction == 'S'):
        # check if in same col
        if gv.loc[0] != goal_entrance[0]:
            return -1
        if goal_direction == 'N': 
            return gv.loc == goal_entrance
        else:
            return gv.get_tail_loc(board_size) == goal_entrance
    else:
        return -1

def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
#IMPLEMENT
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    
    state_gval = 0
    state_parent = None
    state_action = 'START'
    board_properties = (board_size, goal_entrance, goal_direction)
    state = rushhour(state_action, state_gval, state_parent, vehicle_list, board_properties)
    return state

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)
