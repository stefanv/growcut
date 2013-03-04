""" Implementation of the grow-cut algorithm """

import numpy as np

np.set_printoptions(threshold=100000, precision=3)

import automata

#import ipdb


def g(x, maxC):
    """ Damping function """
    return 1. - ((x * 1.) / maxC)**1.5


def norm(x):
    """ L2 norm """
    #return np.sqrt(np.sum(np.power(x, 2)))
    return np.linalg.norm(x)


def numpyAutomate(coordinates, lum, edges, strength, label):
    """ Numpy based grow-cut """

    print coordinates[0].shape, coordinates[1].shape, '!'*100

    nextLabel = label.copy().flatten()
    nextStrength = strength.copy().flatten()

    CP = lum.flatten()
    CP_edge = edges.flatten()
    THETAP = strength.flatten()

    CQ = lum[coordinates]
    CQ_edge = edges[coordinates]
    THETAQ = strength[coordinates]
    LQ = label[coordinates]

    CPminusCQ = np.abs(np.vstack([CP] * CQ.shape[1]).T - CQ)
    CPminusCQ_edge = np.abs(np.vstack([CP_edge] * CQ_edge.shape[1]).T - CQ_edge)

    attackStrength = g(CPminusCQ, lum.max()) * THETAQ
    defendStrength = np.vstack([THETAP] * CQ.shape[1]).T * (1 + CPminusCQ_edge**3)

    growthMask = attackStrength > defendStrength
    cols = np.argmax(growthMask, axis=1)
    rows = np.arange(0, attackStrength.shape[0])
    mask = np.any(growthMask, axis=1)

    # Fill the new strengths
    nextLabel[mask] = LQ[rows[mask], cols[mask]]
    nextStrength[mask] = attackStrength[rows[mask], cols[mask]]

    return nextStrength.reshape(strength.shape), nextLabel.reshape(label.shape)


def automate(lum, strength, label):
    """ Grow-cut """

    nextLabel = label.copy()
    nextStrength = strength.copy()

    for point, (neighbourLum, neighbourStrength, neigbourLabel) in automata.iterGrids(
        (lum, strength, label), neighbours=automata.CONNECT_4
        ):

        cp = lum[point]
        thetap = strength[point]

        for cq, thetaq, lq in zip(neighbourLum, neighbourStrength, neigbourLabel):

            if g(norm(cp - cq), lum.max()) * thetaq > thetap:
                nextLabel[point] = lq
                nextStrength[point] = g(norm(cp - cq), lum.max()) * thetaq

    return nextStrength, nextLabel
