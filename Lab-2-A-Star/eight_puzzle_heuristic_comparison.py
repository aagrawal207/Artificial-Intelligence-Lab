from copy import deepcopy
from prettytable import PrettyTable
from queue import PriorityQueue
import os
import sys
import timeit


class Puzzle:
    def __init__(self, puzzle_configuration, g_n, h_n):
        self.puzzle_configuration = puzzle_configuration
        self.g_n = g_n
        self.h_n = h_n

    def __lt__(self, other):
        return (self.g_n + self.h_n) <= (other.g_n + other.h_n)


def swap(puzzle_state, row, col, new_row, new_col):
    temp = puzzle_state[row][col]
    puzzle_state[row][col] = puzzle_state[new_row][new_col]
    puzzle_state[new_row][new_col] = temp
    return puzzle_state


def convert_to_matrix(row1, row2, row3):
    matrix = [[int(x) for x in row1.split()]]
    matrix.append([int(x) for x in row2.split()])
    matrix.append([int(x) for x in row3.split()])
    return matrix


def print_configuration(matrix):
    for row in matrix:
        for val in row:
            print(val, end=" ")
        print()


def print_optimal_path(parent_list, optimal_path_len, goal, start, string_to_matrix_mapping, total_states_on_optimal_path):
    if goal == start:
        print("Total number of states on optimal path:",
              total_states_on_optimal_path)
    else:
        node = parent_list[''.join(str(val) for row in goal for val in row)]
        node = string_to_matrix_mapping[node]
        print_optimal_path(parent_list, optimal_path_len,
                           node, start, string_to_matrix_mapping, total_states_on_optimal_path + 1)
        print_configuration(node)
        print("  v  ")


def find_neighbours(puzzle_state):
    neighbours = []
    row, col = 0, 0
    N = len(puzzle_state)
    for i in range(3):
        for j in range(3):
            if puzzle_state[i][j] == 0:
                row, col = i, j
                break
    if row + 1 < N:
        temp = deepcopy(puzzle_state)
        neighbours.append(swap(temp, row, col, row + 1, col))
    if row - 1 >= 0:
        temp = deepcopy(puzzle_state)
        neighbours.append(swap(temp, row, col, row - 1, col))
    if col - 1 >= 0:
        temp = deepcopy(puzzle_state)
        neighbours.append(swap(temp, row, col, row, col - 1))
    if col + 1 < N:
        temp = deepcopy(puzzle_state)
        neighbours.append(swap(temp, row, col, row, col + 1))
    return neighbours


def h_n(puzzle_configuration, goal, heuristic_id):
    if heuristic_id == 1:
        return 0
    elif heuristic_id == 2:
        heuristic_distance = 0
        for i in range(3):
            for j in range(3):
                if puzzle_configuration[i][j] == 0:
                    continue
                if puzzle_configuration[i][j] != goal[i][j]:
                    heuristic_distance += 1
        return heuristic_distance
    elif heuristic_id == 3:
        heuristic_distance = 0
        real_row = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        real_col = [0, 1, 2, 0, 1, 2, 0, 1, 2]
        for i in range(3):
            for j in range(3):
                real_row[goal[i][j] - 1] = i
                real_col[goal[i][j] - 1] = j
        for i in range(3):
            for j in range(3):
                val = puzzle_configuration[i][j] - 1
                if val == -1:
                    continue
                heuristic_distance += abs(real_row[val] - i) + \
                    abs(real_col[val] - j)
        return heuristic_distance
    else:
        heuristic_distance = 0
        values = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        for i in range(3):
            for j in range(3):
                if puzzle_configuration[i][j] != goal[i][j]:
                    heuristic_distance += values[3 * i + j]
        return heuristic_distance


def a_star(puzzle_start, goal, heuristic_id):
    open_list = PriorityQueue()
    open_list.put(puzzle_start)
    open_list_len = 1
    closed_list = {}
    parent_list = {}
    string_to_matrix_mapping = {}
    optimal_path_cost = -1
    while open_list_len > 0:
        puzzle_state = open_list.get()
        open_list_len -= 1
        puzzle_configuration_string = ''.join(
            str(val) for row in puzzle_state.puzzle_configuration for val in row)
        if puzzle_configuration_string in closed_list:
            continue
        closed_list[puzzle_configuration_string] = puzzle_state.puzzle_configuration
        string_to_matrix_mapping[puzzle_configuration_string] = puzzle_state.puzzle_configuration
        if puzzle_state.puzzle_configuration == goal:
            optimal_path_cost = puzzle_state.g_n
            break
        neighbours = find_neighbours(puzzle_state.puzzle_configuration)
        for neighbour in neighbours:
            neighbour_string = ''.join(str(val)
                                       for row in neighbour for val in row)
            if neighbour_string not in closed_list:
                string_to_matrix_mapping[neighbour_string] = neighbour
                parent_list[neighbour_string] = puzzle_configuration_string
                open_list.put(
                    Puzzle(neighbour, puzzle_state.g_n + 1, h_n(neighbour, goal, heuristic_id)))
                open_list_len += 1
    return closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping


def check(choice):
    return choice < 1 or choice > 4


# each separate list in puzzle_start list represent a row
# 0 represent blank space
if __name__ == '__main__':
    start = []
    goal = []
    if len(sys.argv) < 2:
        print("Please add input file name to the python run command.")
        exit(0)
    try:
        input_file = open(os.path.join(sys.path[0], sys.argv[1]))
        input_data = input_file.readlines()
        start = convert_to_matrix(input_data[1], input_data[2], input_data[3])
        goal = convert_to_matrix(input_data[6], input_data[7], input_data[8])
        input_file.close()
    except IOError:
        print("ERROR : IOERROR occurred while opening file")
        exit(0)

    choices = ["", "Zero Heuristic", "Displaced Tiles",
               "Manhattan", "Large Heuristic(h(n)>h*(n))"]
    print('''1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Large Heuristic (h(n) > h*(n)).''')
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
        if set2.issuperset(set1):
            print(choices[choice2]+" visits all nodes visited by " +
                  choices[choice1]+"plus extra")
        elif set1.issuperset(set2):
            print(choices[choice1] + " visits all nodes visited by " +
                  choices[choice2] + " plus extra")
        else:
            print("No relation between visited nodes exist.")
