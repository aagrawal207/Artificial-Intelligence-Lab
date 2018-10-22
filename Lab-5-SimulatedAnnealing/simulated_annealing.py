from queue import PriorityQueue
from Puzzle import Puzzle
from copy import deepcopy
import heuristics
import math
import random
import numpy as np


def h_n(neighbour, goal, heuristic_used):
    if heuristic_used == 1:
        return heuristics.displaced_tiles_heuristic(neighbour, goal)
    elif heuristic_used == 2:
        return heuristics.manhattan_heuristic(neighbour, goal)
    elif heuristic_used == 3:
        return heuristics.displaced_tiles_heuristic_with_blank_tile(neighbour, goal)
    elif heuristic_used == 4:
        return heuristics.manhattan_heuristic_with_blank_tile(neighbour, goal)
    elif heuristic_used == 5:
        return heuristics.combined_heuristic(neighbour, goal)


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


def get_temperature(max_temperature, iteration, choice):
    if choice == 1:
        return max_temperature*(0.95**iteration)
    elif choice == 2:
        return max_temperature/iteration
    elif choice == 3:
        if iteration == 1:
            return max_temperature
        return max_temperature/math.log(iteration)


def simulated_annealing(puzzle_start, goal, heuristic_used, max_temperature, cooling_function):
    open_list = PriorityQueue()
    open_list.put(puzzle_start)
    open_list_len = 1
    number_states_explored = 1
    parent_list = {}
    string_to_matrix_mapping = {}
    optimal_path_cost = -1
    max_iter = 5 * 10**4
    current_iter = 0
    while open_list_len > 0 and current_iter < max_iter:
        current_iter += 1
        puzzle_state = open_list.get()
        open_list_len -= 1
        puzzle_configuration_string = ''.join(
            str(val) for row in puzzle_state.puzzle_configuration for val in row)
        string_to_matrix_mapping[puzzle_configuration_string] = puzzle_state.puzzle_configuration
        current_cost = puzzle_state.h_n
        if puzzle_state.puzzle_configuration == goal:
            optimal_path_cost = puzzle_state.g_n
            break
        node_h_n = puzzle_state.h_n
        neighbours = find_neighbours(puzzle_state.puzzle_configuration)

        neighbour_chosen = None
        for neighbour in neighbours:
            neighbour_cost = h_n(neighbour, goal, heuristic_used)
            if neighbour_cost <= current_cost:
                neighbour_chosen = neighbour
                current_cost = neighbour_cost
        if neighbour_chosen is None:
            neighbour_chosen = random.choice(neighbours)
        neighbour_string = ''.join(
            str(val) for row in neighbour_chosen for val in row)
        neighbour_cost = h_n(neighbour_chosen, goal, heuristic_used)
        current_temp = get_temperature(
            max_temperature, current_iter, cooling_function)
        if current_temp == 0:
            current_temp = 1

        if neighbour_cost < current_cost:
            probability = 1
        else:
            probability = math.e ** (-1*(neighbour_cost -
                                         current_cost) / current_temp)

        chosen = np.random.choice(
            [True, False], p=[probability, 1 - probability])
        if chosen:
            number_states_explored += 1
            open_list.put(
                Puzzle(neighbour_chosen, puzzle_state.g_n + 1, neighbour_cost))
            parent_list[neighbour_string] = puzzle_configuration_string

        else:
            open_list.put(
                Puzzle(puzzle_state.puzzle_configuration, puzzle_state.g_n, puzzle_state.h_n))
        open_list_len += 1

    return parent_list, optimal_path_cost, string_to_matrix_mapping, number_states_explored
