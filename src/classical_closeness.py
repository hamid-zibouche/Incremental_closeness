import networkx as nx
from collections import deque

def bfs_distances(graph, source):
    """
    BFS pour calculer les distances depuis source vers tous les autres nœuds
    
    Args:
        graph: networkx.Graph
        source: nœud source
    
    Returns:
        dict: {node: distance}
    """
    distances = {source: 0}
    queue = deque([source])
    
    while queue:
        current = queue.popleft()
        current_dist = distances[current]
        
        for neighbor in graph.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return distances


def compute_closeness_centrality(graph, node):

    if graph.number_of_nodes() <= 1:
        return 0.0
    
    distances = bfs_distances(graph, node)
    
    # Nombre de nœuds atteignables (excluant le nœud lui-même)
    reachable = len(distances) - 1  # -1 pour exclure le nœud source
    
    if reachable == 0:
        return 0.0
    
    # Somme des distances (en excluant la distance à soi-même qui est 0)
    total_distance = sum(distances.values())
    
    if total_distance == 0:
        return 0.0
    
    # Closeness normalisée : (nombre de nœuds atteignables) / somme des distances
    # Puis on normalise par (n-1) pour avoir une valeur entre 0 et 1
    closeness = reachable / total_distance
    
    n = graph.number_of_nodes()
    if n > 1:
        closeness = closeness * (reachable / (n - 1))
    
    return closeness


def compute_all_closeness_classical(graph, verbose=False):
    """
    Calcule la closeness centrality de TOUS les nœuds avec l'algo classique
    
    """
    closeness = {}
    nodes = list(graph.nodes())
    total = len(nodes)
    
    for i, node in enumerate(nodes, 1):
        closeness[node] = compute_closeness_centrality(graph, node)
        if verbose and i % 20 == 0:  # Afficher tous les 20 nœuds
            print(f"  Progression: {i}/{total} nœuds traités ({100*i/total:.1f}%)")
    
    if verbose and total > 0:
        print(f"  Terminé: {total}/{total} nœuds traités (100.0%)")
    
    return closeness


def save_closeness_to_file(closeness_dict, filename):
    """
    Sauvegarde les valeurs de closeness dans un fichier
    Ligne j contient la closeness du nœud j
    
    Args:
        closeness_dict: {node: closeness_value}
        filename: nom du fichier de sortie
    """
    if not closeness_dict:
        return
    
    max_node = max(closeness_dict.keys())
    
    with open(filename, 'w') as f:
        for node in range(max_node + 1):
            value = closeness_dict.get(node, 0.0)
            f.write(f"{value}\n")