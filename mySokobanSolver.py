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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(9945008, 'Cody', 'Cripps'), (10283391, 'Faith', 'Lim'), (10411551, 'Mai', 'Bernt')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
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
    # Placeholder to hold taboo coords
    taboo = []

    # Work out warehouse limits
    X, Y = zip(*warehouse.walls)
    height = max(Y) - min(Y)+1
    width = max(X) - min(X)+1

    # Identify taboo cells via rule 1:
    # Rule 1: if a cell is a corner inside the warehouse and not a target,
    # then it is a taboo cell.

    # Work out if a wall is a corner
    def itsacorner(coord, warehouse):
        # its a corner if it is in walls and
        # there are walls to the top left, top right, bottom left,
        # or bottom right of this cell

        # x+1, y+1 bottom right
        # Condition if its a corner
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

    def inmaze(coord, warehouse):
        xoriginal = coord[0]
        yoriginal = coord[1]
        right = False
        left = False
        top = False
        bottom = False
        x = xoriginal+1
        y = yoriginal
        # Check right
        while x < width:
            if (x, y) in warehouse.walls:
                right = True
                break
            x += 1
        # Check left
        x = xoriginal-1
        while x > -1:
            if (x, y) in warehouse.walls:
                left = True
                break
            x -= 1

        y = yoriginal+1
        x = xoriginal
        # Check top
        while y < height:
            if (x, y) in warehouse.walls:
                top = True
                break
            y += 1
        # Check bottom
        y = yoriginal-1
        x = xoriginal
        while y > -1:
            if (x, y) in warehouse.walls:
                bottom = True
                break
            y -= 1

        return left and right and top and bottom

    for i in emptyspace:
        if itsacorner(i, warehouse) and i not in warehouse.targets and inmaze(i, warehouse):
            taboo.append(i)

    # Identify taboo cells via rule 2:
    # Rule 2: all the cells between two corners inside the warehouse along a
    # wall are taboo if none of these cells is a target.

    # Right now taboo only contains corners
    rule2taboos = []
    for i in taboo:
        x = i[0]
        y = i[1]
        xoriginal = x
        yoriginal = y

        # New plan, check each tile at a time if it is a target. If it is not and has a wall behind it
        # mark potential taboo, move to next tile.
        # Check x right direction
        x += 1  # So as to not check the same tile again
        potentialtaboos = []
        while (x, y) not in warehouse.walls and (x, y) not in warehouse.targets and (x, y) in emptyspace:
            # Check if there is a wall on top or beneath
            if (x, y - 1) in warehouse.walls or (x, y + 1) in warehouse.walls:
                potentialtaboos.append((x, y))

            if itsacorner((x, y), warehouse) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []

            x += 1

        # Check x left direction
        x = xoriginal - 1
        potentialtaboos = []
        while (x, y) not in warehouse.walls and (x, y) not in warehouse.targets and (
                x, y) in emptyspace:
            # Check if there is a wall on top or beneath
            if (x, y - 1) in warehouse.walls or (x, y + 1) in warehouse.walls:
                potentialtaboos.append((x, y))

            if itsacorner((x, y), warehouse) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []

            x -= 1

        # Check y down direction
        x = xoriginal
        y = yoriginal + 1
        potentialtaboos = []
        while (x, y) not in warehouse.walls and (x, y) not in warehouse.targets and (x, y) in emptyspace:
            # Check if there is wall to the left or the right
            if (x - 1, y) in warehouse.walls or (x + 1, y) in warehouse.walls:
                potentialtaboos.append((x, y))

            if itsacorner((x, y), warehouse) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []
            y += 1

        # Check y up direction
        y = yoriginal - 1
        potentialtaboos = []
        while (x, y) not in warehouse.walls and (x, y) not in warehouse.targets and (
                x, y) in emptyspace:
            # Check if there is wall to the left or the right
            if (x - 1, y) in warehouse.walls or (x + 1, y) in warehouse.walls:
                potentialtaboos.append((x, y))

            if itsacorner((x, y), warehouse) and potentialtaboos != []:
                rule2taboos.extend(potentialtaboos)
                potentialtaboos = []
            y -= 1

    taboo.extend(rule2taboos)

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
              goalState=False):

        # Initialise SokobanPuzzle Problem
        self.macro = macro
        self.allow_taboo_push = allow_taboo_push
        self.verbose = verbose

        #-- Load Problemspace (Warehouse) --#
        #save initial state
        self.initial = warehouse.copy()

        self.alternateGoal = alternateGoal
        if alternateGoal == False:
            self.goal = warehouse.copy()
            self.goal.boxes = self.goal.targets
        else:
            self.goal = goalState

        self.original_boxes = warehouse.boxes
        self.original_worker = warehouse.worker


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

        new_state.boxes.remove(box_previous_location)
        new_state.worker = box_previous_location
        moveDirection = action[1]
        #Add box back in at action[1] from the previous location.
        new_state.boxes.append((box_previous_location[0] + MOVEMENTS[moveDirection][0],box_previous_location[1] + MOVEMENTS[moveDirection][1]))

        return new_state

    def result(self, state, action):
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
                    next_location = (box[0] + MOVEMENTS[movement][0], box[1] + MOVEMENTS[movement][1])
                    worker_location = (box[0] - MOVEMENTS[movement][0], box[1] - MOVEMENTS[movement][1])

                    # If the worker can get to the location to push the box
                    if not can_go_there(state, worker_location):
                        continue

                    # If taboo cells are not allowed
                    if not self.allow_taboo_push:
                        if next_location in taboo_cells_positions(state):
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
                action = (state.worker[0] + MOVEMENTS[movement][0], state.worker[1] + MOVEMENTS[movement][1])
                # If taboo cells are not allowed
                if not self.allow_taboo_push:
                    if action in taboo_cells_positions(state):
                        continue
                # If the action results in a wall
                if action in state.walls:
                    continue
                # If the action pushes a box
                if action in state.boxes:
                    # The new position of the box
                    box_movement = (action[0] + MOVEMENTS[movement][0], action[1] + MOVEMENTS[movement][1])
                    # If the box is pushed into a wall or another box
                    if box_movement in state.walls or box_movement in state.boxes:
                        continue
                # If no constraints are violated add the action to the list
                actions.append(movement)
        if self.verbose:
            print("  ->Actions: " + str(actions))
            print(state)
        return actions


    def return_rowColumn(self, solution):
        # Flips x,y in a macro solution so that it becomes row column
        newSolution = []
        for action in solution:
            newSolution.append(((action[0][1],action[0][0]),action[1]))
        return newSolution

    def h(self, n):
            """
            Heuristic
            """
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
    return warehouse


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
        move = (wh.worker[0] + MOVEMENTS[action][0], wh.worker[1] + MOVEMENTS[action][1])
        # If the action results in a wall position the action is illegal
        if move in wh.walls:
            return 'Failure'
        # If the action pushes a box
        if move in wh.boxes:
            # The new position of the box
            box_movement = (move[0] + MOVEMENTS[action][0], move[1] + MOVEMENTS[action][1])
            # If the box is pushed into a wall or another box the action is illegal
            if box_movement in wh.walls or box_movement in wh.boxes:
                return 'Failure'

        # Apply the actions to the wh
        wh.worker = (wh.worker[0] + MOVEMENTS[action][0], wh.worker[1] + MOVEMENTS[action][1])
        # If worker pushes a box
        if wh.worker in wh.boxes:
            # Find the box
            wh.boxes.remove(wh.worker)
            # Append its new position
            wh.boxes.append((wh.worker[0] + MOVEMENTS[action][0],\
                                     wh.worker[1] + MOVEMENTS[action][1]))
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
def solve_sokoban_elem_via_macro(warehouse):
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
    print('Solving for Macro Action Sequence')
    result = solve_sokoban_macro(warehouse)

    #Check if Macro Solver deemed the puzzle impossible
    if result == ['Impossible']:
        return ['Impossible']

    #Flip Row_Column coordinates to xy
    macroActions = []
    for action in result:
        macroActions.append(((action[0][1],action[0][0]),action[1]))

    print('Macro Actions Found \n' + str(macroActions))

    #For these macro actions solve for the workers (elementary) movements
    elemActions = []

    for action in macroActions:
        #Push From position is the position the worker needs to be in
        #  to push the box in the desired direction
        pushFrom = (action[0][0] - MOVEMENTS[action[1]][0],\
             action[0][1] - MOVEMENTS[action[1]][1])

        goal = warehouse.copy(worker=pushFrom)
        elemPuzzle = SokobanPuzzle(warehouse, macro=False,\
            alternateGoal=True ,goalState=goal)

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
        print('\nCompleted the Macro Action' + str(action))
        print(warehouse)

    print('\n\nFinal Elementary Sequence:')
    print(elemActions)
    return elemActions


