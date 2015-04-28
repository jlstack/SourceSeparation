__author__ = 'lukestack'
from numpy import square, mean, shape, matrix, transpose, array, hstack
import math
import random


def difcost(a, b):
    diff = a - b
    dist = math.sqrt(mean(square(diff)))
    return dist


def factorize(v, pc=10, iterations=1000, threshold=.01, models=None):
    ic = shape(v)[0]
    fc = shape(v)[1]
    # Initialize the weight and feature matrices with random values
    h = matrix([[random.random() for j in range(fc)] for i in range(pc)])
    if models is not None:
        w = None
        for i in range(pc):
            model = random.choice(models)
            column = random.randint(0, model.shape[1] - 1)
            if w is None:
                w = model[:,column]
            else:
                w = hstack((w, model[:, column]))
    else:
        w = matrix([[random.random() for j in range(pc)] for i in range(ic)])
    print "w.shape:", w.shape
    lcost = difcost(v, w*h)
    print "starting cost: ", lcost
    for i in range(iterations):
        w += 10 ** -9
        h += 10 ** -9
        if i % 100 == 0 and i > 0:
            wh = w * h
            # Calculate the current difference
            cost = difcost(v, wh)
            print "iteration:", i, "cost:", cost
            # Terminate if the matrix has been fully factorized
            if abs(cost - lcost) < threshold:
                break
            else:
                lcost = cost
        # Update feature matrix
        hn = (transpose(w) * v)
        hd = (transpose(w) * w * h)

        h = matrix(array(h) * array(hn) / (array(hd) + (1 ** -10)))

        # Update weights matrix
        wn = (v * transpose(h))
        wd = (w * h * transpose(h))

        w = matrix(array(w) * array(wn) / array(wd))
    print "\nshapes of w and h:", w.shape, h.shape
    print "final distance:", difcost(v, w*h), "\n"
    return w, h