class Puzzle:
    def __init__(self, puzzle_configuration, g_n, h_n):
        self.puzzle_configuration = puzzle_configuration
        self.g_n = g_n
        self.h_n = h_n

    def __lt__(self, other):
        if (self.g_n + self.h_n) == (other.g_n + other.h_n):
            return self.g_n < other.g_n
        return (self.g_n + self.h_n) < (other.g_n + other.h_n)
