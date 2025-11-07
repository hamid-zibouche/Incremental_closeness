from graph import DynamicGraph
from closeness import compute_all_closeness_classical, save_closeness_to_file

def test_classical_closeness():
    """Test simple de l'algorithme classique"""
    
    # Créer un graphe simple
    g = DynamicGraph()
    
    # Ajouter des nœuds
    n0 = g.add_node(0)  # 0
    n1 = g.add_node(1)  # 1
    n2 = g.add_node(2)  # 2
    n3 = g.add_node(3)  # 3
    n4 = g.add_node(4)  # 4
    n5 = g.add_node(5)  # 5
    
    # Ajouter des arêtes : graphe en ligne 0-1-2-3
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)
    g.add_edge(0, 5)
    g.add_edge(2, 4)
    g.remove_node(5)
    
    print("Graphe créé:")
    print(f"Nœuds: {g.get_nodes()}")
    print(f"Arêtes: {g.get_edges()}")
    
    # Calculer la closeness
    closeness = compute_all_closeness_classical(g.G)
    
    print("\nCloseness Centrality:")
    for node in sorted(closeness.keys()):
        print(f"Nœud {node}: {closeness[node]:.4f}")
    
    # Afficher le graphe simple
    print("\n=== Affichage simple du graphe ===")
    g.visualize(title="Graphe")
    
    # Afficher le graphe avec les valeurs de closeness
    print("\n=== Affichage avec closeness centrality ===")
    g.visualize(closeness, title="Graphe avec Closeness Centrality")
    
    # Sauvegarder
    g.save_to_file("data/test_graph.txt")
    save_closeness_to_file(closeness, "data/test_closeness.txt")
    
    print("\nFichiers sauvegardés dans data/")

if __name__ == "__main__":
    test_classical_closeness()