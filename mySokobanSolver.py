'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and triggers to a fail for the test of your code.

# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search
import time
import sokoban

#  Global Variables - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MOVEMENTS = {"Up": (0, -1),
             "Down": (0, 1),
             "Right": (1, 0),
             "Left": (-1, 0)}

# Placeholder to hold taboo coords
taboo = []

def to_position(elem, direction):
    return elem[0] + MOVEMENTS[direction][0], elem[1] + MOVEMENTS[direction][1]

def from_position(elem, direction):
    return elem[0] - MOVEMENTS[direction][0], elem[1] - MOVEMENTS[direction][1]

def flip_cords_in_macro_solution(solution):
    # Flips x,y in a macro solution so that it becomes row column
    newSolution = []
    for action in solution:
        newSolution.append(((action[0][1],action[0][0]),action[1]))
    return newSolution

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(9945008, 'Cody', 'Cripps'), (10283391, 'Faith', 'Lim'), (10411551, 'Mai', 'Bernt')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse, returnAsList=False):
    '''
    Identify the taboo cells of a warehouse. A cell inside a warehouse is
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle
    becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target,
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a
             wall are taboo if none of these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with
       an '#' and the taboo cells marked with an 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''
    # Identify taboo cells via rule 1:

    # Work out if a wall is a corner
    def corner(coord):
        x = coord[0]
        y = coord[1]
        # Hemmed by walls top and left
        if ((x - 1, y) in warehouse.walls and (x, y - 1) in warehouse.walls):
            return True

        # Hemmed by walls top and right
        if ((x + 1, y) in warehouse.walls and (x, y - 1) in warehouse.walls):
            return True

        # Hemmed by walls bottom and left
        if ((x - 1, y) in warehouse.walls and (x, y + 1) in warehouse.walls):
            return True

        # Hemmed by walls bottom and right
        if ((x + 1, y) in warehouse.walls and (x, y + 1) in warehouse.walls):
            return True

        return False

    # Put warehouse into a list by \n
    warehouseinlines = str(warehouse).split("\n")
    # Create a coordinate list of empty space cells
    emptyspace = list(sokoban.find_2D_iterator(warehouseinlines, " "))

    # Remove coordinates outside the maze from the empty space list
    i = 0
    while i < len(emptyspace):
        coord = emptyspace[i]
        if not can_go_there(warehouse, emptyspace[i], True, True):
            emptyspace.remove(coord)
            i -= 1
        i += 1



    for i in emptyspace:
        if corner(i) and i not in warehouse.targets:
            taboo.append(i)

    # Identify taboo cells via rule 2:
    rule2taboos = []
    for i in taboo:
        x = i[0]
        y = i[1]
        x_original = x
        y_original = y

        # Check each tile at a time to see if it is a target.
        # If it is not and has a wall behind it mark potential taboo.

        # Check x right direction
        x += 1  # So as to not check the same tile again
        potentialtaboos = []
        while (x, y) in emptyspace:
            # Check if there is a wall on top or beneath
            if (x, y - 1) in warehouse.walls or (x, y + 1) in warehouse.walls:
                potentialtaboos.append((x, y))
            else:
                break

            if corner((x, y)) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []

            x += 1

        # Check x left direction
        x = x_original - 1
        potentialtaboos = []
        while (x, y) in emptyspace:
            # Check if there is a wall on top or beneath
            if (x, y - 1) in warehouse.walls or (x, y + 1) in warehouse.walls:
                potentialtaboos.append((x, y))
            else:
                break

            if corner((x, y)) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []

            x -= 1

        # Check y down direction
        x = x_original
        y = y_original + 1
        potentialtaboos = []
        while (x, y) in emptyspace:
            # Check if there is wall to the left or the right
            if (x - 1, y) in warehouse.walls or (x + 1, y) in warehouse.walls:
                potentialtaboos.append((x, y))
            else:
                break

            if corner((x, y)) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []
            y += 1

        # Check y up direction
        y = y_original - 1
        potentialtaboos = []
        while (x, y) in emptyspace:
            # Check if there is wall to the left or the right
            if (x - 1, y) in warehouse.walls or (x + 1, y) in warehouse.walls:
                potentialtaboos.append((x, y))
            else:
                break

            if corner((x, y)) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []
            y -= 1

    taboo.extend(rule2taboos)
    if returnAsList:
        return taboo

    # Finally, make the new string with the taboo tiles marked
    # By using the in built string maker from warehouse
    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)

    vis = [[" "] * x_size for y in range(y_size)]
    for (x, y) in warehouse.walls:
        vis[y][x] = "#"
    for (x, y) in taboo:
        vis[y][x] = "X"


    return "\n".join(["".join(line) for line in vis])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of
    the provided module 'search.py'.

    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro

    When self.allow_taboo_push is set to True, the 'actions' function should
    return all possible legal moves including those that move a box on a taboo
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.

    If self.macro is set True, the 'actions' function should return
    macro actions. If self.macro is set False, the 'actions' function should
    return elementary actions.


    '''

    def __init__(self, warehouse, allow_taboo_push=True,\
         macro=False, verbose=False, alternateGoal=False,\
              goal=None, usingDtransform=False):

        # Initialise SokobanPuzzle Problem
        self.macro = macro
        self.allow_taboo_push = allow_taboo_push
        self.verbose = verbose

        #-- Load Problemspace (Warehouse) --#
        #save initial state
        self.initial = warehouse.copy()

        self.alternateGoal = alternateGoal
        if not alternateGoal:
            self.goal = warehouse.copy()
            self.goal.boxes = self.goal.targets
        else:
            self.goal = warehouse.copy()
            self.goal.worker = goal

        self.usingDtransform = usingDtransform
        if usingDtransform:
            self.dTransform = distanceTransform(warehouse.copy())

        self.original_boxes = warehouse.boxes
        self.original_worker = warehouse.worker

        if not allow_taboo_push:
            self.taboo = taboo_cells(warehouse,returnAsList=True)


    def resultElem(self, state, action):
        new_state = state.copy(boxes=self.original_boxes,worker=self.original_worker)
        # return state with the box and worker moved after action
        new_state = check_and_move(new_state, [action])

        if self.verbose:
            print("    ->Checking action " + str(action))
            print("      -->Result: " + str(new_state))
        return new_state

    def resultMacro(self, state, action):
        '''
        Move boxes based on a macro action

        @param action: a tuple of box location and direction
            in the form ((x,y),"direction")

        @return
            a warehouse object which boxes was moved
        '''
        if self.verbose:
            print("    ->Checking action " + str(action))
            print("      *boxes in locations: " + str(state.boxes))

        new_state = state.copy(boxes=state.boxes.copy())

        box_previous_location = action[0]

        #Remove box from previous location and move the worker there
        new_state.boxes.remove(box_previous_location)
        new_state.worker = box_previous_location

        #Move box into new position
        moveDirection = action[1]
        new_state.boxes.append(to_position(box_previous_location, moveDirection))

        return new_state

    def result(self, state, action):
        # Check which result function to use
        if self.macro:
            return self.resultMacro(state,action)
        else:
            return self.resultElem(state,action)

    def goal_test(self, state):
        """
        Check if the set that is the current box positions, aligns with
            the set that is the boxes in the goal state
        Return True if the sets align (boxes at targets).
        """
        if self.alternateGoal == True:
            return state == self.goal

        return set(self.goal.boxes.copy()) == set(state.boxes.copy())

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def actions(self, state_in):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        state = state_in.copy(boxes = state_in.boxes.copy())
        self.original_boxes = state.boxes.copy()
        self.original_worker = state.worker
        actions = []
        if self.verbose:
            print("For Warehouse:")
            print(state)
        if self.macro:
            for box in state.boxes.copy():
                for movement in MOVEMENTS:
                    # Apply movement to the box
                    next_location = to_position(box, movement)
                    worker_location = from_position(box, movement)

                    # If the worker can get to the location to push the box
                    if not can_go_there(state, worker_location, useXY=True):
                        continue

                    # If taboo cells are not allowed
                    if not self.allow_taboo_push:
                        if next_location in self.taboo:
                            continue
                    # If the next_location results in a wall
                    if next_location in state.walls:
                        continue
                    # If the next_location results in another box
                    if next_location in state.boxes:
                        continue
                    # If no constraints are violated add the box position and the movement to the list
                    actions.append((box, movement))
        else:
            for movement in MOVEMENTS:
                # Apply movement to the worker
                move = to_position(state.worker, movement)
                # If the action results in a wall
                if move in state.walls:
                    continue
                # If the action pushes a box
                if move in state.boxes:
                    # The new position of the box
                    box_movement = to_position(move, movement)

                    if not self.allow_taboo_push:
                        if box_movement in taboo:
                            continue
                    # If the box is pushed into a wall or another box
                    if box_movement in state.walls or box_movement in state.boxes:
                        continue
                # If no constraints are violated add the action to the list
                actions.append(movement)
        if self.verbose:
            print("  ->Actions: " + str(actions))
            print(state)
        return actions


    def h(self, n):
            """
            Heuristic
            """
            if not self.alternateGoal:

                #Check which heuristic to use
                if self.usingDtransform:
                    heur = 0
                    for box in n.state.boxes:
                        #Lookup box in dTransform
                        if box in self.dTransform:
                            heur = heur + self.dTransform[box]
                        else:
                            # If it isn't in the dTransform than give large value as it
                            # is outside of the maze
                            heur = heur + 500
                    return heur

                heur = 0
                for box in n.state.boxes:
                    #Find closest target
                    closest_target = n.state.targets[0]
                    for target in n.state.targets:
                        if (manhatten(target, box) < manhatten(closest_target, box)):
                            closest_target = target

                    #Update Heuristic
                    heur = heur + manhatten(closest_target, box)
                return heur

            # Alternate Heuristic for moving worker
            return manhatten(n.state.worker, self.goal.worker)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def manhatten(p1, p2):
    """
    Computes the manhatten distance between a set of points

    inputs:
        2 locations as tuples

    return:
        Manhatten distance between the input locations
    """
    return abs((p1[0] - p2[0])) + abs((p1[1] - p2[1]))


