import numpy as np

class DeGrootModel:
    def __init__(self, num_nodes, trust_matrix=None, initial_opinions=None):
        self.n = num_nodes

        if initial_opinions is None:
            self.opinions = np.random.uniform(0.0, 1.0, size=self.n)
        else:
            self.opinions = np.array(initial_opinions, dtype=float)

        if trust_matrix is None:
            self.W = np.eye(self.n)
        else:
            self.W = np.array(trust_matrix, dtype=float)
            self._normalize_rows()
    
    def _normalize_rows(self):
        row_sums = self.W.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        self.W = self.W / row_sums

    def step(self):
        self.opinions = self.W @ self.opinions
        return self.opinions
    
    def set_opinion(self, i, value):
        self.opinions[i] = float(value)

    def get_opinion(self, i):
        return float(self.opinions[i])

    def get_all_opinions(self):
        return self.opinions.copy()