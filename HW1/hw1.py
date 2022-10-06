import numpy as np
import math

with open('input.dat', 'r') as f:
    d = f.readlines()
    n, tau = int(d[0]), float(d[1]) # d[0] is the number of messages. d[1] is τ
    cis = [] # list for storing all transmission time (Ci)
    tis = [] # list for storing all period (Ti)
    
    # extract priority (Pi), the transmission time (Ci), and the period (Ti) of each message starting from col 3
    for i in range(2, len(d)):
        mu = [float(x) for x in d[i].split()]
        cis.append(mu[1])
        tis.append(mu[2])

# n = 3
# tau = 0.1
# cis = [10, 30, 20]
# tis = [50, 200, 100]
schedulable = True
worst_response = []
for i in range(n):
    qi = rhs = bi = max(cis[i:]) # blocking time for μi
    # qi = rhs = bi = cis[i]
        
    first = True
    while first or (rhs + cis[i] <= tis[i] and qi != rhs):
        qi = rhs
        rhs = bi
        first = False
        for j in range(i):
            rhs += (math.ceil((qi+tau)/tis[j])*cis[j])
        # print(qi, bi, rhs)

    if rhs + cis[i] > tis[i]: 
        print('constraint violation')
        schedulable = False
        break
    elif qi == rhs: 
        print('the system is schedulable')
        worst_response.append(qi+cis[i])

if schedulable:
    print("\n Worst-Case Response Times : ")
    for i in range(n):
        print('{:.3f} ms'.format(worst_response[i]))