def solve_sokoban_elem(warehouse):
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
    usingMacro = 1
    if usingMacro:
        return solve_sokoban_elem_via_macro(warehouse)

    else:
        puzzle = SokobanPuzzle(warehouse, verbose=True)
        puzzle.macro = False

        result = search.astar_graph_search(puzzle)

        if result:
            print("Start State: \n" + str(warehouse))
            print("Result State: \n" + str(result.state))
            return result.solution()
        else:
            return ['Impossible']


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''
    Determine whether the worker can walk to the cell dst=(row,column)
    without pushing any box.
    @param warehouse: a valid Warehouse object (from sokoban.py)
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    wh = warehouse.copy()
    walls = wh.walls
    boxes = wh.boxes.copy()
    # Because we can't move boxes, they are basically walls
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

def solve_sokoban_macro(warehouse, verbose=False):
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

    puzzle = SokobanPuzzle(warehouse, verbose=verbose)
    puzzle.macro = True

    t0 = time.time()
    result = search.astar_graph_search(puzzle)
    t1 = time.time()
    print ('The Macro Solve took {:.6f} seconds'.format(t1-t0))

    if result:
        print("Start State: \n" + str(puzzle.initial))
        print("Result State: \n" + str(result.state))
        return puzzle.return_rowColumn(result.solution())
    else:
        print("Start State: \n" + str(warehouse))
        print("Impossible")
        return ['Impossible']


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells_positions(warehouse):
    tc = taboo_cells(warehouse)
    row = 0
    column = 0
    for character in tc:
        if character == r'\n':
            row += 1
            column = 0
        if character == 'X':
            if row > 0:
                row = -row
            yield (row, column)


from sokoban import Warehouse

if __name__ == "__main__":
    wh=Warehouse()
    wh.load_warehouse("./warehouses/warehouse_19.txt")
    taboo = taboo_cells(wh)
