__author__ = 'lukestack'
from numpy import square, mean, shape, matrix, transpose, array, hstack
import math
import random
import warnings


component_warning = "\nA number of components less than the number of components found in the training data was requested." \
                    "\n***Defaulted to number of components in training data***"


def factorize(v, components, process="mult", iterations=1000, threshold=.01, training_data=None):
    """
    Factorizes v into w and h.
    :param v: initial mixed signal matrix
    :param components: number of components to be extracted from v
    :param iterations: number of iterations for factorization
    :param threshold: distance that allows factorization to halt
    :param training_data: data to help with factorization of components
    :return: w and h (separated feature and weight matrices)
    """
    init_w, init_h = initialize_matrices(v, components, training_data)
    if process == "mult":
        w, h = multiplicative(v, init_w, init_h, iterations, threshold)
    else:
        raise Exception('Invalid nmf process')
    print "final distance:", difcost(v, w * h), "\n"
    return w, h


def initialize_matrices(v, components, training_data=None):
    """
    Initializes w and h with training data if present and random values from 0 to 1 for all remaining elements.
    :param v: initial mixed signal matrix
    :param components: number of components to be extracted from v
    :param training_data: data to help with factorization of components
    :return: initialized w and h matrices
    """
    ic = shape(v)[0]
    fc = shape(v)[1]

    if training_data is not None:
        w = None
        if components < training_data.shape[1]:
            components = training_data.shape[1]  # allows w and h matrices to be aligned
            warnings.warn(component_warning, UserWarning)
        for column in range(training_data.shape[1]):
            if w is None:
                w = training_data[:, column]
            else:
                w = hstack((w, training_data[:, column]))
        temp = matrix([[random.random() for j in range(components - w.shape[1])] for i in range(ic)])
        w = hstack((w, temp))
    else:
        w = matrix([[random.random() for j in range(components)] for i in range(ic)])
    h = matrix([[random.random() for j in range(fc)] for i in range(components)])
    print "w.shape:", w.shape
    print "h.shape:", h.shape
    return w, h


def multiplicative(v, w, h, iterations=1000, threshold=.01):
    """
    Uses multiplicative update rules for nmf
    :param v: initial mixed signal matrix
    :param w: initialized feature matrix
    :param h: initialized weight matrix
    :param iterations: number of iterations for factorization
    :param threshold: distance that allows factorization to halt
    :return: w and h (separated feature and weight matrices)
    """
    print "Using Multiplicative update rules for nmf"
    lcost = difcost(v, w * h)
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
    return w, h


def difcost(a, b):
    """
    Calculates the distance between two matrices
    :param a: first matrix
    :param b: second matrix
    :return: distance between a and b
    """
    diff = a - b
    dist = math.sqrt(mean(square(diff)))
    return dist