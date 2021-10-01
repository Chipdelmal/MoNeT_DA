
from math import exp

def trapProbability(dist, A=1, b=1):
    prob = A * exp(-b * dist)
    return prob


def unifyTransitionsMatrix(BB, BQ, QB, QQ):
    (n, m) = (BB.shape[0], QQ.shape[0])
    psi = np.empty((n+m, n+m))
    # BB Section --------------------------------------------------------------
    for i in range(n):
        for j in range(n):
            psi[i, j] = BB[i, j]
    # BQ Section --------------------------------------------------------------
    for i in range(n):
        for j in range(m):
            psi[i, j + n] = BQ[j, i]
    # QB Section --------------------------------------------------------------
    for i in range(n):
        for j in range(m):
            psi[j+n, i] = QB[i, j]
    # QQ Section --------------------------------------------------------------
    for i in range(m):
        for j in range(m):
            psi[i+n, j+n] = QQ[i, j]
    return psi
