"""
File: main.py
Author: Aiden Telgenhof
Description: This file serves as the primary entrypoint for the simulator program, it handles user
input as well as creating all of the proper initialization steps to get a simulation running.
"""
import argparse
from network_generator import NetworkGenerator
from environment import Environment
from visualizer import Visualizer

def main():
    """
    Entry point for the main simulator program
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", type=str, default="small_world",
                        choices=["small_world", "fully_connected", "random"])
    parser.add_argument("-n", "--nodes", type=int, default=30)
    parser.add_argument("-k", "--neighbors", type=int, default=4)
    parser.add_argument("-p", "--rewire", type=float, default=0.1)
    parser.add_argument("-s", "--steps", type=int, default=30)

    args = parser.parse_args()

    print("Generating network...")
    gen = NetworkGenerator(args.nodes, mode=args.mode, k=args.neighbors, rewire_p=args.rewire)
    edges, positions = gen.generate()

    print("Creating environment...")
    env = Environment(edges, positions)

    print("Starting visualization...")
    vis = Visualizer(env, positions, edges)
    vis.run_simulation(steps=args.steps)

if __name__ == "__main__":
    main()