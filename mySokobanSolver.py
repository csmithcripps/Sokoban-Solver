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

import sokoban

#  Global Variables - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MOVEMENTS = {"Up": (0, -1),
             "Down": (0, 1),
             "Left": (-1, 0),
             "Right": (1, 0)}

UP = MOVEMENTS["Up"]
DOWN = MOVEMENTS["Down"]
LEFT = MOVEMENTS["Left"]
RIGHT = MOVEMENTS["Right"]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(9945008, 'Cody', 'Cripps'), (10283391, 'Faith', 'Lim'), (10411551, 'Mai', 'Bernt')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#returns the empty spaces in the maze
def getemptyspace(warehouse, includeboxes):
    # Put warehouse into a list by \n
    warehouseinlines = str(warehouse).split("\n")
    # Create a coordinate list of empty space cells
    emptyspace = list(sokoban.find_2D_iterator(warehouseinlines, " "))

    i=0
    while i < len(emptyspace):
        coord=emptyspace[i]
        if (not inmaze(coord, warehouse, includeboxes)):
            emptyspace.remove(coord)
            i-=1
        i+=1

    return emptyspace

#Works out if a tile is in the maze
#Returns true if it is, false if not
def inmaze(coord, warehouse, includeboxes):
    walls = warehouse.walls
    if includeboxes:
        walls.extend(warehouse.boxes)
    # Work out warehouse limits
    X, Y = zip(*walls)
    height = max(Y) - min(Y) + 1
    width = max(X) - min(X) + 1
    xoriginal = coord[0]
    yoriginal = coord[1]
    right = False
    left = False
    top = False
    bottom = False
    x = xoriginal + 1
    y = yoriginal
    # Check right
    while x < width:
        if (x, y) in walls:
            right = True
            break
        x += 1
    # Check left
    x = xoriginal - 1
    while x > -1:
        if (x, y) in walls:
            left = True
            break
        x -= 1
    y = yoriginal + 1
    x = xoriginal
    # Check top
    while y < height:
        if (x, y) in walls:
            top = True
            break
        y += 1
    # Check bottom
    y = yoriginal - 1
    x = xoriginal
    while y > -1:
        if (x, y) in walls:
            bottom = True
            break
        y -= 1

    return left and right and top and bottom


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
    # FAITH DO IT

    # Placeholder to hold taboo coords
    taboo = []

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

    emptyspace = getemptyspace(warehouse, False)

    for i in emptyspace:
        if itsacorner(i, warehouse) and i not in warehouse.targets:
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
    # Shamelessly rip the in built string maker from warehouse
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

    def __init__(self, warehouse, allow_taboo_push=False, macro=False):
        # Initialise SokobanPuzzle Problem

        # Load Problemspace (Warehouse)
        self.Warehouse = warehouse
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.walls = tuple(warehouse.walls)
        self.boxes = tuple(warehouse.boxes)
        self.worker = tuple(warehouse.worker)
        self.targets = tuple(warehouse.targets)

    def result(self, action):

        raise NotImplementedError

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        actions = []

        if self.macro:
            return actions
        else:
            for movement in MOVEMENTS:
                # Apply given movement to the position of the worker
                action = (state.worker[0] + MOVEMENTS[movement][0], state.worker[1] + MOVEMENTS[movement][1])
                # If taboo cells are not allowed
                if not self.allow_taboo_push:
                    if action in taboo_cells_positions():
                        continue
                # If the action results in a wall position the action is illegal
                if action in state.walls:
                    continue
                # If the action pushes a box
                if action in state.boxes:
                    # The new position of the box
                    box_movement = (action[0] + MOVEMENTS[movement][0], action[1] + MOVEMENTS[movement][1])
                    # If the box is pushed into a wall or another box the action is illegal
                    if box_movement in state.walls or box_movement in state.boxes:
                        continue
                # If no constraints are violated add the action to the list
                actions.append(action)

        return actions

    def h(self, action):
        raise NotImplementedError


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    for action in action_seq:
        # Apply given movement to the position of the worker
        move = (warehouse.worker[0] + MOVEMENTS[action][0], warehouse.worker[1] + MOVEMENTS[action][1])
        # If the action results in a wall position the action is illegal
        if move in warehouse.walls:
            return 'Failure'
        # If the action pushes a box
        if move in warehouse.boxes:
            # The new position of the box
            box_movement = (move[0] + MOVEMENTS[action][0], move[1] + MOVEMENTS[action][1])
            # If the box is pushed into a wall or another box the action is illegal
            if box_movement in warehouse.walls or box_movement in warehouse.boxes:
                return 'Failure'

        # Apply the actions to the warehouse
        warehouse.worker = (warehouse.worker[0] + MOVEMENTS[action][0], warehouse.worker[1] + MOVEMENTS[action][1])
        # If worker pushes a box
        if warehouse.worker in warehouse.boxes:
            for i in range(0, len(warehouse.boxes)):
                # Find the box and push it in the given direction
                if warehouse.worker == warehouse.boxes[i]:
                    warehouse.boxes[i] = (
                        warehouse.worker[0] + MOVEMENTS[action][0], warehouse.worker[1] + MOVEMENTS[action][1])

    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    puzzle = SokobanPuzzle(warehouse)
    puzzle.macro = False

    result = search.uniform_cost_search(puzzle)

    if result:
        return result
    else:
        return 'Impossible'


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

    walls = warehouse.walls
    # because we can't move boxes they are basically walls
    walls.extend(warehouse.boxes)
    worker = warehouse.worker
    explored = []

    fullyexplored=False

    explored.append(worker)

    # Keep checking the 4 squares around tile in question, if you can go to them,
    # add to explored. Keep going back to explored and doing the test on each one of them
    def explore(coord):
        x = coord[0]
        y = coord[1]

        # explore tile on top
        if (x, y - 1) not in walls and (x, y - 1) not in explored:
            explored.append((x, y - 1))

        # explore tile on beneath
        if (x, y + 1) not in walls and (x, y + 1) not in explored:
            explored.append((x, y + 1))

        # explore tile on left
        if (x - 1, y) not in walls and (x - 1, y) not in explored:
            explored.append((x - 1, y))

        # explore tile on right
        if (x + 1, y) not in walls and (x + 1, y) not in explored:
            explored.append((x + 1, y))

    # while its not the tile we're looking for or we've explored every single tile.
    while not fullyexplored:
        lengthofexplored=len(explored)
        for i in explored:
            explore(i)
            if dst in explored:
                return True
            #if explored hasn't grown, it means there is no where else to explore
            #meaning it's fully explored
            if lengthofexplored==len(explored):
                fullyexplored=True

    return False
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
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

    puzzle = SokobanPuzzle(warehouse)
    puzzle.macro = True

    result = search.uniform_cost_search(puzzle)

    if result:
        return result
    else:
        return 'Impossible'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells_positions(self):
    tc = taboo_cells(self.Warehouse)
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
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_19.txt")
    taboo = taboo_cells(wh)
    can_go_there(wh, (0,1))
