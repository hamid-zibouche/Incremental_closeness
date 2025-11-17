"""
Implémentation de l'algorithme incrémental de closeness centrality
inspiré de Kas et al. (2013) et Ramalingam & Reps (1996).

Version qui identifie les sources affectées et ne recalcule que pour celles-ci.
"""
import networkx as nx
from collections import deque


class IncrementalCloseness:
    """
    Calcul incrémental de la closeness centrality sur un graphe non orienté.
    
    L'algorithme maintient une matrice de distances D[s][v] pour chaque source s
    et met à jour incrémentalement ces distances lors de l'ajout/suppression d'arêtes.
    """

    def __init__(self, G: nx.Graph):
        if G.is_directed():
            raise ValueError("Le graphe doit être non dirigé.")
        self.G = G
        
        # Distances D[x][y]
        self.D = {}
        self.sum_distances = {}
        self.closeness = {}
        
        # Initialiser pour tous les nœuds existants
        self._compute_initial_all_distances()

    def _compute_initial_all_distances(self):
        """Calcule D[x][y] pour tout x,y et les closeness."""
        # Réinitialiser les structures
        self.D = {x: {} for x in self.G.nodes()}
        self.sum_distances = {x: 0 for x in self.G.nodes()}
        self.closeness = {x: 0.0 for x in self.G.nodes()}
        
        # Calculer les distances pour chaque source
        for x in self.G.nodes():
            dist = self._bfs_from(x)
            self.D[x] = dist
            self.sum_distances[x] = sum(dist.values())
        
        # Calculer les closeness
        self._update_all_closeness()

    def _bfs_from(self, source):
        """BFS depuis une source pour calculer les distances."""
        dist = {source: 0}
        q = deque([source])
        while q:
            u = q.popleft()
            du = dist[u]
            for v in self.G.neighbors(u):
                if v not in dist:
                    dist[v] = du + 1
                    q.append(v)
        return dist

    def _update_closeness(self, x):
        """Met à jour la closeness d'un seul nœud."""
        if x not in self.sum_distances:
            self.closeness[x] = 0.0
            return
        
        sd = self.sum_distances[x]
        if sd == 0:
            self.closeness[x] = 0.0
            return

        reachable = len(self.D[x]) - 1  # -1 car on ne compte pas le nœud lui-même
        n = len(self.G.nodes())
        if n <= 1:
            self.closeness[x] = 0.0
            return

        # Formule NetworkX : (reachable / sum_distances) * (reachable / (n-1))
        self.closeness[x] = (reachable / sd) * (reachable / (n - 1))

    def _update_all_closeness(self):
        """Met à jour la closeness de tous les nœuds."""
        for x in self.G.nodes():
            self._update_closeness(x)

    def add_edge(self, u, v):
        """
        Ajoute une arête (u,v) et met à jour les distances incrémentalement.
        
        Algorithme inspiré de Kas et al.:
        1. Identifier les sources affectées (celles pour qui le chemin peut raccourcir)
        2. Recalculer les distances uniquement pour ces sources
        3. Si des composantes se connectent, faire un recalcul complet
        """
        if self.G.has_edge(u, v):
            return  # L'arête existe déjà
        
        self.G.add_edge(u, v)
        
        # Identifier les sources affectées selon l'algorithme de l'article
        affected_sources = set()
        
        for s in self.G.nodes():
            # Distance actuelle de s vers u et v
            du = self.D[s].get(u, float('inf'))
            dv = self.D[s].get(v, float('inf'))
            
            # Si la nouvelle arête (u,v) peut créer un chemin plus court:
            # - s -> u -> v (si d(s,u) + 1 < d(s,v))
            # - s -> v -> u (si d(s,v) + 1 < d(s,u))
            if du != float('inf') and du + 1 < dv:
                affected_sources.add(s)
            elif dv != float('inf') and dv + 1 < du:
                affected_sources.add(s)
        
        # Mettre à jour les distances pour les sources affectées
        if affected_sources:
            for s in affected_sources:
                # Recalculer via BFS pour cette source
                dist = self._bfs_from(s)
                self.D[s] = dist
                self.sum_distances[s] = sum(dist.values())
                self._update_closeness(s)
        else:
            # Cas où aucune source n'est "affectée" selon le critère ci-dessus
            # mais des composantes isolées peuvent s'être connectées
            # Dans ce cas, il faut recalculer pour tous
            needs_full_recompute = False
            for s in self.G.nodes():
                # Vérifier si s connaît tous les nœuds du graphe
                if s not in self.D or len(self.D[s]) < self.G.number_of_nodes():
                    needs_full_recompute = True
                    break
            
            if needs_full_recompute:
                self._compute_initial_all_distances()

    def remove_edge(self, u, v):
        """
        Supprime une arête (u,v) et met à jour les distances incrémentalement.
        
        Algorithme inspiré de Kas et al.:
        1. Identifier les sources affectées (celles dont un plus court chemin utilisait cette arête)
        2. Recalculer les distances uniquement pour ces sources
        """
        if not self.G.has_edge(u, v):
            return  # L'arête n'existe pas
        
        self.G.remove_edge(u, v)
        
        # Identifier les sources affectées selon l'algorithme de l'article
        affected_sources = set()
        
        for s in self.G.nodes():
            du = self.D[s].get(u, float('inf'))
            dv = self.D[s].get(v, float('inf'))
            
            # Si l'arête (u,v) était potentiellement sur un plus court chemin de s
            # Condition nécessaire : |d(s,u) - d(s,v)| == 1
            if abs(du - dv) == 1 and du != float('inf') and dv != float('inf'):
                affected_sources.add(s)
        
        # Recalculer les distances pour les sources affectées
        for s in affected_sources:
            dist = self._bfs_from(s)
            self.D[s] = dist
            self.sum_distances[s] = sum(dist.values())
            self._update_closeness(s)

    def get_closeness(self):
        """Retourne une copie du dictionnaire de closeness."""
        return self.closeness.copy()
