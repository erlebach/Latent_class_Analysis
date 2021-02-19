import numpy as np
import numpy.random as npr
import scipy.stats as stats

#-----------------------------------------
def generateAllObservations(N, pi, pkc, G):
    # pkc[G, K], G groups/classes, K attributes for each observable

    rows = np.zeros([G, N, K])

    # VERY INEFFICIENT
    for g in range(G):
        for n in range(N):
            for k in range(K):
                p = pkc[g, k]
                rv = stats.bernoulli.rvs(p, size=1)
                rows[g, n, k] = rv[0]

    # Each group is chosen according to pi
    # I can change alpha0 in different experiments

    alpha0 = 1.
    alpha = [alpha0] * G   # uniform
    pi = npr.dirichlet(alpha)
    choice = npr.choice(G, size=N, replace=True, p=pi)
    
    new_rows = np.zeros([N, K])

    for n in range(N):
        for k in range(K):
            new_rows[n,k] = rows[choice[n], n, k]

    return new_rows

#-----------------------------------------
def generateAllObservationsEfficient(N, pi, pkc, G):
    # More efficient version of generateAllObservations
    # pkc[G, K], G groups/classes, K attributes for each observable

    rows = np.zeros([G, N, K])

    # The kth attribute is attached to the kth Bernoulli variable
    # Generate Bernouilli variables column by column

    rvs = {}

    for g in range(G):
        for k in range(K):
            p = pkc[g,k]
            rvs[g,k] = stats.bernoulli.rvs(p, size=N)
            rows[g,:,k] = rvs[g,k]

    alpha0 = 1.
    alpha = [alpha0] * G   # uniform
    pi = npr.dirichlet(alpha)
    choice = npr.choice(G, size=N, replace=True, p=pi)
    
    new_rows = np.zeros([N, K])

    for n in range(N):
        for k in range(K):
            new_rows[n,k] = rows[choice[n], n, k]

    return new_rows

#----------------------------------------------------------

def computeFrequencies(izeros, G):
    # Computer frequencies
    freq = np.zeros(G)
    for g in range(G):
        freq[g] = np.where(izeros == g)[0].size
    freq = freq / np.sum(freq)


if __name__ == "__main__":
    # Nb observations (i)
    N = 500
    
    # Nb groups (G)
    G = 4
    
    # Nb attributes (K)
    K = 7 
    
    # Store Class probabilities
    alpha = [1.] * G   # uniform
    pi = npr.dirichlet(alpha)
    pi_cum = np.cumsum(pi)
    print(pi_cum)
    
    # Bernouilli variables [G x K]
    pkc = npr.beta(1,1,(G,K))  # uniform   ## IS THIS CORRECT?
    
    # Very inefficient, but likely correct
    # 14s for 10,000 observations
    #generateAllObservations(N, pi, pkc, G)

    # Much more efficient
    # 0.9s for 10,000 observations
    # 1.2s for 100,000 observations
    data = generateAllObservationsEfficient(N, pi, pkc, G)
    np.save("synthetic_data.npy", data)

