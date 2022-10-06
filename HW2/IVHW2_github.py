

import math
import pandas as pd
import random
from datetime import datetime
from copy import deepcopy as copy
import numpy as np

def load_data(file):
    datContent = [i.strip().split() for i in open(file).readlines()]

    message_num = int(datContent[0][0])
    tau = float(datContent[1][0])
    datContent = datContent[2:]

    for i in range(message_num):
        datContent[i] = [int(datContent[i][0]), float(datContent[i][1]), int(datContent[i][2])] 

    df = pd.DataFrame(datContent, columns=["ID", "Ci", "Ti"]).set_index(["ID"])
    return df, message_num, tau

def get_response_time(message_df, message_num, tau):
    response_list = []
    for i in range(message_num):
        block = max(message_df.iloc[i:].Ci)
        Qi = block
        Bi = block
        RHS = Bi + sum([math.ceil((Qi+tau)/m.Ti) * m.Ci for m in message_df.iloc[:i].itertuples(index=False)])

        while Qi!=RHS:
            Qi = RHS
            RHS = Bi + sum([math.ceil((Qi+tau)/m.Ti) * m.Ci for m in message_df.iloc[:i].itertuples(index=False)])

        response_time = RHS + message_df.iloc[i].Ci
        if response_time > message_df.iloc[i].Ti:
            raise Exception
        
        response_list.append(response_time)
    return sum(response_list)

def simulated_annealing(message_df, message_num, tau, init_T):
    random.seed(datetime.now())
    T = init_T
    S_star = list(range(message_num))
    S = copy(S_star)
    optim = get_response_time(message_df, message_num, tau)
    while(T>0.01):
        T = T*0.99
        S_prime = copy(S)
        a = random.randint(0, message_num-1)
        b = random.randint(0, message_num-1)
        while a==b:
            b = random.randint(0, message_num-1)
        S_prime[a], S_prime[b] = S_prime[b], S_prime[a]
        
        try:
            cost_prime, cost = get_response_time(message_df.iloc[S_prime], message_num, tau), \
                                get_response_time(message_df.iloc[S], message_num, tau)
        except Exception:
            del S_prime
            continue
        
        delta = cost_prime-cost
        if cost_prime < optim:
            optim = cost_prime
            S_star = copy(S_prime)
            
        if delta<=0:
            S = copy(S_prime)
        else:
            prob = math.exp(-delta/T)
            random.seed(datetime.now())
            if random.random()<=prob:
                S = copy(S_prime)
        print(T)
        del S_prime
    
    S_star = np.array(S_star)
    print(S_star)
    for i in range(len(S_star)):
        m_id = np.argmin(S_star)
        print(m_id)
        S_star[m_id]=9999999
    print(optim)

m, message_num, tau = load_data('input.dat')
simulated_annealing(m, message_num, tau, 3)

 

