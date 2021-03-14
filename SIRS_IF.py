"""
Program to run the SIRS simulation for various values of immune fractions, with fixed p1,p2 and p3

Calculates Infected fraction for each immune fraction and stores it in a file
"""


import sys
import time
import random
import numpy as np

from typing import no_type_check
import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation

from methods_SIRS import random_init,nn_check,num_infected,update_rule, plot_lattice, check_absorb, set_immune


#############   MAIN FUNCTION   #######################

nstep = 1000              # Number of timesteps

# Input
if(len(sys.argv) != 5):
   print ("Usage python SIRS_IF.py N p1 p2 p3")
   sys.exit()

# Number of sites
lx = int(sys.argv[1]) 
ly = lx
N = lx*ly

# Probabilities
p1 = float((sys.argv[2]))
p2 = float((sys.argv[3]))
p3 = float((sys.argv[4]))

# Immune fraction ( list from 0.01 to 0.50 spacing of 0.01)
f_Im_list = np.around(np.linspace(0.01,0.50, num = 50),2)

# Set up files
f = open("Immune_frac.txt","w")

# To calculate time elapsed
start = time.time()

# Loop through Immune fraction list
for f_Im in f_Im_list:

    print("Immune fraction = " + str(f_Im))

    # List to store Infected fraction values
    I_list = []

    # Re initialise matrix
    lattice = random_init(lx,ly).copy()

    # Initialize some sites to be infected
    lattice = set_immune(lattice,lx,ly,f_Im)

    # Set up plot
    fig = plt.figure()

    # Plot first time
    plot_lattice(lattice)

    # Start Sweep        
    for n in range(nstep):  

        
        # Looping through lx*ly iterations (one sweep)
        for i in range(lx):
            for j in range(ly):
            
                # Select spin randomly
                itrial=np.random.randint(0,lx)
                jtrial=np.random.randint(0,ly)

                r = random.random()

                # S to I
                if lattice[itrial,jtrial] == 0:
                    if (nn_check(lattice,itrial,jtrial,lx,ly) == True):
                        if r < p1:
                            lattice[itrial,jtrial] = 1

                # I to R 
                elif lattice[itrial,jtrial] == 1:
                    if r < p2:
                        lattice[itrial,jtrial] = 2

                # R to S
                elif lattice[itrial,jtrial] == 2:
                    if r < p3:
                        lattice[itrial,jtrial] = 0

                # Immune stays immune
                else:
                    pass

        # Check if system has reached absorbing state
        if check_absorb(lattice,lx,ly) == True:
            I_list = [0]
            break

        # 100 steps Equilibriation time
        if n>100:                
            # Append value of infected fraction to list
            I_list.append(num_infected(lattice,lx,ly))

        if (n % 100 == 0):
            print(n)

        if n % 10 == 0:
            # Plot each 10 sweeps
            plot_lattice(lattice)

    # Calculate infected fraction for the run
    frac_I = np.mean(I_list)/N

    f.write('%0.2f %0.3f\n' %(f_Im,frac_I))

# Print time elapsed
print("Time Elapsed = {:.2f}s".format(time.time()-start))

