import numpy as np
from collections import Counter
import random

prob_c1 = float(input("Enter the probability of chosing coin 1\n"))
prob_head1 = float(input("Enter the probability of head occuring on coin 1\n"))
prob_head2 = float(input("Enter the probability of head occuring on coin 2\n"))

NO_ITERATIONS = 5000
dictionary = {'H': 1, 'T': 0}


def get_observations():
    observations = []
    for no in range(NO_ITERATIONS):
        prob_p = np.random.choice(np.arange(0, 2), p=[prob_c1, 1-prob_c1])
        if prob_p == 0:
            prob_getting_head = np.random.choice(
                np.arange(0, 2), p=[prob_head1, 1-prob_head1])
        else:
            prob_getting_head = np.random.choice(
                np.arange(0, 2), p=[prob_head2, 1-prob_head2])
        if prob_getting_head == 0:
            observations.append('H')
        else:
            observations.append('T')
    return observations


def get_e_zi(observations, p, p1, p2, i: "ith observation"):
    num = p * (p1 ** dictionary[observations[i]]) * \
        ((1-p1) ** (1-dictionary[observations[i]]))
    den = num + ((1-p) * (p2 ** (dictionary[observations[i]]))
                 * ((1-p2) ** (1-dictionary[observations[i]])))

    return num/den


def get_expected_c1(observations, p, p1, p2):
    num = sum(get_e_zi(observations, p, p1, p2, i)
              for i in range(len(observations)))
    return num


def get_expected_heads_c1(observations, p, p1, p2):
    num = sum(dictionary[observations[i]] * get_e_zi(observations,
                                                     p, p1, p2, i) for i in range(len(observations)))
    return num


def get_p(observations, p, p1, p2, expected_c1):
    return expected_c1/len(observations)


def get_p1(observations, p, p1, p2, expected_heads_c1, expected_c1):
    return expected_heads_c1/expected_c1


def get_p2(observations, p, p1, p2, expected_heads_c1, expected_c1):
    M = Counter(observations)['H']
    num = M - expected_heads_c1
    denom = len(observations) - expected_c1
    return num/denom


observation = get_observations()
p, p1, p2 = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
print("Initial values:\np = %f\np1=%f\np2 = %f" % (p, p1, p2))
total_heads = Counter(observation)['H']
print("Total heads observed: %d" % (total_heads))
print("Total number of iterations: %d" % NO_ITERATIONS)

for i in range(NO_ITERATIONS):
    expected_c1 = get_expected_c1(observation, p, p1, p2)
    expected_heads_c1 = get_expected_heads_c1(observation, p, p1, p2)
    new_p = get_p(observation, p, p1, p2, expected_c1)
    new_p1 = get_p1(observation, p, p1, p2, expected_heads_c1, expected_c1)
    new_p2 = get_p2(observation, p, p1, p2, expected_heads_c1, expected_c1)
    p, p1, p2 = new_p, new_p1, new_p2

print("Final values:\np: %f p1: %f p2: %f  \n" % (p, p1, p2))
