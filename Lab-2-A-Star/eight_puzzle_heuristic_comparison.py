import sys
import timeit
from copy import deepcopy

from prettytable import PrettyTable
from Puzzle import Puzzle
from puzzle_utils import file_input
from a_star import a_star, h_n


def check(choice):
    return choice < 1 or choice > 6


if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)

    choices = ["", "Zero Heuristic", "Displaced Tiles",
               "Manhattan", "Large Heuristic(h(n)>h*(n))", "Displaced Tiles (blank tile included)", "Manhattan (blank tile included)"]
    print('''1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Large Heuristic (h(n) > h*(n)).
5. Displaced tiles heuristic with blank tile cost included.
6. Manhattan distance heuristic with blank tile cost included''')
    choice1 = int(input('''Enter choice 1: '''))
    choice2 = int(input('Enter choice 2: '))
    if check(choice1) or check(choice2):
        print("Invalid choice bc.")
    else:
        table = PrettyTable(["Heuristic", "No. states explored",
                             "No. states on the optimal path", "Optimal path cost", "Time taken (secs)", "Monotonic restriction satisfied"])
        start_temp = deepcopy(start)
        # 1st choice
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice1))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, choice1)
        stop = timeit.default_timer()
        table.add_row([choices[choice1], len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        set1 = set(closed_list.keys())

        # 2nd choice
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice2))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_satisfied = a_star(
            puzzle_start, goal, choice2)
        stop = timeit.default_timer()
        table.add_row([choices[choice2], len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start, monotonic_satisfied])
        set2 = set(closed_list.keys())
        if optimal_path_cost == -1:
            print("\nNo path found. Goal is unreachable.\n")
        print(table)
        print()
        if set2.__eq__(set1):
            print("Both explored the same set of nodes.")
        elif set2.issuperset(set1):
            print(choices[choice2]+" visits all nodes visited by " +
                  choices[choice1]+" plus extra")
        elif set1.issuperset(set2):
            print(choices[choice1] + " visits all nodes visited by " +
                  choices[choice2] + " plus extra")
        else:
            print("No relation between visited nodes exist.")
