import numpy as np
from cov_selection.common import ncd_blocks
import time

def NCD(emp_cov, G, n):
    # this value needs to be
    # positive definite in order
    # to guarantee convergences
    s = np.copy(emp_cov)
    for _ in range(n):
        for u in range(s.shape[0]):
            b = G.neighbours[u,:]
            r = G.non_neighbours[u,:]
            if np.all(b == False):
                tmp_ru = np.array([[0]])
                tmp_ur = tmp_ru
            else:
                uu, ub, bu, ur, ru, br, rb, rr, bb = ncd_blocks(s,u,G)
                tmp_ru = rb @ (np.linalg.inv(bb) @ bu)
                tmp_ur = tmp_ru.T
            s[r,u] = tmp_ru
            s[u,r] = tmp_ur
    return s

