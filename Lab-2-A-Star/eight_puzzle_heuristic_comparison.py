import sys
import timeit
from copy import deepcopy

from prettytable import PrettyTable
from Puzzle import Puzzle
from puzzle_utils import file_input
from a_star import a_star, h_n


def check(choice):
    return choice < 1 or choice > 4


# each separate list in puzzle_start list represent a row
# 0 represent blank space
if __name__ == '__main__':
    start, goal = file_input(sys.path[0], sys.argv)

    choices = ["", "Zero Heuristic", "Displaced Tiles",
               "Manhattan", "Large Heuristic(h(n)>h*(n))"]
    print("1. Zero Heuristic.\n"
          "2. Displced tiles Heuristic.\n"
          "3. Manhattan distance Heuristic.\n"
          "4. Large Heuristic (h(n) > h*(n)).")
    choice1 = int(input('''Enter choice 1: '''))
    choice2 = int(input('Enter choice 2: '))
    if check(choice1) or check(choice2):
        print("Invalid choice bc.")
    else:
        table = PrettyTable(["Heuristic", "Total states explored",
                             "Total states on the optimal path", "Optimal path cost", "Total time taken (secs)"])
        start_temp = deepcopy(start)
        # 1st choice
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice1))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, choice1)
        stop = timeit.default_timer()
        table.add_row([choices[choice1], len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start])
        set1 = set(closed_list.keys())

        # 2nd choice
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice2))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, choice2)
        stop = timeit.default_timer()
        table.add_row([choices[choice2], len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start])
        set2 = set(closed_list.keys())
        print(table)
        print()
        if set2.__eq__(set1):
            print("Both explored same number of states.")
        elif set2.issuperset(set1):
            print(choices[choice2]+" visits all nodes visited by " +
                  choices[choice1]+"plus extra")
        elif set1.issuperset(set2):
            print(choices[choice1] + " visits all nodes visited by " +
                  choices[choice2] + " plus extra")
        else:
            print("No relation between visited nodes exist.")
