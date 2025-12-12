"""
File: run_batch.py
Author: Aiden Telgenhof
Description: This file was created as a way of running the simulator a bunch of times
without the visualizer so that the simulations could run faster. This was useful
for finding the average number of infected in the simulator.
"""
import argparse
from network_generator import NetworkGenerator
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt

def run_single_sim(num_nodes, mode, k, rewire_p, steps, base_infection_p):
    gen = NetworkGenerator(num_nodes, mode=mode, k=k, rewire_p=rewire_p)
    edges, positions = gen.generate()

    env = Environment(edges, positions, base_infection_p=base_infection_p)

    infected_counts = []

    for _ in range(steps):
        infected_counts.append(sum(n["infected"] for n in env.nodes))
        env.step()

    return max(infected_counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, default="small_world",
                        choices=["small_world", "fully_connected", "random"])
    parser.add_argument("-n", "--nodes", type=int, default=30)
    parser.add_argument("-k", "--neighbors", type=int, default=4)
    parser.add_argument("-p", "--rewire", type=float, default=0.1)
    parser.add_argument("-s", "--steps", type=int, default=30)
    parser.add_argument("-r", "--runs", type=int, default=100)
    parser.add_argument("--base_inf_p", type=float, default=0.1)

    args = parser.parse_args()

    max_infected_list = []

    for i in range(args.runs):
        print(f"Run {i+1}/{args.runs}")
        max_inf = run_single_sim(
            num_nodes=args.nodes,
            mode=args.mode,
            k=args.neighbors,
            rewire_p=args.rewire,
            steps=args.steps,
            base_infection_p=args.base_inf_p
        )
        max_infected_list.append(max_inf)

    print("\n=== Results ===")
    print("Max infected across runs:")
    print(max_infected_list)
    print(f"\nMean max infected: {np.mean(max_infected_list):.2f}")
    print(f"Std dev: {np.std(max_infected_list):.2f}")

    plt.hist(max_infected_list, bins=20)
    plt.xlabel("Maximum infected in run")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    main()
