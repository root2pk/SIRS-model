
"""
Methods used for all SIRS based simulations

"""
import numpy as np
import random

from typing import no_type_check
import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation

def check_absorb(lattice,lx,ly):
    """
    Function to check whether the lattice has reached an absorbing state

    """

    # At absorbing state, there are no infected sites
    for i in range(lx):
        for j in range(ly):
            if lattice[i][j] == 1:
                return False
    
    return True

def plot_lattice(lattice):
    """
    Function to plot the lattice using imshow()
    """
    plt.cla()
    im = plt.imshow(lattice.T, animated=True, origin='lower')
    plt.draw()
    plt.pause(0.0001)

def update_rule(lattice,itrial,jtrial,lx,ly,p1,p2,p3):
    r = random.random()

    # S to I
    if lattice[itrial,jtrial] == 0:
        if (nn_check(lattice,itrial,jtrial,lx,ly) == True):
            if r < p1:
                return True

    # I to R 
    elif lattice[itrial,jtrial] == 1:
        if r < p2:
            return True

    # R to S
    else:
        if r < p3:
            return True

    return False
    
def random_init(lx,ly):

    """
    Initialises a lx*ly lattice with random initial conditions
    (Equal probability of S,I and R)
    Takes in lx and ly
    Returns lattice
    
    """

    # Initialise spins randomly
    lattice = np.zeros((lx,ly),dtype = int)

    # Random
    for i in range(lx):
        for j in range(ly):

            r = random.random()
            if(r < 0.33):
                lattice[i,j] = 0           # 0 implies Susceptible (Purple)
            elif(r < 0.66):
                lattice[i,j] = 1           # 1 implies Infected (Green)
            else:
                lattice[i,j] = 2           # 2 implies Recovered (Yellow)

    return lattice

def nn_check(lattice,itrial,jtrial,lx,ly):
    """ 
    Function to check whether any of the nearest neighbours of the selected site are infected
    
    Returns True if there is an infected neighbour
    Returns False otherwise
    """
    if lattice[itrial,(jtrial+1)%ly] == 1 or lattice[itrial,(jtrial-1)%ly] == 1 or lattice[(itrial+1)%lx,jtrial] == 1 or lattice[(itrial-1)%lx,jtrial] == 1:
        return True
    else:
        return False

def num_infected(lattice,lx,ly):
    """
    Function to calculate the number infected sites in the lattice at any point of time

    """
    # Initialise count = 0
    count = 0

    # loop through lattice
    for i in range(lx):
        for j in range(ly):
            if lattice[i][j] == 1:
                count+=1
        
    return count

def resample(x, k, N):
    """
     Function to resample a list
     Takes in the list to be resampled x, number of resamples k, kT and number of sites N
     Returns a list of c values {c1,c2,c3...ck}
    """
    var_list = []
    for i in range(k):
        y = [random.choice(x) for element in x]                    # y is a resampled list of x
        y_sq = np.square(y)                                        # y_sq is square of y
        var = (np.mean(y_sq) - np.mean(y)**2)/N                      # Calculate c for the resampled list
        var_list.append(var)                                           # Add to list of c values

    # return list of c values
    return var_list

def set_immune(lattice,lx,ly,f_Im):
    """
    Function to set a certain fraction of sites in the lattice immune
    """
    for i in range(lx):
        for j in range(ly):
            r = random.random()
            if r < f_Im:                   
                lattice[i][j] = 3

    return lattice
