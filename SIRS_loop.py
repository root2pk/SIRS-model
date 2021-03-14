"""
Program to run the SIRS model in a loop with vaired p1 and p3 values to obtain phase data and cut along a phase line 

Writes data to file
"""



import sys
import time
import random
import numpy as np

from typing import no_type_check
import matplotlib
from numpy.core.numeric import array_equal
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation

from methods_SIRS import random_init,nn_check,num_infected,resample,check_absorb,plot_lattice

#############   MAIN FUNCTION   #######################

nstep = 1000              # Number of timesteps


# Number of sites
lx = 50
ly = lx
N = lx*ly

# Probabilities
# p1_list = np.around(np.linspace(0.2,0.5,31),2)
p1_list = [0.90]
p2 = 0.5
# p3_list = np.around(np.linspace(0,1,21),2)
p3_list = [0.80]
 
# Set up files
f = open("Phase_data.txt","w")

# To calculate time elapsed
start = time.time()

# Initialise lattice with random initial conditions
lattice = random_init(lx,ly).copy()

# Loop through all the p1 and p3 values

for p1 in p1_list:
    for p3 in p3_list:

        print("p1 = " + str(p1) + ", p3 = " + str(p3))
        # Set up lists to put data
        I_list = []

        lattice = random_init(lx,ly).copy()

        # Set up plot
        fig = plt.figure()

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
                    else:
                        if r < p3:
                            lattice[itrial,jtrial] = 0
                
            if (n % 100 == 0):
                print(n)

            if (n % 10 == 0):
                # Plot every 10 sweeps 
                plot_lattice(lattice)
                
            
            # Check if absorbing phase has been reached
            if check_absorb(lattice,lx,ly) == True:
                I_list = [0]
                break

            # Equilibration time = 100 sweeps
            if n>100:
                I_list.append(num_infected(lattice,lx,ly))

        # Calculations of <I>,<I^2> and variance

        I_sq_list = np.square(I_list)
        I_mean = np.mean(I_list)
        I_sq_mean = np.mean(I_sq_list)

        # Required Quantities
        var_I = (I_sq_mean - I_mean**2)/N
        frac_I = I_mean/N

        ###### Error in variance of infected fraction (Resampling using bootstrap method) ################

        var_list = resample(I_list, 100, N)
        err = np.std(var_list)

        f.write('%0.2f %0.2f %0.3f %0.3f %0.3f\n' %(p1,p3,frac_I,var_I,err))


f.close()
# Print time elapsed

print("Time Elapsed = {:.2f}s".format(time.time()-start))


