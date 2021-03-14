"""
Program to simulate SIRS model for a given value of p1,p2 and p3

"""


import sys
import time
import random
import numpy as np

from typing import no_type_check
import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from methods_SIRS import random_init,nn_check,num_infected,update_rule,check_absorb, plot_lattice


#############   MAIN FUNCTION   #######################

nstep = 1000              # Number of timesteps

# Input
if(len(sys.argv) != 5):
   print ("Usage python SIRS.py N p1 p2 p3")
   sys.exit()

# Number of sites
lx = int(sys.argv[1]) 
ly = lx
N = lx*ly

# Probabilities
p1 = float((sys.argv[2]))
p2 = float((sys.argv[3]))
p3 = float((sys.argv[4]))

# To calculate time elapsed
start = time.time()

# Initialise sites randomly
lattice = random_init(lx,ly)

# Set up plot
fig = plt.figure()

# Draw first plot
plot_lattice(lattice)

# Start Sweep        
for n in range(nstep):

    # Looping through lx*ly iterations (one sweep)
    for i in range(lx):
        for j in range(ly):
        
            # Select spin randomly
            itrial=np.random.randint(0,lx)
            jtrial=np.random.randint(0,ly)

            if update_rule(lattice, itrial, jtrial, lx, ly, p1, p2, p3) == True:    
                lattice[itrial,jtrial] = (lattice[itrial,jtrial] + 1) % 3
      
    if check_absorb(lattice,lx,ly) == True:
        break
    if (n % 10 == 0):
        print(n)

        # Plot each 10 sweeps
        plot_lattice(lattice)


# Print time elapsed
print("Time Elapsed = {:.2f}s".format(time.time()-start))

