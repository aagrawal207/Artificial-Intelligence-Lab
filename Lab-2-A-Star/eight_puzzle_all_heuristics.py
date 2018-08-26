from copy import deepcopy
from prettytable import PrettyTable
from Puzzle import Puzzle
from a_star import a_star, h_n
import sys
import timeit
from puzzle_utils import file_input, print_a_star


if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)
    choice = int(input('''1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Large Heuristic (h(n) > h*(n)).
5. Displaced tile heuristic with blank tile cost included
6. Manhattand distance heuristic with blank tile cost included
7. Compare all the above and show in table format.
Enter choice: '''))
    if choice > 7 or choice < 1:
        print("Invalid choice bc.")
    elif choice == 7:
        table = PrettyTable(["Heuristic", "Total states explored", "Total states on the optimal path",
                             "Optimal path cost", "Total time taken (secs)", "Monotonic restriction satisfied"])
        start_temp = deepcopy(start)
        # No Heuristic
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 1))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 1)
        stop = timeit.default_timer()
        table.add_row(["No Heuristic", len(closed_list.keys(
        )), optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        # displaced tiles
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 2))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 2)
        stop = timeit.default_timer()
        table.add_row(["Displaced tiles", len(closed_list.keys(
        )), optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        # Manhattan
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 3))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 3)
        if optimal_path_cost == -1:
            print("No path found. Goal is unreachable.")
            exit(0)
        stop = timeit.default_timer()
        table.add_row(["Manhattan", len(closed_list.keys()), optimal_path_cost +
                       1, optimal_path_cost, stop - start, monotonic_satisfied])
        # Larger heuristic
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 4))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 4)
        stop = timeit.default_timer()
        table.add_row(["Large Heuristic", len(closed_list.keys(
        )), optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        # Displaced tile heuristic with blank tile cost included
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 5))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 5)
        stop = timeit.default_timer()
        table.add_row(["Displaced with blank tile", len(closed_list.keys(
        )), optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        # Manhattand distance heuristic with blank tile cost included
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 6))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, 6)
        stop = timeit.default_timer()
        table.add_row(["Manhattan with blank tile", len(closed_list.keys(
        )), optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        print(table)
    else:
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice))
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, choice)
        print_a_star(start, goal, parent_list, optimal_path_cost,
                     string_to_matrix_mapping, str(len(closed_list)))

        print("Is monotonic restriction followed: %s" %
              (str(monotonic_satisfied)))
