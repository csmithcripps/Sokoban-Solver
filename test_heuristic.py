from sokoban import Warehouse

from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_action_seq
from mySokobanSolver import solve_sokoban_elem, can_go_there, solve_sokoban_macro, SokobanPuzzle

class tester(SokobanPuzzle):


    def h(self, n):
            """
            switch based on macro.
            """
            if self.macro:
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

def manhatten(p1, p2):
    """
    Computes the manhatten distance between a set of points

    inputs:
        2 locations as tuples

    return:
        Manhatten distance between the input locations
    """
    return abs((p1[0] - p2[0])) + abs((p1[1] - p2[1]))



puzzle_t1 ='#######\n#.$@ #\n#######'
wh = Warehouse()
wh.extract_locations(puzzle_t1.split(sep='\n'))
# wh.load_warehouse("./warehouses/warehouse_05.txt")
# test = tester(wh, True, False)
# heur = test.h(test)
# actions = test.actions(test.initial)
# print(wh.targets)
print(wh)
# res = test.result(test.initial,"Right")
# print(actions)
# print(res)

result = solve_sokoban_elem(wh)
print(result)
