"""
Test minimal pour vérifier l'implémentation des algorithmes de l'article.
"""
import networkx as nx
from incremental_closeness_article import IncrementalClosenessArticle
from closeness import compute_all_closeness_classical

# Test sur un très petit graphe : 3 nœuds
print("=== TEST MINIMAL: 3 nœuds ===\n")

# Créer un graphe non orienté pour la référence
G_ref = nx.Graph()
G_ref.add_nodes_from([0, 1, 2])

# Créer l'incrémental vide
incr = IncrementalClosenessArticle()

# Ajouter les nœuds
print("1. Ajout des nœuds 0, 1, 2")
for i in range(3):
    incr.add_node(i)
print(f"   Closeness: {incr.get_all_closeness()}")

# Ajouter arête 0-1
print("\n2. Ajout arête 0--1")
G_ref.add_edge(0, 1)
incr.add_undirected_edge(0, 1)

c_ref = compute_all_closeness_classical(G_ref)
c_incr = incr.get_all_closeness()
print(f"   Classique   : {c_ref}")
print(f"   Incrémental : {c_incr}")

# Ajouter arête 0-2
print("\n3. Ajout arête 0--2")
G_ref.add_edge(0, 2)
incr.add_undirected_edge(0, 2)

c_ref = compute_all_closeness_classical(G_ref)
c_incr = incr.get_all_closeness()
print(f"   Classique   : {c_ref}")
print(f"   Incrémental : {c_incr}")

# Vérifier l'égalité
print("\n=== VÉRIFICATION ===")
max_diff = 0
for node in c_ref:
    diff = abs(c_ref[node] - c_incr.get(node, 0))
    if diff > max_diff:
        max_diff = diff
        
print(f"Différence maximale: {max_diff}")
print(f"Résultat: {'✓ CORRECT' if max_diff < 1e-9 else '✗ ERREUR'}")
