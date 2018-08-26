import os


def print_a_star(start, goal, parent_list, optimal_path_cost, string_to_matrix_mapping, len_closed_list):
    if optimal_path_cost >= 0:
        print("Goal found successfully.")
    else:
        print("Goal NOT found")

    print("Start state: ")
    print_configuration(start)
    print("\nGoal state: ")
    print_configuration(goal)
    print('Total configurations explored: ' + len_closed_list)
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


def file_input(directory, args):
    start = []
    goal = []
    if len(args) < 2:
        print("Please add input file name to the python run command.")
        exit(0)
    try:
        input_file = open(os.path.join(directory, args[1]))
        input_data = input_file.readlines()
        start = convert_to_matrix(input_data[1], input_data[2], input_data[3])
        goal = convert_to_matrix(input_data[6], input_data[7], input_data[8])
        input_file.close()
    except IOError:
        print("ERROR : IOERROR occurred while opening file")
        exit(0)
    return start, goal


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
