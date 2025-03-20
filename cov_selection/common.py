import numpy as np

def ncd_blocks(s, u, G):
    b = G.neighbours[u,:]
    r = G.non_neighbours[u,:]
    uu = s[u,u]
    ub = s[u, b]
    bu = s[b,:][:,u]
    ur = s[u, r]
    ru = s[r,:][:,u]
    rr = s[r,:][:,r]
    bb = s[b,:][:,b]
    br = s[b,:][:,r]
    rb = s[r,:][:,b]
    return uu, ub, bu, ur, ru, br, rb, rr, bb

