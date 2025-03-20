import numpy as np
import time

def IPS(s, G, n):
    sigma = np.eye(s.shape[0]) * s
    K = np.linalg.inv(sigma)
    # it can take a long time to converge
    for _ in range(n):
        for c in G.edges:
            a = np.setdiff1d(np.arange(s.shape[0]), c)
            cc = np.ix_(c,c)
            ac = np.ix_(a,c)
            ca = np.ix_(c,a)
            aa = np.ix_(a,a)
            # update K
            L = K[cc] - np.linalg.inv(sigma[cc])
            K[cc] = np.linalg.inv(s[cc]) + L

            # update sigma
            sig_ac = sigma[ac]
            sig_ca = sigma[ca]
            sigma_cc_inv = np.linalg.inv(sigma[cc])
            sigma[ca] = s[cc] @ (sigma_cc_inv @ sig_ca)
            sigma[ac] = sigma[ac] @ (sigma_cc_inv @ s[cc])
            H = sigma_cc_inv -  sigma_cc_inv @ (s[cc] @ sigma_cc_inv)
            sigma[aa] = sigma[aa]- (sig_ac @ (H @ sig_ca))
            sigma[cc] = s[cc]
    return (sigma, K)
