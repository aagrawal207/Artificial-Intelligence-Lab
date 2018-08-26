from queue import PriorityQueue
from Puzzle import Puzzle
from copy import deepcopy
import heuristics


def h_n(neighbour, goal, heuristic_used):
    if heuristic_used == 1:
        return heuristics.zero_heuristic()
    elif heuristic_used == 2:
        return heuristics.displaced_tiles_heuristic(neighbour, goal)
    elif heuristic_used == 3:
        return heuristics.manhattan_heuristic(neighbour, goal)
    elif heuristic_used == 4:
        return heuristics.greater_heuristic(neighbour, goal)
    elif heuristic_used == 5:
        return heuristics.displaced_tiles_heuristic_with_blank_tile(neighbour, goal)
    elif heuristic_used == 6:
        return heuristics.manhattan_heuristic_with_blank_tile(neighbour, goal)


def swap(puzzle_state, row, col, new_row, new_col):
    temp = puzzle_state[row][col]
    puzzle_state[row][col] = puzzle_state[new_row][new_col]
    puzzle_state[new_row][new_col] = temp
    return puzzle_state


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


def a_star(puzzle_start, goal, heuristic_used):
    monotonic_restriction_satisfied = True
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
        node_h_n = puzzle_state.h_n
        neighbours = find_neighbours(puzzle_state.puzzle_configuration)
        for neighbour in neighbours:
            neighbour_string = ''.join(str(val)
                                       for row in neighbour for val in row)
            if neighbour_string not in closed_list:
                parent_list[neighbour_string] = puzzle_configuration_string
                neighbour_h_n = h_n(neighbour, goal, heuristic_used)

                # to check for monotonic restriction is satisfied or not
                if node_h_n > neighbour_h_n + 1:
                    monotonic_restriction_satisfied = False

                open_list.put(
                    Puzzle(neighbour, puzzle_state.g_n + 1, h_n(neighbour, goal, heuristic_used)))
                open_list_len += 1
    return closed_list, parent_list, optimal_path_cost, string_to_matrix_mapping, monotonic_restriction_satisfied
