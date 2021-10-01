
from math import exp

def trapProbability(dist, A=1, b=1):
    prob = A * exp(-b * dist)
    return prob