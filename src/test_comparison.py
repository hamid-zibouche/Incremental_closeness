import time
import os
from pathlib import Path
from graph import DynamicGraph
from incremental_closeness_article import IncrementalClosenessArticle
from closeness import compute_all_closeness_classical
from lecteur_graphe import to_int

# Créer le dossier results s'il n'existe pas
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# --------------------------------------------------------------------
# MÉTHODE CLASSIQUE — recalcul à chaque action
# --------------------------------------------------------------------
def run_classical(actions_file):
    print("\n=== MÉTHODE CLASSIQUE ===\n")

    Gdyn = DynamicGraph()

    # Charger toutes les actions
    with open(actions_file, "r", encoding="utf-8") as f:
        actions = [line.strip() for line in f if line.strip()]

    n = len(actions)
    t0_total = time.time()

    # Exécution pas à pas
    for i, line in enumerate(actions, 1):
        print(f"\r[Classique] Étape {i}/{n} : {line}     ", end="", flush=True)

        parts = line.split()
        action = parts[0]

        if action == "addNode":
            Gdyn.add_node(to_int(parts[1]))

        elif action == "removeNode":
            Gdyn.remove_node(to_int(parts[1]))

        elif action == "addEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            Gdyn.add_edge(u, v)

        elif action == "removeEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            Gdyn.remove_edge(u, v)

        # --- IMPORTANT : on recalcule TOUTE la closeness à chaque ligne ---
        closeness = compute_all_closeness_classical(Gdyn.G)

    total_time = time.time() - t0_total

    print("\n\n--- TOP-10 (CLASSIQUE) ---")
    top10 = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:10]
    for n, v in top10:
        print(f"Node {n}  : {v}")

    print(f"\nTemps total (classique) : {total_time:.4f} sec")

    # --- Visualisation PyVis avec ton code natif ---
    output_path = RESULTS_DIR / "graph_classique.html"
    Gdyn.visualize_interactive(
        closeness_values=closeness,
        output_path=str(output_path),
        physics=True
    )

    return closeness, total_time, Gdyn.G


# --------------------------------------------------------------------
# MÉTHODE INCRÉMENTALE — mise à jour à chaque action
# --------------------------------------------------------------------
def run_incremental(actions_file):
    print("\n=== MÉTHODE INCRÉMENTALE ===\n")

    Gdyn = DynamicGraph()

    # Charger les actions
    with open(actions_file, "r", encoding="utf-8") as f:
        actions = [line.strip() for line in f if line.strip()]

    # Créer l'objet incrémental vide
    import networkx as nx
    incr = IncrementalClosenessArticle()

    n = len(actions)
    t0_total = time.time()

    # Exécution action par action
    for i, line in enumerate(actions, 1):
        print(f"\r[Incrémental] Étape {i}/{n} : {line}     ", end="", flush=True)

        parts = line.split()
        action = parts[0]

        if action == "addNode":
            node = to_int(parts[1])
            Gdyn.add_node(node)
            incr.add_node(node)

        elif action == "removeNode":
            node = to_int(parts[1])
            Gdyn.remove_node(node)
            incr.remove_node(node)

        elif action == "addEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            # Pour Gdyn (non orienté)
            Gdyn.add_edge(u, v)
            # Pour incr (orienté) : ajouter les deux directions
            incr.add_undirected_edge(u, v)

        elif action == "removeEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            # Pour Gdyn (non orienté)
            Gdyn.remove_edge(u, v)
            # Pour incr (orienté) : supprimer les deux directions
            incr.remove_undirected_edge(u, v)

    closeness = incr.get_all_closeness()
    total_time = time.time() - t0_total

    print("\n\n--- TOP-10 (INCRÉMENTAL) ---")
    top10 = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:10]
    for n, v in top10:
        print(f"Node {n}  : {v}")

    print(f"\nTemps total (incrémental) : {total_time:.4f} sec")

    # --- Visualisation PyVis avec TON code ---
    output_path = RESULTS_DIR / "graph_incremental.html"
    Gdyn.visualize_interactive(
        closeness_values=closeness,
        output_path=str(output_path),
        physics=True
    )

    return closeness, total_time, Gdyn.G


# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("=== DÉMARRAGE DU TEST COMPLET ===")

    # Trouver automatiquement test_graph.txt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    graph_file = os.path.join(data_dir, "test_graph.txt")

    # Méthode classique
    clos_class, time_class, G1 = run_classical(graph_file)

    # Méthode incrémentale
    clos_inc, time_inc, G2 = run_incremental(graph_file)

    # Analyse finale
    print("\n=== RÉSUMÉ FINAL ===")
    print(f"Temps classique   : {time_class:.4f} sec")
    print(f"Temps incrémental : {time_inc:.4f} sec")
    if time_inc > 0:
        print(f"Accélération      : {time_class / time_inc:.2f}x")

    # Vérification égalité et calcul des différences
    differences = []
    for node in clos_class:
        diff = abs(clos_class[node] - clos_inc.get(node, 0))
        if diff > 1e-9:
            differences.append((node, diff, clos_class[node], clos_inc.get(node, 0)))
    
    same = len(differences) == 0
    print(f"Closeness identiques ? {'OUI' if same else 'NON'}")
    
    if not same:
        print(f"\nNombre de nœuds avec différences : {len(differences)}")
        print("\n--- TOP 10 PLUS GRANDES DIFFÉRENCES ---")
        differences.sort(key=lambda x: x[1], reverse=True)
        for i, (node, diff, c_class, c_inc) in enumerate(differences[:10], 1):
            print(f"{i}. Nœud {node}:")
            print(f"   Différence : {diff:.10f}")
            print(f"   Classique  : {c_class:.10f}")
            print(f"   Incrémental: {c_inc:.10f}")

    print(f"\nGraphes générés dans {RESULTS_DIR}:")
    print(" - graph_classique.html")
    print(" - graph_incremental.html")
    print("\n=== FIN ===")
