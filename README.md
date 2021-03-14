# SIRS-model
Modelling and visualisation of the Susceptible, Infectious, Recovered (SIRS) compartmental model for spread of infectious diseases


SIRS.py simulates SIRS for a given p1, p2 and p3
Usage "python SIRS.py N p1 p2 p3"

SIRS_loop.py simulates SIRS for a range of p1 and p3 values, with fixed p2 = 0.5
Writes data to "Phase_data.txt"

SIRS_IF.py simulates SIRS for various values of immune fraction, and computes infected fraction
Usage "python SIRS_IF.py N p1 p2 p3"
Writes data to "Immune_frac.txt"

methods_SIRS.py contains all the methods used for SIRS simulation
