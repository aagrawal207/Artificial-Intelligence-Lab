import numpy as np
from collections import Counter

prob_c1 = float(input("Enter the probability of chosing coin 1\n"))
prob_head1 = float(input("Enter the probability of head occuring on coin 1\n"))
prob_head2 = float(
    input("Enter the probability of head occuring on coint 2\n"))

NO_ITERATIONS = 1000
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


def get_e_z(observations, p, p1, p2, i: 'ith observation'):
    num = p * (p1 ** dictionary[observations[i]]) * \
        ((1-p1) ** (1-dictionary[observations[i]]))

    den = p * (p1 ** dictionary[observations[i]]) * ((1-p1) ** (1-dictionary[observations[i]])) \
        + (1-p) * (p2 ** (dictionary[observations[i]])) * \
        ((1-p2) ** (1-dictionary[observations[i]]))

    return num/den


def get_p(observations, p, p1, p2):
    sumation = sum((get_e_z(observations, p, p1, p2, i)
                    for i in range(len(observations))))
    return sumation/len(observations)


def get_p1(observations, p, p1, p2):
    num = sum((dictionary[observations[i]] * get_e_z(observations,
                                                     p, p1, p2, i) for i in range(len(observations))))
    denom = sum((get_e_z(observations, p, p1, p2, i)
                 for i in range(len(observations))))
    return num/denom


def get_p2(observations, p, p1, p2):
    M = Counter(observations)['H']
    temp = sum((dictionary[observations[i]] * get_e_z(observations,
                                                      p, p1, p2, i) for i in range(len(observations))))
    num = M - temp
    temp2 = sum((get_e_z(observations, p, p1, p2, i)
                 for i in range(len(observations))))
    denom = len(observations) - temp2
    return num/denom


observation = get_observations()
p, p1, p2 = 0.1, 0.1, 0.1
print(Counter(observation)['H'])
print(Counter(observation)['H'] - sum((dictionary[observation[i]] * get_e_z(observation,
                                                                            p, p1, p2, i) for i in range(len(observation)))))
print(sum((dictionary[observation[i]] * get_e_z(observation,
                                                p, p1, p2, i) for i in range(len(observation)))))


for i in range(1000):
    # e_z = get_e_z(observation,p, p1, p2)
    new_p = get_p(observation, p, p1, p2)
    new_p1 = get_p1(observation, p, p1, p2)
    new_p2 = get_p2(observation, p, p1, p2)
    p, p1, p2 = new_p, new_p1, new_p2

print("p: %f p1: %f p2: %f  \n" % (p, p1, p2))
