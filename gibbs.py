
import numpy as np
import numpy.random as npr
import scipy.stats as stats


# I do not want to specify nb iterations in advance

#----------------------------------------------------------
def setupArrays(gdict, nb_iter):
    gdict['Pi'] = np.zeros([nb_iter, G])   # class membership
    gdict['Pjk'] = np.zeros([nb_iter, G, K]) # item resp prob
    gdict['Cij'] = np.zeros([nb_iter, N, G])  # discrete classes
    gdict['Cij_pr'] = np.zeros([nb_iter, N, G])  # latent class prob
    gdict['label_stor'] = np.zeros([nb_iter, G]) # relabeling (what for??)

    ## Simulated prameters pjk, C, at iteration t+1
    pjk_t1 = np.zeros([G, K]) # latest p_jk^(t+1)
    # People by group: matrix of each person's class membership probability
    Clp_t1 = np.zeros([N, G]) # 

    ## Priors
    dirichlet_prior = [1.] * G  # flat

    alpha = 1.
    beta = 1.

    start_pi = npr.dirichlet(dirichlet_prior)

    # Not clear why we do not generate them all at once
    start_item_p = np.zeros([G, K]) 
    for g in range(G):
        start_item_p[g,:] = npr.beta(alpha, beta, K)
        print(start_item_p[g])

    # More efficient
    start_item_p = npr.beta(alpha, beta, [G,K])

    # Address lbel switch problem
    # NOT IMPLEMENTED. Line 53 in Li's code

    trace_num = 0  # trace of match between t0 and t+1  (????)

    print("The end!!")

#-----------------------------------------------------
def GibbsSingleStep():
    pass

def GibbsBurn(nb_iter):
    for i in range(nb_iter):
        RBibbsSingleStep()

def GibbsSample(nb_iter, nb_thin):
    for i in range(nb_iter):
        if not(nb_iter % nb_thin):
            Pi, Pjk = GibbsSingleStep()
            updateMean(PiMean, PjkMean, Pi, Pjk)

    return PiMean, PjkMean
# Additional arrays to return: Cpr.chain, Pjk.chain, Pi.chain if needed

# ---------------------------------------------------
if __name__ == "__main__":
    data = np.load("synthetic_data.npy")
    N, K = data.shape    # nb observations
    G = 4  # A guess (which happens to be correct)


    gdict = {}
    setupArrays(gdict, nb_iter=100)

 
