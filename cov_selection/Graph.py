import numpy as np
import networkx as nx

#Used for simulating data

class Graph:
    def __init__(self, adj):
        self.adj = adj
        self.n = self.adj.shape[0]
        self.neighbours = np.copy(self.adj)
        np.fill_diagonal(self.neighbours, 0)
        self.neighbours = self.neighbours == 1
        self.non_neighbours = np.copy(self.adj)
        self.non_neighbours = self.non_neighbours == 0
        self.a = np.diag(np.full(self.adj.shape[0], 1)) != 1
        self.__generate_edges__()

    def sample(self, i):
        return np.random.multivariate_normal(np.zeros(self.n), self.cov, i)
    
    def __generate_edges__(self):
        # Extract edges as a list of tuples
        np.fill_diagonal(self.adj, 0)
        self.edges = []
        self.non_edges = []
        rows, cols = self.adj.shape
        for i in range(rows):
            for j in range(i+1, cols):  # Only look at the upper triangle
                if self.adj[i, j] == 1:  # If there's an edge
                    self.edges.append((i, j))
                    self.non_edges.append(np.setdiff1d(np.arange(self.adj.shape[0]), (i, j)))
        np.fill_diagonal(self.adj, 1)

class RandomGraph:
    def __init__(self, n, graph_structure='erdos_renyi', pd_selection='laplacian', d=0.2, k=2, p=0.2, seed=None):
        self.n = n
        self.d = d
        self.k = k 
        self.p = p
        self.graph_structure_name = graph_structure
        self.pd_selection = pd_selection
        self.seed = seed
        self.con = self.__generate_random_precision_matrix__()
        self.cov = np.linalg.inv(self.con)
        self.neighbours = np.copy(self.adj)
        np.fill_diagonal(self.neighbours, 0)
        self.neighbours = self.neighbours == 1
        self.non_neighbours = np.copy(self.adj)
        self.non_neighbours = self.non_neighbours == 0

        self.a = np.diag(np.full(self.adj.shape[0], 1)) != 1
        self.__generate_edges__()
        pass

    def __generate_random_precision_matrix__(self):
        # Generate a random graph
        if self.graph_structure_name == 'watts_strogatz':
            self.graph_structure = nx.watts_strogatz_graph(n=self.n,k=self.k, p=self.p, seed=self.seed)
        elif self.graph_structure_name == 'erdos_renyi':
            self.graph_structure = nx.erdos_renyi_graph(n=self.n, p=self.d, seed=self.seed)
        else:
            raise Exception("ERROR: Not a valid graph structure")

        # Construct concentration matrix
        self.adj = nx.adjacency_matrix(self.graph_structure).toarray()
        np.fill_diagonal(self.adj, 1)
        D = np.diag(self.adj.sum(axis=1))
        L = D-self.adj
        M = L + 0.3 * np.eye(self.n)
        return M
            
    
    def sample(self, i):
        return np.random.multivariate_normal(np.zeros(self.n), self.cov, i)
    
    def __generate_edges__(self):
        # Extract edges as a list of tuples
        np.fill_diagonal(self.adj, 0)
        self.edges = []
        self.non_edges = []
        rows, cols = self.adj.shape
        for i in range(rows):
            for j in range(i+1, cols):  # Only look at the upper triangle
                if self.adj[i, j] == 1:  # If there's an edge
                    self.edges.append((i, j))
                    self.non_edges.append(np.setdiff1d(np.arange(self.adj.shape[0]), (i, j)))
        np.fill_diagonal(self.adj, 1)
        
    
    def __repr__(self):
        if self.graph_structure_name == 'watts_strogatz':
            return f"G($|V|$={self.n}, WS(k={self.k},p={self.p}))"
        elif self.graph_structure_name == 'erdos_renyi':
            return f"G($|V|$={self.n}, ER(d={self.d}))"
        elif self.graph_structure_name == 'barabasi_albert':
            return f"G($|V|$={self.n}, BA(d={self.d}))"
        return f""










