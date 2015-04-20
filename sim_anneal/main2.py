import random
import math
import DiscreteCS as dcs

from matplotlib import pyplot as plt

random.seed(128392)
# LIMIT = 100000
LIMIT = 1000

def update_temperature(T, k):
    return T - 0.001

def get_neighbors(i, L):
    assert L > 1 and i >= 0 and i < L
    if i == 0:
        return [1]
    elif i == L - 1:
        return [L - 2]
    else:
        return [i - 1, i + 1]

def accept(x, A, T):
    # nhbs = get_neighbors(x, len(A))
    # nhb = nhbs[random.choice(range(0, len(nhbs)))]
    nhb = random.choice(xrange(0, len(A))) # choose from all points

    delta = A[nhb] - A[x]

    if delta < 0:
        return nhb
    else:
        p = math.exp(-delta / T)
        return nhb if random.random() < p else x

def simulated_annealing(A):
    L = len(A)
    x0 = random.choice(xrange(0, L))
    T = 1.
    k = 1

    x = x0
    x_best = x0

    while T > 1e-3:
        x = accept(x, A, T)
        if(A[x] < A[x_best]):
            x_best = x
        T = update_temperature(T, k)
        k += 1

    print "iterations:", k
    return x, x_best, x0

def isLocalMinimum(value, funcRange):
    return all(value < v for v in funcRange)

def func(x):
    return - ( (0.5 - x[0] ** 2 + x[1] ** 2) * (math.exp( 1 - x[0]**2 - x[1]**2 )) )

def initialize(prod):
    return map(lambda (x): func(list(x)), prod)




cs = dcs.DiscreteCS(2, [ DimLimit(-4.0,4.0), DimLimit(-4.0,4.0) ], 0.1)

A = initialize(cs.getProduct())

def runSimAnneal(A):

    localMins = []

    for prod in cs.getProduct():

        nbs = cs.getNeighbors(list(prod))
        nbsVals = map(lambda(x): func(list(x)), nbs)
        val = func(list(prod))


        # exclude boundry points
        if len(nbs) == 4:

            if(isLocalMinimum(val, nbsVals)):
                localMins.append([ prod, val ])


    idx = 0
    mostMin = None

    for l in localMins:

        if mostMin == None:
            mostMin = l

        else:
            if mostMin[1] > l[1]:
                mostMin = l



    print "number of local minima: %d" % (len(localMins))
    print "global minimum @f(%s) = %0.3f" % (str(mostMin[0]), mostMin[1])

    print "***"
    localMins.sort(key=lambda x: x[1])
    print localMins[:5]


    print "***"
    localMins.reverse()
    print localMins[:5]
        #if(isminima_local(list(i), A)):
        #    local_minima.append([prod, A[i]])

    #for idx, val in enumerate(cs.getProduct()):
    #    print val



