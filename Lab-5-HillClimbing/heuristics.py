# combined heuristic of manhattan and displaced
def combined_heuristic(puzzle_configuration, goal):
    return manhattan_heuristic(puzzle_configuration, goal) + displaced_tiles_heuristic(puzzle_configuration, goal)


# manhattan heuristic (without consideration of blank tile)
def manhattan_heuristic(puzzle_configuration, goal):
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


# displaced tiles heuristic
def displaced_tiles_heuristic(puzzle_configuration, goal):
    heuristic_distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle_configuration[i][j] == 0:
                continue
            if puzzle_configuration[i][j] != goal[i][j]:
                heuristic_distance += 1
    return heuristic_distance


# displaced tiles heuristic with blank tile included in cost
def displaced_tiles_heuristic_with_blank_tile(puzzle_configuration, goal):
    heuristic_distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle_configuration[i][j] != goal[i][j]:
                heuristic_distance += 1
    return heuristic_distance


# manhattan heuristic (without consideration of blank tile)
def manhattan_heuristic_with_blank_tile(puzzle_configuration, goal):
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
            heuristic_distance += abs(real_row[val] - i) + \
                abs(real_col[val] - j)
    return heuristic_distance
