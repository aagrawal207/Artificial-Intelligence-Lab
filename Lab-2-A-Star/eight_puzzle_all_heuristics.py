from copy import deepcopy
from prettytable import PrettyTable
from puzzle import Puzzle
from queue import PriorityQueue
import os
import sys
import timeit


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


def get_row_col_of_val(matrix, value):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == value:
                return (i, j)
    return None


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
        for i in range(3):
            for j in range(3):
                value = puzzle_configuration[i][j]
                final_row, final_col = get_row_col_of_val(goal, value)
                heuristic_distance += abs(i - final_row) + abs(j - final_col)
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
        # print(puzzle_state.puzzle_configuration)
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
    choice = int(input('''1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Compare all the above and show in table format.
Enter choice: '''))
    if choice > 4 or choice < 1:
        print("Invalid choice bc.")
    elif choice == 4:
        table = PrettyTable(["Heuristic", "Total states explored",
                             "Total states on the optimal path", "Optimal path cost", "Total time taken (secs)"])
        start_temp = deepcopy(start)
        # Manhattan
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 3))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, 3)
        if optimal_path_cost == -1:
            print("No path found. Goal is unreachable.")
            exit(0)
        stop = timeit.default_timer()
        table.add_row(["Manhattan", len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start])
        # displaced tiles
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 2))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, 2)
        stop = timeit.default_timer()
        table.add_row(["Displaced tiles", len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start])
        # No Heuristic
        start = start_temp
        puzzle_start = Puzzle(start, 0, h_n(start, goal, 1))
        start = timeit.default_timer()
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, 1)
        stop = timeit.default_timer()
        table.add_row(["No Heuristic", len(closed_list.keys()),
                       optimal_path_cost + 1, optimal_path_cost, stop - start])
        print(table)
    else:
        puzzle_start = Puzzle(start, 0, h_n(start, goal, choice))
        closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping = a_star(
            puzzle_start, goal, choice)
        if optimal_path_cost >= 0:
            print("Goal found successfully.")
        else:
            print("Goal NOT found")
        print("Start state: ")
        print_configuration(start)
        print("\nGoal state: ")
        print_configuration(goal)
        print('Total configurations explored: ' + str(len(closed_list.keys())))
        if optimal_path_cost > 0:
            print_optimal_path(parent_list, 0,
                               goal, start, string_to_matrix_mapping, 1)
            print_configuration(goal)
            print("Optimal cost of the path:", optimal_path_cost)
        elif optimal_path_cost == 0:
            print("Total number of states on optimal path:", 1)
            print_configuration(goal)
            print("  v  ")
            print_configuration(goal)
            print("Optimal cost of the path:", optimal_path_cost)
