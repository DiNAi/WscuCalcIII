import math as m
import random as r
import numpy as np

# a state s of the system is a vector R^n

# the energy function is the function f :: R^n -> R that we want to minimze/maximize

class ObjectiveFunction(object):
    """function that we want to minimze/maximize"""

    def __init__(self, airity, fn):
        self.airity = airity
        self.fn = fn

    # apply the function to an array of arguments
    def apply(self, args):
        if len(args) != self.airity:
            raise Exception('ObjectiveFunction has airity ' + str(self.airity))

        return self.fn(args);


class NeighborGenerator(object):
    """Generates neighbors of a state"""

    def __init__(self, objectiveFunction, neighborMaxDelta):
        self.objectiveFunction = objectiveFunction
        self.neighborMaxDelta = neighborMaxDelta

    def generateRandomDelta(self, bit):
        if (bit == 1):
            return self.neighborMaxDelta
        else:
            return - self.neighborMaxDelta


    def generateRandomNeighbor(self, currentState):
        delta = [
            self.generateRandomDelta(r.getrandbits(1))
            for x in range(0,self.objectiveFunction.airity)
        ]

        return np.add(currentState, delta);


    def generateRandomNeighborWithTemp(self, temp, currentState):
        delta = [
            (temp * self.generateRandomDelta(r.getrandbits(1)))
            for x in range(0,self.objectiveFunction.airity)
        ]

        return np.add(currentState, delta);





def Acceptance(currStateEnergy, newStateEnergy, temperature):

    if(newStateEnergy < currStateEnergy):
        return 1.0

    return m.exp( ( - ( newStateEnergy - currStateEnergy ) ) / temperature )


# create a tempurature function based off of initial temperature
def ExpoentialTemperature(initialTemp):
    return lambda(iterNumber): initialTemp * (0.95 ** iterNumber)


def go3(delta, tempS):

    obFn = lambda(x): -1 * ( ( (0.5) - x[0]**2 + x[1]**2 ) * m.exp( 1 - x[0]**2 - x[1]**2 ) )

    obF = ObjectiveFunction(2, obFn)
    ng = NeighborGenerator(obF, delta)

    temp = tempS
    coolingRate = 0.03
    maxIterations = 100

    tempFn = ExpoentialTemperature(temp)

    initialState = [1,1]
    currentState = initialState
    best = obF.apply(initialState)

    k = 0
    while temp > 1:
        temp = tempFn(k)

        newState = ng.generateRandomNeighborWithTemp(temp, currentState)

        currStateEnergy = obF.apply(currentState)
        newStateEnergy = obF.apply(newState)

        if(Acceptance(currStateEnergy, newStateEnergy, temp) > r.random()):
            currentState = newState

        if(obF.apply(currentState) < best):
            best = obF.apply(currentState)

        print temp
        k = k + 1

    print str(currentState) + " -> " + str(best)

def go2(delta, tempS):

    obFn = lambda(x): m.exp(m.sin(50.0 * x[0])) + m.sin(60.0 * m.exp(x[1])) + m.sin(70.0 * m.sin(x[0])) + m.sin(m.sin(80.0 * x[1])) - m.sin(10.0 * (x[0] + x[1])) + (((x[0] ** 2.0) + (x[1] ** 2.0)) / 4.0)

    obF = ObjectiveFunction(2, obFn)
    ng = NeighborGenerator(obF, delta)

    temp = tempS
    coolingRate = 0.03
    maxIterations = 100

    tempFn = ExpoentialTemperature(temp)

    initialState = [20,20]
    currentState = initialState
    best = obF.apply(initialState)

    k = 0
    while temp > 1:
        temp = tempFn(k)

        newState = ng.generateRandomNeighbor(currentState)

        currStateEnergy = obF.apply(currentState)
        newStateEnergy = obF.apply(newState)

        if(Acceptance(currStateEnergy, newStateEnergy, temp) > r.random()):
            currentState = newState

        if(obF.apply(currentState) < best):
            best = obF.apply(currentState)

        k = k + 1

        print best

def go():
    obF = ObjectiveFunction(1, lambda(x): x[0] ** 2)
    ng = NeighborGenerator(obF, 5)

    temp = 1000
    coolingRate = 0.03
    maxIterations = 100

    tempFn = ExpoentialTemperature(temp)

    initialState = [50]
    currentState = initialState
    best = obF.apply(initialState)

    k = 0
    while temp > 1:
        temp = tempFn(k)

        newState = ng.generateRandomNeighbor(currentState)

        currStateEnergy = obF.apply(currentState)
        newStateEnergy = obF.apply(newState)

        if(Acceptance(currStateEnergy, newStateEnergy, temp) > r.random()):
            currentState = newState


        if(obF.apply(currentState) < best):
            best = obF.apply(currentState)

        k = k + 1

        print best


