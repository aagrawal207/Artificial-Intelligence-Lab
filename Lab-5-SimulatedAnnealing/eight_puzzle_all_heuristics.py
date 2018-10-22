from copy import deepcopy
from prettytable import PrettyTable
from Puzzle import Puzzle
from simulated_annealing import simulated_annealing, h_n
import sys
import timeit
from puzzle_utils import file_input, print_simulated_annealing
import math


if __name__ == '__main__':
    # sys.setrecursionlimit(1)
    start, goal = file_input(sys.path[0], sys.argv)
    choice = int(input('''
1. Displced tiles Heuristic.
2. Manhattan distance Heuristic.
3. Displaced tile heuristic with blank tile cost included
4. Manhattan distance heuristic with blank tile cost included
5. Manhattan and displaced tile combined heuristic
Enter choice: '''))
    if choice > 5 or choice < 1:
        print("Invalid choice bc.")
    else:
        max_temperature = int(input("Enter the max temperature\n"))
        cooling_function = int(
            input("1. Exponential decay\n2. linear decay\n3. logarithmic decay"))
        start_time = timeit.default_timer()
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice))
        parent_list, optimal_path_cost, string_to_matrix_mapping, number_states_explored = simulated_annealing(
            puzzle_start, goal, choice, max_temperature, cooling_function)
        stop_time = timeit.default_timer()
        # print(f'Len of parent list : {len(parent_list)}')
        print_simulated_annealing(start, goal, parent_list, optimal_path_cost,
                                  string_to_matrix_mapping, number_states_explored)
        print(f'Time taken: {stop_time -start_time}')
