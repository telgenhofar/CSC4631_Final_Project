# Name
Aiden Telgenhof

# Project Overview
This repository contains the code for an epidemic simulator which uses opinion dynamics from DeGroot learning to propogate percieved risk across a social network. This percieved risk then causes individuals in the network to behave in certain ways which affect the way that the disease spread throughout the social network.

# Files
- degroot.py: contains the mathematical logic for the DeGroot learning model
- environment.py: contains the logic for creating a simulation environment
- main.py: the entry point for the simulator
- network_generator.py: contains the logic necessary for generating different kinds of graphical networks
- run_batch.py: secondary entry point which runs a number of simulations without the visualizer to produce data for comparison with SIR model
- SIR_model.py: secondary entry point which runs a number of simulations using the baseline SIR model to collect data for comparison to simulator
- visualizer.py: contains the logic for visualizing the disease and opinion graphs using the data from the environment

# Instructions for Compiling and Running
### main.py
Necessary libraries:
- numpy
- PyGame

Input parameters:
- h: shows help message
- m: graph type (small_world, fully_connected, random)
- n: number of nodes in network
- k: number of neighbors for small world graphs
- p: probability for node to rewire a neighbor in small world
- s: number of steps for simulation to run

Sample Input:
- python main.py -m random -n 100 -s 100
- python main.py -m small_world -n 100 -s 100 -k 5 -p 0.05

Output:
PyGame window showing simulation in real time and simulation.gif when PyGame window closes so that the most recent simulation can easily be viewed at any time.

### run_batch.py
Necessary libraries:
- numpy
- Matplotlib

Input parameters:
- h: shows help message
- m: graph type (small_world, fully_connected, random)
- n: number of nodes in network
- k: number of neighbors for small world graphs
- p: probability for node to rewire a neighbor in small world
- s: number of steps for simulation to run
- r: number of simulations to run
- base_inf_p: base infection probability

Sample Snput:
- python run_batch.py -m random -n 100 -s 100
- python run_batch.py -m small_world -n 100 -s 100 -k 5 -p 0.05 -r 200 --base_inf_p 0.05

Output:
Plot generated of distribution of runs and terminal output giving descriptive statistics.

### SIR_model.py
Necessary libraries:
- numpy
- Matplotlib

Sample Input:
- python SIR_model.py

Output:
Plot generated of distribution of runs and terminal output giving descriptive statistics.