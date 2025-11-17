"""
Test de débogage pour voir où l'algorithme diverge.
"""
import networkx as nx
from incremental_closeness_article import IncrementalClosenessArticle
from closeness import compute_all_closeness_classical

def compare_at_step(step_name, G_ref, incr):
    """Compare les closeness à une étape donnée."""
    c_ref = compute_all_closeness_classical(G_ref)
    c_incr = incr.get_all_closeness()
    
    print(f"\n{step_name}")
    print(f"  Classique   : {c_ref}")
    print(f"  Incrémental : {c_incr}")
    
    # Vérifier différences
    max_diff = 0
    diff_node = None
    for node in c_ref:
        diff = abs(c_ref[node] - c_incr.get(node, 0))
        if diff > max_diff:
            max_diff = diff
            diff_node = node
    
    if max_diff > 1e-9:
        print(f"  ⚠️  DIFFÉRENCE max={max_diff:.6f} pour nœud {diff_node}")
        return False
    else:
        print(f"  ✓ CORRECT")
        return True

# Test avec quelques opérations
print("=== TEST DEBUG: Séquence complète ===")

G_ref = nx.Graph()
incr = IncrementalClosenessArticle()

# Ajouter 5 nœuds
print("\n1. Ajout de 5 nœuds")
for i in range(5):
    G_ref.add_node(i)
    incr.add_node(i)
compare_at_step("Après ajout nœuds", G_ref, incr)

# Ajouter quelques arêtes
print("\n2. Ajout arêtes 0-1, 0-2, 1-3, 2-4")
edges = [(0,1), (0,2), (1,3), (2,4)]
for u, v in edges:
    G_ref.add_edge(u, v)
    incr.add_undirected_edge(u, v)
compare_at_step("Après ajout arêtes", G_ref, incr)

# Supprimer une arête
print("\n3. Suppression arête 0-1")
G_ref.remove_edge(0, 1)
incr.remove_undirected_edge(0, 1)
compare_at_step("Après suppression arête 0-1", G_ref, incr)

# Supprimer un nœud
print("\n4. Suppression nœud 4")
G_ref.remove_node(4)
incr.remove_node(4)
compare_at_step("Après suppression nœud 4", G_ref, incr)

print("\n=== FIN ===")
