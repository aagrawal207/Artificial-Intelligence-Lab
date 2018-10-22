from copy import deepcopy
from prettytable import PrettyTable
from Puzzle import Puzzle
from hill_climbing import hill_climbing, h_n
import sys
import timeit
from puzzle_utils import file_input, print_hill_climbing
import math


if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)
    choice = int(input('''
1. Displced tiles Heuristic.
2. Manhattan distance Heuristic.
3. Displaced tile heuristic with blank tile cost included
4. Manhattand distance heuristic with blank tile cost included
5. Manhattan distance + displaced tile heuristic
Enter choice: '''))
    if choice > 5 or choice < 1:
        print("Invalid choice bc.")
    start_time = timeit.default_timer()
    puzzle_start = Puzzle(start, 0, h_n(start, goal, choice))
    closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = hill_climbing(
        puzzle_start, goal, choice)
    stop_time = timeit.default_timer()
    print_hill_climbing(start, goal, parent_list, optimal_path_cost,
                        string_to_matrix_mapping, str(len(closed_list)))
    print(f'Time taken: {stop_time -start_time}')

    print("Is monotonic restriction followed: %s" %
          (str(monotonic_satisfied)))
