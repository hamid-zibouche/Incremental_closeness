import networkx as nx

class DynamicGraph:
    """Classe pour gérer un graphe dynamique"""
    
    def __init__(self):
        self.G = nx.Graph()
        self.node_counter = 0  # Pour générer des IDs uniques
    
    def add_node(self):
        """Ajoute un nouveau nœud"""
        node_id = self.node_counter
        self.G.add_node(node_id)
        self.node_counter += 1
        return node_id
    
    def remove_node(self, node_id):
        """Supprime un nœud"""
        if node_id in self.G:
            self.G.remove_node(node_id)
            return True
        return False
    
    def add_edge(self, u, v):
        """Ajoute une arête entre u et v"""
        if u in self.G and v in self.G and u != v:
            self.G.add_edge(u, v)
            return True
        return False
    
    def remove_edge(self, u, v):
        """Supprime une arête entre u et v"""
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            return True
        return False
    
    def get_nodes(self):
        """Retourne la liste des nœuds"""
        return list(self.G.nodes())
    
    def get_edges(self):
        """Retourne la liste des arêtes"""
        return list(self.G.edges())
    
    def number_of_nodes(self):
        return self.G.number_of_nodes()
    
    def number_of_edges(self):
        return self.G.number_of_edges()
    
    def save_to_file(self, filename):
        """Sauvegarde le graphe dans un fichier"""
        with open(filename, 'w') as f:
            f.write(f"{self.number_of_nodes()} {self.number_of_edges()}\n")
            for u, v in self.get_edges():
                f.write(f"{u} {v}\n")
    
    def load_from_file(self, filename):
        """Charge un graphe depuis un fichier"""
        self.G.clear()
        with open(filename, 'r') as f:
            first_line = f.readline().strip().split()
            n_nodes, n_edges = int(first_line[0]), int(first_line[1])
            
            # Ajouter les nœuds
            for i in range(n_nodes):
                self.G.add_node(i)
            
            # Ajouter les arêtes
            for line in f:
                u, v = map(int, line.strip().split())
                self.G.add_edge(u, v)