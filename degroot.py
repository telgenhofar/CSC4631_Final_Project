import numpy as np

class DeGrootModel:
    """
    A class which implements DeGroot social learning for a number of agents where
    each agent has their own opinion and level of trust in other agents
    """
    def __init__(self, num_nodes, trust_matrix=None, initial_opinions=None):
        """
        Initializes the DeGroot model
        
        :param num_nodes: Number of agents in the system
        :param trust_matrix: Matrix that denotes trust an agent places in another agent
        :param initial_opinions: Initial opinion vector representing each agent's opinion
        """
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
        """
        Normalizes each row of the trust matrix so that their sum is 1
        If a row sum is 0, it is treated as 1 to avoid division by 0
        """
        row_sums = self.W.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        self.W = self.W / row_sums

    def step(self):
        """
        Performs one step in the DeGroot model
        this is just multiplying the trust matrix and opinion vector
        """
        self.opinions = self.W @ self.opinions
        return self.opinions
    
    def set_opinion(self, i, value):
        """
        Sets opinion entry for a specific agent
        """
        self.opinions[i] = float(value)

    def get_opinion(self, i):
        """
        Gets the opinion of a specific agent
        """
        return float(self.opinions[i])

    def get_all_opinions(self):
        """
        Returns a copy of the opinion vector
        """
        return self.opinions.copy()