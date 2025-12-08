import random
from degroot import DeGrootModel
import numpy as np

VACCINATION_PROTECTION = 0.8
BASE_VAX_RATE = 0.01
OPINION_DECAY = 0.98
OPINION_INCREASE_PER_NEIGHBOR = 0.1

class Environment:
    def __init__(self, edges, positions, base_infection_p=0.1):
        self.edges = edges
        self.positions = positions
        self.base_p = base_infection_p

        self.num_nodes = len(positions)
        self.nodes = []
        self.adj = {i: [] for i in range(self.num_nodes)}

        self._build_graph()
        self._init_nodes()

        self.trust_matrix = self._create_trust_matrix()
        initial_opinions = [n["opinion_risk"] for n in self.nodes]
        self.degroot = DeGrootModel(self.num_nodes, trust_matrix=self.trust_matrix, initial_opinions=initial_opinions)

    def _init_nodes(self):
        for _ in range(self.num_nodes):
            node = {
                "innate_risk": random.uniform(0.2, 0.8),
                "opinion_risk": random.uniform(0.0, 0.1),
                "infected": False,
                "vaccinated": False
            }
            self.nodes.append(node)

        patient_zero = random.randint(0, self.num_nodes - 1)
        self.nodes[patient_zero]["infected"] = True

    def step(self):
        self.update_percieved_risk_from_infections()
        self.degroot.opinions = np.array([n["opinion_risk"] for n in self.nodes], dtype=float)
        updated_opinions = self.degroot.step()

        for i in range(self.num_nodes):
            self.nodes[i]["opinion_risk"] = float(updated_opinions[i])

        self._vaccinate()

        new_infections = []
        infected_edges = []

        for (u, v) in self.edges:
            u_inf = self.nodes[u]["infected"]
            v_inf = self.nodes[v]["infected"]

            if u_inf and not v_inf:
                p = self._transmission_p(u, v)
                if random.random() < p:
                    new_infections.append(v)
                    infected_edges.append((u, v))

            if v_inf and not u_inf:
                p = self._transmission_p(v, u)
                if random.random() < p:
                    new_infections.append(u)
                    infected_edges.append((v, u))

        for i in new_infections:
            self.nodes[i]["infected"] = True

        return infected_edges
    
    def _transmission_p(self, src, dst):
        node = self.nodes[dst]
        risk = node["innate_risk"]
        if node["vaccinated"]:
            risk *= (1 - VACCINATION_PROTECTION)
        return self.base_p * risk
    
    def _build_graph(self):
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
    
    def _create_trust_matrix(self):
        W = np.zeros((self.num_nodes, self.num_nodes))

        for i in range(self.num_nodes):
            neighbors = self.adj[i]
            if not neighbors:
                W[i, i] = 1.0
                continue
            
            trust_vals = np.random.uniform(0.1, 1.0, size=len(neighbors))

            for t, nbr in zip(trust_vals, neighbors):
                W[i, nbr] = t

            W[i, i] = np.random.uniform(0.2, 0.8)

        return W
        
    def _vaccinate(self):
        for node in self.nodes:
            if not node["vaccinated"]:
                p_vax = BASE_VAX_RATE * node["opinion_risk"]
                if random.random() < p_vax:
                    node["vaccinated"] = True

    def update_percieved_risk_from_infections(self):
        for i in range(self.num_nodes):
            infected_neighbors = sum(self.nodes[n]["infected"] for n in self.adj[i])
            if infected_neighbors == 0:
                self.nodes[i]["opinion_risk"] *= OPINION_DECAY
            else:
                increase = OPINION_INCREASE_PER_NEIGHBOR * infected_neighbors
                self.nodes[i]["opinion_risk"] += increase
            self.nodes[i]["opinion_risk"] = max(0.0, min(1.0, self.nodes[i]["opinion_risk"]))