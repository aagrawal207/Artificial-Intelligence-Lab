def profile(epsilon1, epsilon2, epsilon3, x):
    y = -1
    epsilon4 = epsilon3 + (epsilon2 - epsilon1)
    if epsilon1 <= x < epsilon2:
        y = (x - epsilon1) / (epsilon2 - epsilon1)
    elif epsilon2 <= x <= epsilon3:
        y = 1
    elif epsilon3 < x <= epsilon4:
        y = (epsilon4 - x) / ((epsilon4 - epsilon3))
    return y


def fuzzication(epsilon: 'array', x):
    epsilon1 = -1 * epsilon[0]
    epsilon2 = 0
    epsilon3 = 0
    y_zero = profile(epsilon1, epsilon2, epsilon3, x)

    epsilon1 = 0
    epsilon2 = epsilon[1]
    epsilon3 = epsilon[2]
    y_small_pos = profile(epsilon1, epsilon2, epsilon3, x)

    epsilon1 = -1 * (epsilon[1] + epsilon[2])
    epsilon2 = -1 * epsilon[2]
    epsilon3 = -1 * (epsilon[1])
    y_small_neg = profile(epsilon1, epsilon2, epsilon3, x)

    return (y_small_neg, y_zero, y_small_pos)


def rules(theta, omega, epsilon_theta: 'array', epsilon_omega: 'array'):
    y_theta = fuzzication(epsilon_theta, theta)
    y_omega = fuzzication(epsilon_omega, omega)

    dictionary = {'00': 2, '01': 1, '02': 0, '10': 1,
                  '11': 0, '12': -1, '20': 0, '21': -1, '22': -2}
    y_curr = []
    for id1, val1 in enumerate(y_theta):
        for id2, val2 in enumerate(y_omega):
            if val1 or val2 == -1:
                continue
            else:
                curr_belongingness = min(val1, val2)
                curr_id = dictionary[str(id1) + str(id2)]
                y_curr.append([curr_belongingness, curr_id])
    return y_curr


def defuzzify(epsilon: 'array of epsilon for curr', y):
    epsilon1 = epsilon[0]
    epsilon2 = epsilon[1]
    epsilon3 = epsilon[2]
    epsilon4 = epsilon3 + (epsilon2 - epsilon1)
    x_centroid = (epsilon1 + epsilon4) / 2
    base1 = epsilon4 - epsilon1
    base2 = base1 - 2*(epsilon2 - epsilon1)
    area = 0.5 * (base1 + base2) * y
    # either x_centroid or area is being returned 0 for the given values
    return x_centroid, area


def compute_current(theta, omega, epsilon_theta, epsilon_omega, epsilon_curr):
    curr_list = rules(theta, omega, epsilon_theta, epsilon_omega)

    dictionary = {0: [-1 * epsilon_curr[0], 0, 0],
                  1: [0, epsilon_curr[1], epsilon_curr[2]],
                  2: [epsilon_curr[3], epsilon_curr[4], epsilon_curr[5]],
                  -1: [-1 * (epsilon_curr[2] + epsilon_curr[1]), -1 * epsilon_curr[2], -1 * epsilon_curr[1]],
                  - 2: [-1 * (epsilon_curr[5] + epsilon_curr[4] - epsilon_curr[3]), -1 * epsilon_curr[5], -1 * epsilon_curr[4]]
                  }

    total_area = 0
    weighted_area = 0
    for tup in curr_list:
        centroid, area = defuzzify(dictionary[tup[1]], tup[0])
        weighted_area += (centroid * area)
        total_area += area
    return weighted_area / total_area


def main():
    print("started")
    epsilon_theta = [3, 2, 5]
    epsilon_omega = [2, 2, 4]
    epsilon_curr = [1, 1, 1, 1, 1, 1]
    theta = 2.5
    omega = 3

    current = compute_current(
        theta, omega, epsilon_theta, epsilon_omega, epsilon_curr)
    print(current)


if __name__ == "__main__":
    main()
