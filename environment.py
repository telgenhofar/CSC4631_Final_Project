import random

class Environment:
    def __init__(self, edges, positions, base_infection_p=0.1):
        self.edges = edges
        self.positions = positions
        self.base_p = base_infection_p

        self.num_nodes = len(positions)
        self.nodes = []

        self._init_nodes()

    def _init_nodes(self):
        for _ in range(self.num_nodes):
            node = {
                "innate_risk": random.uniform(0.2, 0.8),
                "opinion_risk": random.uniform(0.0, 1.0),
                "infected": False
            }
            self.nodes.append(node)

        patient_zero = random.randint(0, self.num_nodes - 1)
        self.nodes[patient_zero]["infected"] = True

    def step(self):
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
        n = self.nodes[dst]
        risk_factor = 0.5 * n["innate_risk"] + 0.5 * n["opinion_risk"]
        return self.base_p * risk_factor