import sys

from a_star import a_star
from heuristics import zero_heuristic
from Puzzle import Puzzle
from puzzle_utils import file_input, print_a_star


if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)
    puzzle_start = Puzzle(start, 0, zero_heuristic())
    closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_restriction = a_star(
        puzzle_start, goal, 1)

    print_a_star(start, goal, parent_list, optimal_path_cost,
                 string_to_matrix_mapping, str(len(closed_list)))

    print("Is monotonic restriction followed: %s" %
          (str(monotonic_restriction)))
