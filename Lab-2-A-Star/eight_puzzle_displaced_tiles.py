import sys

from a_star import a_star
from heuristics import displaced_tiles_heuristic
from Puzzle import Puzzle
from puzzle_utils import file_input, print_a_star

# each separate list in puzzle_start list represent a row
# 0 represent blank space
if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)
    puzzle_start = Puzzle(start, 0, displaced_tiles_heuristic(start, goal))
    closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
        puzzle_start, goal, 2)
    if optimal_path_cost >= 0:
        print("Goal found successfully.")
    else:
        print("Goal NOT found")

    print_a_star(start, goal, parent_list, optimal_path_cost,
                 string_to_matrix_mapping, str(len(closed_list)))

    print("Is monotonic restriction followed: %s" % (str(monotonic_satisfied)))
