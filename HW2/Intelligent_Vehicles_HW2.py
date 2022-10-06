import numpy as np
import math
import random
from copy import copy

with open("input.dat", "r") as f:
    d = f.readlines()
    n, tau = int(d[0]), float(d[1])

    mus = {}

    for i in range(n):
        mu = [float(x) for x in d[i+2].split()]
        mus[i] = [mu[1], mu[2]]

def CAN_analysis(s):
    schedulable = True
    cis = []
    tis = []

    for id in s:
        cis.append(mus[id][0])
        tis.append(mus[id][1])
    wcrt = sum(tis) + len(tis) #worst-case response time


    worst_response = []
    for i in range(len(s)):
        qi = rhs = bi = max(cis[i:])

        first = True
        while first or (rhs+cis[i]<=tis[i] and qi!=rhs):
            qi = rhs
            rhs = bi
            first = False
            for j in range(i):
                rhs += (math.ceil((qi+tau)/tis[j])*cis[j])

        if rhs+cis[i] > tis[i]:
            # print('constraint violation')
            schedulable = False
            break
        # print('the system is scheduelable')
        worst_response.append(qi+cis[i])

    if schedulable:
        # print("\n Worst-Case Response Time : ")
        # for i in range(n):
            # print('{:.3f}ms'.format(worst_response[i]))
        wcrt = sum(worst_response)
    return wcrt

# s = [10 , 4 , 7 , 1 , 2 , 5 , 3 , 8 , 9  ,6 ,15  ,0 ,13 ,12 ,16 ,14 ,11]
# [a,b] = CAN_analysis(s)
# print(a,b)


def simluated_annealing(s, T, r):
    wcrt = CAN_analysis(s)
    wcrt_list = []

    s_best = copy(s)
    wcrt_min = wcrt
    rounds = 0

    while T > 0.01:
        rounds += 1
        T *= r
        s_prime = copy(s)
        id1 = random.randint(0, n-1)
        id2 = random.randint(0, n-1)
        while id1 == id2:
            id2 = random.randint(0, n-1)

        s_prime[id1], s_prime[id2] = s_prime[id2], s_prime[id1]

        wcrt_prime = CAN_analysis(s_prime)
        dc = wcrt_prime - wcrt
        wcrt_list.append(wcrt_prime)


        if dc <= 0:
            s = copy(s_prime)
            if wcrt_prime < wcrt_min:
                wcrt_min = wcrt_prime
                s_best = copy(s_prime)
            wcrt = wcrt_prime
                
        else:
            prob_to_move = np.exp(-dc/T)
            if random.uniform(0, 1) <= prob_to_move:
                s = copy(s_prime)
    print('Total Round: ', rounds)

    print(min(wcrt_list) == wcrt_min)

    return s_best

s = [i for i in range(n)]
s_best = simluated_annealing(s, 100, 0.99)
wcrt_best = CAN_analysis(s_best)
print(wcrt_best)
