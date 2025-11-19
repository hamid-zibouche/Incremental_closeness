import time
import os
from pathlib import Path
from graph import DynamicGraph
from incremental_closeness_article import IncrementalClosenessArticle
from classical_closeness import compute_all_closeness_classical
from lecteur_graphe import to_int

# Créer le dossier results/visualisation s'il n'existe pas
RESULTS_DIR = Path(__file__).parent.parent / "results" / "visualisation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------
# MÉTHODE CLASSIQUE — recalcul à chaque action
# --------------------------------------------------------------------
def run_classical(actions_file, graph_name):
    print(f"\n=== MÉTHODE CLASSIQUE - {graph_name} ===\n")

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

    output_path = RESULTS_DIR / f"{graph_name}_classique.html"
    Gdyn.visualize_interactive(
        closeness_values=closeness,
        output_path=str(output_path),
        physics=True
    )

    return closeness, total_time, Gdyn.G


# --------------------------------------------------------------------
# MÉTHODE INCRÉMENTALE — mise à jour à chaque action
# --------------------------------------------------------------------
def run_incremental(actions_file, graph_name):
    print(f"\n=== MÉTHODE INCRÉMENTALE - {graph_name} ===\n")

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

    output_path = RESULTS_DIR / f"{graph_name}_incremental.html"
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
    print("="*80)
    print("=== GÉNÉRATION DES VISUALISATIONS POUR TOUS LES GRAPHES ===")
    print("="*80)

    # Trouver tous les fichiers .txt dans data/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = Path(current_dir).parent / "data"
    
    # Récupérer tous les fichiers graphe_*.txt
    graph_files = sorted(data_dir.glob("graphe_*.txt"))
    
    if not graph_files:
        print(f"\n Aucun fichier graphe_*.txt trouvé dans {data_dir}")
        exit(1)
    
    print(f"\n✓ {len(graph_files)} graphe(s) trouvé(s) dans {data_dir}\n")
    
    # Traiter chaque graphe
    for idx, graph_file in enumerate(graph_files, 1):
        graph_name = graph_file.stem  # Nom sans extension
        
        print("\n" + "="*80)
        print(f"GRAPHE {idx}/{len(graph_files)}: {graph_name}")
        print("="*80)
        
        # Méthode classique
        clos_class, time_class, G1 = run_classical(str(graph_file), graph_name)
        
        # Méthode incrémentale
        clos_inc, time_inc, G2 = run_incremental(str(graph_file), graph_name)
        
        # Analyse finale pour ce graphe
        print(f"\n--- RÉSUMÉ {graph_name} ---")
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
        print(f"Closeness identiques ? {'OUI ✓' if same else 'NON ✗'}")
        
        if not same:
            print(f"Nombre de nœuds avec différences : {len(differences)}")
            print("\n--- TOP 5 PLUS GRANDES DIFFÉRENCES ---")
            differences.sort(key=lambda x: x[1], reverse=True)
            for i, (node, diff, c_class, c_inc) in enumerate(differences[:5], 1):
                print(f"{i}. Nœud {node}:")
                print(f"   Différence : {diff:.10f}")
                print(f"   Classique  : {c_class:.10f}")
                print(f"   Incrémental: {c_inc:.10f}")
        
        print(f"\nVisualisations générées:")
        print(f" ✓ {graph_name}_classique.html")
        print(f" ✓ {graph_name}_incremental.html")
    
    print("\n" + "="*80)
    print(f"✓ TERMINÉ - Toutes les visualisations dans: {RESULTS_DIR}")
    print("="*80)
    print(f"\nNombre total de graphes traités: {len(graph_files)}")
    print(f"Nombre total de fichiers HTML générés: {len(graph_files) * 2}")
    print("\n=== FIN ===\n")
