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
    """
    Calcule la closeness centrality d'un nœud
    
    Formule: CC(x) = 1 / Σ d(x,y) pour tous y ≠ x
    
    Args:
        graph: networkx.Graph
        node: nœud dont on calcule la closeness
    
    Returns:
        float: closeness centrality du nœud
    """
    if graph.number_of_nodes() <= 1:
        return 0.0
    
    distances = bfs_distances(graph, node)
    
    # Vérifier si le graphe est connexe depuis ce nœud
    if len(distances) < graph.number_of_nodes():
        # Graphe non connexe : on peut retourner 0 ou gérer autrement
        return 0.0
    
    # Somme des distances (en excluant la distance à soi-même qui est 0)
    total_distance = sum(distances.values())
    
    if total_distance == 0:
        return 0.0
    
    return 1.0 / total_distance


def compute_all_closeness_classical(graph):
    """
    Calcule la closeness centrality de TOUS les nœuds avec l'algo classique
    
    Complexité: O(n*m) où n = nombre de nœuds, m = nombre d'arêtes
    
    Args:
        graph: networkx.Graph
    
    Returns:
        dict: {node: closeness_centrality}
    """
    closeness = {}
    
    for node in graph.nodes():
        closeness[node] = compute_closeness_centrality(graph, node)
    
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