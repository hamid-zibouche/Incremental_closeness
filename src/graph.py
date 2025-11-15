import networkx as nx
import matplotlib.pyplot as plt

class DynamicGraph:
    """Classe pour gérer un graphe dynamique"""
    
    def __init__(self):
        self.G = nx.Graph()
        self.node_counter = 0  # Pour générer des IDs uniques
    
    def add_node(self,tag):
        """Ajoute un nouveau nœud"""
        node_id = self.node_counter
        self.G.add_node(tag)
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


    
    def visualize(self, closeness_values=None, save_path=None, title="Graphe"):
        """
        Affiche le graphe avec matplotlib
        
        Args:
            closeness_values: dict optionnel {node: closeness} pour colorer les nœuds
            save_path: chemin pour sauvegarder l'image (optionnel)
            title: titre du graphe
        """
        plt.figure(figsize=(10, 8))
        
        # Calculer la disposition des nœuds
        pos = nx.spring_layout(self.G, seed=42)  # Layout force-directed
        
        # Si on a des valeurs de closeness, on colore selon ces valeurs
        if closeness_values:
            node_colors = [closeness_values.get(node, 0) for node in self.G.nodes()]
            
            # Dessiner les nœuds avec une échelle de couleurs
            nodes = nx.draw_networkx_nodes(
                self.G, pos,
                node_color=node_colors,
                node_size=700,
                cmap=plt.cm.YlOrRd,  # Palette jaune-orange-rouge
                vmin=min(node_colors),
                vmax=max(node_colors)
            )
            
            # Ajouter une barre de couleur
            plt.colorbar(nodes, label='Closeness Centrality')
        else:
            # Dessiner les nœuds avec une couleur unique
            nx.draw_networkx_nodes(
                self.G, pos,
                node_color='lightblue',
                node_size=700
            )
        
        # Dessiner les arêtes
        nx.draw_networkx_edges(self.G, pos, alpha=0.5, width=2)
        
        # Ajouter les labels des nœuds
        nx.draw_networkx_labels(self.G, pos, font_size=12, font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')  # Masquer les axes
        plt.tight_layout()
        
        # Sauvegarder si demandé
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graphe sauvegardé dans: {save_path}")
        
        plt.show()
    
    def visualize_simple(self, title="Graphe"):
        """Affichage simple et rapide du graphe"""
        plt.figure(figsize=(8, 6))
        nx.draw(self.G, with_labels=True, node_color='lightblue', 
                node_size=700, font_size=12, font_weight='bold',
                edge_color='gray', width=2, alpha=0.7)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def visualize_interactive(self, closeness_values=None, output_path="graph_interactive.html", physics=True):
        """Génère une visualisation interactive (drag & zoom) avec PyVis.

        Args:
            closeness_values (dict|None): valeurs par nœud pour modifier taille/couleur.
            output_path (str): chemin du fichier HTML généré.
            physics (bool): activer le moteur physique (layout dynamique).

        Résultat:
            Fichier HTML interactif ouvrable dans un navigateur.
        """
        try:
            from pyvis.network import Network
        except ImportError:
            print("PyVis n'est pas installé. Installez-le avec: pip install pyvis")
            return

        net = Network(height="750px", width="100%", directed=False, notebook=False, bgcolor="#000000", font_color="#FFFFFF")
        net.toggle_physics(physics)

        # Préparer normalisation pour la taille/couleur si closeness fourni
        if closeness_values and len(closeness_values) > 0:
            vals = [v for v in closeness_values.values() if isinstance(v, (int, float))]
            if len(vals) == 0:
                vmin = vmax = 0.0
            else:
                vmin, vmax = min(vals), max(vals)
            span = (vmax - vmin) if vmax != vmin else 1.0
        else:
            vmin = 0.0
            vmax = 1.0
            span = 1.0

        for n in self.G.nodes():
            if closeness_values:
                raw = closeness_values.get(n, vmin)
                norm = (raw - vmin) / span
                size = 15 + norm * 35  # taille entre 15 et 50
                # Couleur gradient bleu->rouge
                r = int(255 * norm)
                b = int(255 * (1 - norm))
                g = 80
                color = f"rgb({r},{g},{b})"
                title = f"Noeud {n}<br>Closeness={raw:.5f}"
            else:
                size = 20
                color = "#66b3ff"
                title = f"Noeud {n}"
            net.add_node(str(n), label=str(n), title=title, color=color, size=size)

        for u, v in self.G.edges():
            net.add_edge(str(u), str(v))

        # PyVis attend une chaîne JSON valide (pas de 'const options =').
        options = {
            "interaction": {"hover": True, "zoomView": True, "dragView": True},
            "nodes": {"borderWidth": 1, "shape": "dot"},
            "edges": {"color": {"color": "#ADADAD"}, "smooth": True},
            "physics": {"stabilization": {"iterations": 120}}
        }
        import json
        net.set_options(json.dumps(options))

        # Générer le HTML
        net.save_graph(output_path)
        print(f"Visualisation interactive générée: {output_path}")