def distanceTransform(warehouse):
    """
    Computes a manhatten distance transform for a given warehouse

    @param warehouse: a warehouse object

    @return
        a dictionary with keys that are the ground locations in the puzzles,
        who's values are their distance from a goal.
    """
    # Initialise variables
    wh = warehouse.copy()
    walls = wh.walls

    frontier = []
    dtransform = {}
    frontier.extend(wh.targets)

    # Targets have 0 distance to targets
    for target in wh.targets:
        dtransform[target] = 0

    explored = set() # initial empty set of explored states
    while frontier:
        node = frontier.pop()
        # Look in each direction from the current node
        for direction in MOVEMENTS:
            pos = to_position(node, direction)
            # Check if we should give it a distance
            if pos not in walls and\
                pos not in frontier and\
                    pos not in explored:
                # The distance of a point is 1 more than it's parent
                dtransform[pos] = dtransform[node] + 1
                frontier.append(pos)
            # Check if a point needs to be reparented
            if pos in dtransform:
                tempH = dtransform[node] + 1
                if tempH < dtransform[pos]:
                    dtransform[pos] = tempH

        explored.add(node)


    return dtransform



def check_and_move(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not,
    and performs the sequence on the warehouse.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
        Otherwise, the altered warehouse.
    '''
    wh = warehouse.copy(boxes=warehouse.boxes.copy())
    for action in action_seq:
        # Apply given movement to the position of the worker
        move = to_position(wh.worker, action)
        # If the action results in a wall position the action is illegal
        if move in wh.walls:
            return 'Failure'
        # If the action pushes a box
        if move in wh.boxes:
            # The new position of the box
            box_movement = to_position(move, action)
            # If the box is pushed into a wall or another box the action is illegal
            if box_movement in wh.walls or box_movement in wh.boxes:
                return 'Failure'

        # Apply the actions to the wh
        wh.worker = to_position(wh.worker, action)
        # If worker pushes a box
        if wh.worker in wh.boxes:
            # Find the box position, which is the workers current position, and remove it
            wh.boxes.remove(wh.worker)
            # Append its new position
            wh.boxes.append(to_position(wh.worker, action))
    return wh


def check_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    warehouse = check_and_move(warehouse, action_seq)

    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def solve_sokoban_elem_via_macro(warehouse, usingDtransform=True, verbose=False):
    '''
    This function should solve using elementary actions
    the puzzle defined in a file.

    @param warehouse: a valid Warehouse object (from sokoban.py)

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    #Find the macro actions required to solve the puzzle

    if verbose: print('Solving for Macro Action Sequence')
    result = solve_sokoban_macro(warehouse, usingDtransform=usingDtransform,\
        verbose=verbose)

    #Check if Macro Solver deemed the puzzle impossible
    if result == ['Impossible']:
        return ['Impossible']

    macroActions = flip_cords_in_macro_solution(result)


    if verbose: print('Macro Actions Found \n' + str(macroActions))

    #For these macro actions solve for the workers (elementary) movements
    elemActions = []

    for action in macroActions:
        #Push From position is the position the worker needs to be in
        #  to push the box in the desired direction
        pushFrom = from_position(action[0], action[1])

        elemPuzzle = SokobanPuzzle(warehouse, macro=False,alternateGoal=True ,goal=pushFrom)

        if warehouse.worker == pushFrom:
            #move worker in desired direction
            warehouse = check_and_move(warehouse, [action[1]])
        else:
            #move worker to desired location
            res = search.astar_graph_search(elemPuzzle)

            #move worker in desired direction
            warehouse = check_and_move(res.state, [action[1]])
            #update list of required elementary actions
            elemActions.extend(res.solution())

        #update list of required elementary actions
        elemActions.append(action[1])
        if verbose:
            print('\nCompleted the Macro Action' + str(action))
            print(warehouse)
    if verbose:
        print('\n\nFinal Elementary Sequence:')
        print(elemActions)
    return elemActions


def solve_sokoban_elem(warehouse,\
    usingMacro=True, usingDtransform=True, verbose=False):
    '''
    This function should solve using elementary actions
    the puzzle defined in a file.

    @param warehouse: a valid Warehouse object (from sokoban.py)

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    #If @param usingMacro, then pass to via_macro function
    if usingMacro:
        return solve_sokoban_elem_via_macro(warehouse,\
            usingDtransform=usingDtransform, verbose=verbose)

    else:
        #Initialise Puzzle
        puzzle = SokobanPuzzle(warehouse, verbose=verbose)
        puzzle.macro = False

        #Find Solution
        result = search.astar_graph_search(puzzle)
        t1 = time.time()
        print ('The Elementary Solve took {:.6f} seconds'.format(t1-t0))

        if result:
            print("Start State: \n" + str(warehouse))
            print("Result State: \n" + str(result.state))
            return result.solution()
        else:
            return ['Impossible']


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst, useXY=False, ignoreBoxes=False):
    '''
    Determine whether the worker can walk to the cell dst=(row,column)
    without pushing any box.
    @param warehouse: a valid Warehouse object (from sokoban.py)
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    # Check if using (Row, Column) input, convert to (x, y)
    if not useXY:
        dst = (dst[1],dst[0])
    wh = warehouse.copy()
    walls = wh.walls
    boxes = wh.boxes.copy()
    # So we can use this function as an in maze checker as well
    if ignoreBoxes:
        boxes = []
    worker = wh.worker
    explored = []

    fullyexplored=False

    explored.append(worker)

    # Keep checking the 4 squares around tile in question, if you can go to them,
    # add to explored. Keep going back to explored and doing the test on each one of them.
    def explore(coord):
        x = coord[0]
        y = coord[1]

        for direction in MOVEMENTS:
            pos = (x + MOVEMENTS[direction][0],y + MOVEMENTS[direction][1])
            if (pos not in walls and\
                pos not in boxes and\
                    pos not in explored):

                explored.append(pos)

    # While its not the tile we're looking for or we've explored every single tile.
    while not fullyexplored:
        lengthofexplored=len(explored)
        for i in explored:
            explore(i)
            if dst in explored:
                return True
            # If explored hasn't grown, it means there is no where else to explore
            # Meaning it's fully explored
            if lengthofexplored==len(explored):
                fullyexplored=True

    return False


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse, usingDtransform=True, verbose=False):
    '''
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ]
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    t0 = time.time()
    puzzle = SokobanPuzzle(warehouse, verbose=verbose, allow_taboo_push=False,\
        usingDtransform=usingDtransform)
    puzzle.macro = True


    result = search.astar_graph_search(puzzle)
    t1 = time.time()
    print ('The Macro Solve took {:.6f} seconds'.format(t1-t0))

    if result:
        print("Start State: \n" + str(puzzle.initial))
        print("Result State: \n" + str(result.state))
        return flip_cords_in_macro_solution(result.solution())
    else:
        return ['Impossible']


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from sokoban import Warehouse

if __name__ == "__main__":
    wh=Warehouse()
    wh.load_warehouse("./warehouses/warehouse_19.txt")

    tabooC = taboo_cells(wh)

    print(solve_sokoban_elem(wh, usingMacro=True))
