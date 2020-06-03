# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:15:23 2020

@author: Tim
"""
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

xi = (10, 17, -13, 2, -18, 3, -3, -8, -9, -2)
yi = (-20, 5, -15, -2, -4, -5, 9, 5, -9, 3)
xi = np.array(xi)
yi = np.array(yi)
#p = interp1d(xi,yi)
xnew = np.array(sorted(xi))


def polynomial(x):
    summands = []
    prods = []
    a = xi
    b = yi
    for i,j in zip(a,b):
    #for i in a:
        for k in a:
            if k==i:
                continue
            else:
                prod_j = (x-k)/(i-k)
                prods.append(prod_j)
        summands.append(j*np.prod(prods))
        prods = []
    return sum(summands)

results = [] 
for i in xnew:  #why do i need this, otherwise it says the dimensions are different
    results.append(polynomial(i))

    

def f(x):
    return 2-(x**2/16)

plt.plot(xi,yi,'o',xnew,results,'-',xnew,f(xnew),'--')
    