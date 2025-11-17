"""
Test minimaliste pour déboguer la suppression d'arête.
"""
import networkx as nx
from incremental_closeness_article import IncrementalClosenessArticle
from closeness import compute_all_closeness_classical

# Graphe simple : 0--1--3
#                  \\--2--4

G_ref = nx.Graph()
incr = IncrementalClosenessArticle()

print("=== CONSTRUCTION ===")
# Ajouter nœuds
for i in range(5):
    G_ref.add_node(i)
    incr.add_node(i)

# Ajouter arêtes
edges = [(0,1), (0,2), (1,3), (2,4)]
for u, v in edges:
    G_ref.add_edge(u, v)
    incr.add_undirected_edge(u, v)

print("Graphe initial:")
print(f"  Classique   : {compute_all_closeness_classical(G_ref)}")
print(f"  Incrémental : {incr.get_all_closeness()}")

print("\n=== SUPPRESSION 0--1 ===")
print("Avant suppression, distances depuis nœud 0:")
print(f"  D[0] = {incr.D[0]}")

# Supprimer 0--1 (non orienté = supprimer 0→1 ET 1→0)
G_ref.remove_edge(0, 1)
print("\nSuppression dans l'incrémental...")
incr.remove_undirected_edge(0, 1)

print("\nAprès suppression, distances depuis nœud 0:")
print(f"  D[0] = {incr.D[0]}")
print(f"  TotDist[0] = {incr.TotDist[0]}")

c_ref = compute_all_closeness_classical(G_ref)
c_incr = incr.get_all_closeness()

print("\nCloseness:")
print(f"  Classique   : {c_ref}")
print(f"  Incrémental : {c_incr}")

print("\nDifférences:")
for node in c_ref:
    diff = abs(c_ref[node] - c_incr[node])
    if diff > 1e-9:
        print(f"  Nœud {node}: diff={diff:.6f}  (ref={c_ref[node]:.4f}, incr={c_incr[node]:.4f})")
