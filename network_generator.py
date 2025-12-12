"""
File: network_generator.py
Author: Aiden Telgenhof
Description: This file contains all of the logic necessary to create a graphical network. This was 
designed to be adaptable to any task which requires a graphical network to be generated. It also 
contains logic to create positions for each node so that they can easily be visualized within a 
PyGame window, but it should also work with any visualizer that uses PyGame-like coordinates.
"""
import random
import math

class NetworkGenerator:
    """
    Generates different types of networks and their positions so that
    the visualizer can create a proper representation of the graph
    """
    def __init__(self, n, mode="small_world", k=4, rewire_p=0.1):
        """
        Initializes the network generator
    
        :param n: The number of nodes
        :param mode: The type of graph to be generated
        :param k: for Small world graphs, number of neighbors for each node
        :param rewire_p: probability in small world graph for nodes to rewire connection
        to further away nodes to make graph traversal faster
        """
        self.n = n
        self.mode = mode
        self.k = k
        self.rewire_p = rewire_p

    def generate(self):
        """
        Generates a network based on the selected mode
        """
        if self.mode == "fully_connected":
            return self._generate_fully_connected()
        elif self.mode == "small_world":
            return self._generate_small_world()
        elif self.mode == "random":
            return self._generate_random()
        else:
            raise ValueError(f"Unknown mode {self.mode}")
    
    def _generate_fully_connected(self):
        """
        Generates a fully connected network
        """
        edges = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                edges.append((i, j))
        self.edges = edges
        positions = self._circle_layout()
        return edges, positions
    
    def _generate_random(self, p=0.1):
        """
        Generates a random network

        :param p: the probability of an edge being created between two nodes
        """
        edges = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                if random.random() < p:
                    edges.append((i, j))
        self.edges = edges
        positions = self._spring_layout()
        return edges, positions
    
    def _generate_small_world(self):
        """
        Generates a small world graph
        """
        edges = []

        deg = self.k
        if deg % 2 == 1:
            deg += 1

        for i in range(self.n):
            for j in range(1, deg//2 + 1):
                neighbor = (i + j) % self.n
                edges.append((i, neighbor))

        new_edges = []
        for (u, v) in edges:
            if random.random() < self.rewire_p:
                new_v = random.choice([x for x in range(self.n) if x != u])
                new_edges.append((u, new_v))
            else:
                new_edges.append((u, v))

        self.edges = edges
        positions = self._spring_layout()
        return new_edges, positions
    
    def _spring_layout(self, iterations=200, k=40, repulsion=50000):
        """
        Terrible code that is necessary for positions so that the visualizer
        doesn't just output a mess of datapoints. This code attempts to create graphs
        where neighbor points are closer together than they are with other points.
        """
        positions = {
            i: [random.uniform(50, 750), random.uniform(50, 550)] for i in range(self.n)
        }

        for _ in range(iterations):
            forces = {i: [0.0, 0.0] for i in range(self.n)}

            for i in range(self.n):
                xi, yi = positions[i]
                for j in range(i + 1, self.n):
                    xj, yj = positions[j]
                    dx = xi - xj
                    dy = yi - yj
                    dist2 = dx*dx + dy*dy + 0.01
                    dist = math.sqrt(dist2)

                    force = repulsion / dist2

                    fx = force * (dx / dist)
                    fy = force * (dy / dist)

                    forces[i][0] += fx
                    forces[i][1] += fy
                    forces[j][0] -= fx
                    forces[j][1] -= fy

            for (u, v) in self.edges:
                xu, yu = positions[u]
                xv, yv = positions[v]
                dx = xu - xv
                dy = yu - yv
                dist = math.sqrt(dx*dx + dy*dy) + 0.01

                force = (dist - k)

                fx = force * (dx / dist)
                fy = force * (dy / dist)

                forces[u][0] -= fx
                forces[u][1] -= fy
                forces[v][0] += fx
                forces[v][1] += fy

            for i in range(self.n):
                positions[i][0] += 0.03 * forces[i][0]
                positions[i][1] += 0.03 * forces[i][1]

                if math.isnan(positions[i][0]) or math.isnan(positions[i][1]):
                    positions[i][0] = random.uniform(100, 700)
                    positions[i][1] = random.uniform(100, 500)

                positions[i][0] = max(20, min(780, positions[i][0]))
                positions[i][1] = max(20, min(580, positions[i][1]))

        return {i: (positions[i][0], positions[i][1]) for i in range(self.n)}
    
    def _circle_layout(self, radius=250, center=(400, 300)):
        cx, cy = center
        positions = {}
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            positions[i] = (x, y)
        return positions