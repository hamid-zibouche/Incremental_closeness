import os
from graph import DynamicGraph
from classical_closeness import compute_all_closeness_classical



def to_int(label: str) -> int:
    """Convertit un label de type 'n123' ou entier/chaine en entier 123.

    - 'n0' -> 0
    - '42' -> 42
    - sinon: essaie int(label), et en cas d'échec, renvoie le label tel quel.
      (mais dans notre cas les fichiers d'actions sont de type nX).
    """
    if isinstance(label, int):
        return label
    s = str(label)
    if s.startswith("n") and s[1:].isdigit():
        return int(s[1:])
    if s.isdigit():
        return int(s)
    # fallback: pas convertible proprement, on pourrait lever une erreur
    # mais pour l'instant on renvoie tel quel
    return s


def lire_fichier(nom_fichier: str) -> DynamicGraph:
    """
    Lit un fichier d'actions (addNode, removeNode, addEdge, removeEdge)
    et applique ces actions sur un DynamicGraph, puis renvoie le graphe.
    """
    g = DynamicGraph()

    with open(nom_fichier, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            args = len(parts)

            if args == 2:
                # addNode nX  /  removeNode nX
                act, n1 = parts
                n1 = to_int(n1)
                if act == "addNode":
                    g.add_node(n1)
                elif act == "removeNode":
                    g.remove_node(n1)
                else:
                    print(f"Ligne {ln}: opération inconnue '{act}' (ignorée)")
            elif args == 3:
                # addEdge nX nY  /  removeEdge nX nY
                act, n1, n2 = parts
                n1, n2 = to_int(n1), to_int(n2)
                if act == "addEdge":
                    g.add_edge(n1, n2)
                elif act == "removeEdge":
                    g.remove_edge(n1, n2)
                else:
                    print(f"Ligne {ln}: opération inconnue '{act}' (ignorée)")
            else:
                print(f"Ligne {ln}: format invalide (ignorée)")

    return g


if __name__ == "__main__":
    # Exemple d'utilisation simple
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    fichier = os.path.join(data_dir, "graphe_croissance.txt")

    print("\n=== Lecture du fichier d'actions ===")
    g = lire_fichier(fichier)

    print("\n=== Calcul de la Closeness Centrality ===")
    print("Cela peut prendre quelques secondes pour un grand graphe...")
    closeness = compute_all_closeness_classical(g.G, verbose=True)

    print(f"\n=== Graphe final ===")
    print(f"Nombre de nœuds: {g.number_of_nodes()}")
    print(f"Nombre d'arêtes: {g.number_of_edges()}")

    if closeness:
        sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
        print("\nTop 5 nœuds par closeness centrality:")
        for i, (node, value) in enumerate(sorted_closeness[:5], 1):
            print(f"  {i}. Nœud {node}: {value:.6f}")
    
    # Visualisation interactive (PyVis -> HTML)
    print("\n=== Génération de la visualisation interactive ===")
    try:
        g.visualize_interactive(closeness, output_path="graph_interactive.html")
    except Exception as e:
        print("Visualisation interactive échouée:", e)