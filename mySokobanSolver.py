
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

MOVEMENTS = {"Up"   : ( 0,-1),
             "Down" : ( 0, 1),
             "Left" : (-1, 0),
             "Right": ( 1, 0)}

UP    = MOVEMENTS["Up"]
DOWN  = MOVEMENTS["Down"]
LEFT  = MOVEMENTS["Left"]
RIGHT = MOVEMENTS["Right"]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [ (9945008, 'Cody', 'Cripps'), (10283391, 'Faith', 'Lim'), (10411551, 'Mai', 'Bernt') ]
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
    # FAITH DO IT

    taboo=[]

    def warehouselimits(warehouse):
        X,Y=zip(*warehouse.walls)
        height=max(Y)-min(Y)
        width = max(X)-min(X)
        return (height,width)

    #Identify taboo cells via rule 1:
    # Rule 1: if a cell is a corner inside the warehouse and not a target,
    #then it is a taboo cell.

    #Work out if a wall is a corner

    def itsacorner(coord, warehouse):
        #its a corner if it is in walls and
        # there are walls to the top left, top right, bottom left,
        # or bottom right of this cell

        #x+1, y+1 bottom right
        #Condition if its a corner
        x=coord[0]
        y=coord[1]
        # Hemmed by walls top and left
        if ((x-1, y) in warehouse.walls and (x, y-1) in warehouse.walls):
                return True

        # Hemmed by walls top and right
        if ((x+1,y) in warehouse.walls and (x, y-1) in warehouse.walls):
                return True

        # Hemmed by walls bottom and left
        if ((x-1, y) in warehouse.walls and (x, y+1) in warehouse.walls):
                return True

        # Hemmed by walls bottom and right
        if ((x+1, y) in warehouse.walls and (x+1, y+1) in warehouse.walls):
                return True

        return False

    #Put warehouse into a list by \n
    warehouseinlines=str(warehouse).split("\n")
    #Create a coordinate list of empty space cells
    emptyspace = list(sokoban.find_2D_iterator(warehouseinlines, " "))

    for i in emptyspace:
        if itsacorner(i, warehouse) and i not in warehouse.targets:
            taboo.append(i)

    return taboo


    #Identify taboo cells via rule 2:
     #Rule 2: all the cells between two corners inside the warehouse along a
    #wall are taboo if none of these cells is a target.


    raise NotImplementedError()

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


    def __init__(self, warehouse):
        # Initialise SokobanPuzzle Problem

        # Load Problemspace (Warehouse)
        self.Warehouse = warehouse
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
        # Mai

        #if self.macro:
            #Do one thing
        #else:
            #Do the other


        raise NotImplementedError

    def h(self,action):
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

    ##         "INSERT YOUR CODE HERE"

    raise NotImplementedError()


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

    ##         "INSERT YOUR CODE HERE"

    raise NotImplementedError()

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
