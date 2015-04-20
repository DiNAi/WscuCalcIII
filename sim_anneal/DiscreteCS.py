# In [38]: ls = [ [1,-1], [1,-1] ]
# In [40]: [x for x in it.product(*ls)]
# Out[40]: [(1, 1), (1, -1), (-1, 1), (-1, -1)]


import numpy as np
import itertools as it
import frange as fr

class DimLimit(object):
    """minimum and maximum of a dimension"""

    def __init__(self, dimMin, dimMax):

        if(dimMin >= dimMax):
            raise Exception('max must be greater than min')

        self.dimMin = dimMin

        self.dimMax = dimMax


class DiscreteCS(object):
    """a discrete coordinate system in N dimensions"""

    def __init__(self, independentVarDimensions, independentVarDimensionLimits, stepSize):

        if independentVarDimensions != len(independentVarDimensionLimits):
            raise Exception('not all dimensions have limits')

        self.independentVarDimensions = independentVarDimensions

        self.independentVarDimensionLimits = independentVarDimensionLimits

        self.stepSize = stepSize


    def getAtDim(self, dim):
        dimMin = self.independentVarDimensionLimits[dim].dimMin
        dimMax = self.independentVarDimensionLimits[dim].dimMax

        return fr.frange(dimMin, dimMax, self.stepSize)


    def getProduct(self):

        dimensions = []

        for idx in range(0, self.independentVarDimensions):

            dimensions.append(self.getAtDim(idx))

        return it.product(*dimensions)


    def neighborIn1d(self, dim, value):

        limit = self.independentVarDimensionLimits[dim]

        assert value >= limit.dimMin and value < limit.dimMax

        if value == limit.dimMin:
            return [limit.dimMin + self.stepSize]

        elif value == limit.dimMax - self.stepSize:
            return [limit.dimMax - (2 * self.stepSize)]

        else:

            return [value - self.stepSize, value + self.stepSize]


    def getNeighbors(self, value):

        neighborsPerDimension = []

        for idx in range(0, self.independentVarDimensions):

            neighborsPerDimension.append(self.neighborIn1d(idx, value[idx]))

        return [x for x in it.product(*neighborsPerDimension)]


