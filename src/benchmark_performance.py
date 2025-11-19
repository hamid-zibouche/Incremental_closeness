"""
Benchmark pour comparer les performances des méthodes classique et incrémentale
sur des graphes de différentes tailles.

Ce script :
1. Génère des graphes de tailles variées (Barabási-Albert)
2. Mesure le temps d'exécution pour chaque méthode
3. Sauvegarde les résultats dans results/benchmark_results.csv
4. Génère des graphes de visualisation
"""

import time
import csv
import os
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent))

from generateur_graphs import generate_barabasi_albert_actions
from graph import DynamicGraph
from incremental_closeness_article import IncrementalClosenessArticle
from classical_closeness import compute_all_closeness_classical
from lecteur_graphe import to_int


def run_classical_benchmark(actions):
    """
    Exécute la méthode classique et mesure le temps.
    CALCULE LA CLOSENESS APRÈS CHAQUE ACTION (comparaison équitable).
    
    """
    G = DynamicGraph()
    
    start_time = time.time()
    
    for action in actions:
        parts = action.split()
        cmd = parts[0]
        
        if cmd == "addNode":
            node = to_int(parts[1])
            G.add_node(node)
        elif cmd == "removeNode":
            node = to_int(parts[1])
            G.remove_node(node)
        elif cmd == "addEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            G.add_edge(u, v)
        elif cmd == "removeEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            G.remove_edge(u, v)
        
        # Calculer closeness APRÈS CHAQUE ACTION
        closeness = compute_all_closeness_classical(G.G)
    
    elapsed_time = time.time() - start_time
    return elapsed_time, closeness


def run_incremental_benchmark(actions):
    """
    Exécute la méthode incrémentale et mesure le temps.
    
    """
    incr = IncrementalClosenessArticle()
    
    start_time = time.time()
    
    for action in actions:
        parts = action.split()
        cmd = parts[0]
        
        if cmd == "addNode":
            node = to_int(parts[1])
            incr.add_node(node)
        elif cmd == "removeNode":
            node = to_int(parts[1])
            incr.remove_node(node)
        elif cmd == "addEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            incr.add_undirected_edge(u, v)
        elif cmd == "removeEdge":
            u, v = to_int(parts[1]), to_int(parts[2])
            incr.remove_undirected_edge(u, v)
    
    # Récupérer closeness finale
    closeness = incr.get_all_closeness()
    
    elapsed_time = time.time() - start_time
    return elapsed_time, closeness


def verify_correctness(clos_class, clos_incr, tolerance=1e-5):
    """
    Vérifie que les deux méthodes donnent les mêmes résultats.
    
    """
    differences = []
    for node in clos_class:
        diff = abs(clos_class[node] - clos_incr.get(node, 0))
        if diff > tolerance:
            differences.append((node, diff))
    
    max_diff = max([d[1] for d in differences], default=0)
    return len(differences) == 0, max_diff, len(differences)


def run_benchmark(graph_sizes, num_runs=3):
    """
    Exécute le benchmark sur différentes tailles de graphes.
    
    """
    results = []
    
    print("="*80)
    print("BENCHMARK CLOSENESS CENTRALITY INCRÉMENTALE")
    print("="*80)
    print()
    
    for n_nodes, m in graph_sizes:
        print(f"\n{'='*80}")
        print(f"Configuration: {n_nodes} nœuds, m={m} arêtes par nouveau nœud")
        print(f"{'='*80}")
        
        times_classical = []
        times_incremental = []
        num_actions_list = []
        correctness_results = []
        
        for run in range(num_runs):
            print(f"\n  Run {run + 1}/{num_runs}...", end=" ", flush=True)
            
            # Générer le graphe
            actions, final_nodes, final_edges = generate_barabasi_albert_actions(n_nodes, m)
            num_actions = len(actions)
            num_actions_list.append(num_actions)
            
            # Benchmark classique
            print("Classique...", end=" ", flush=True)
            time_class, clos_class = run_classical_benchmark(actions)
            times_classical.append(time_class)
            
            # Benchmark incrémental
            print("Incrémental...", end=" ", flush=True)
            time_incr, clos_incr = run_incremental_benchmark(actions)
            times_incremental.append(time_incr)
            
            # Vérifier la correction
            correct, max_diff, num_diff = verify_correctness(clos_class, clos_incr)
            correctness_results.append((correct, max_diff, num_diff))
            
            speedup = time_class / time_incr if time_incr > 0 else 0
            print(f"✓ (Speedup: {speedup:.2f}x)", flush=True)
        
        # Calculer les moyennes
        avg_time_class = sum(times_classical) / len(times_classical)
        avg_time_incr = sum(times_incremental) / len(times_incremental)
        avg_num_actions = sum(num_actions_list) / len(num_actions_list)
        avg_speedup = avg_time_class / avg_time_incr if avg_time_incr > 0 else 0
        
        # Vérifier si tous les runs sont corrects
        all_correct = all(c[0] for c in correctness_results)
        max_max_diff = max(c[1] for c in correctness_results)
        
        print(f"\n  Résultats moyens:")
        print(f"    Actions       : {avg_num_actions:.0f}")
        print(f"    Temps classique   : {avg_time_class:.4f} sec")
        print(f"    Temps incrémental : {avg_time_incr:.4f} sec")
        print(f"    Speedup           : {avg_speedup:.2f}x")
        print(f"    Correction        : {'✓ OUI' if all_correct else f'✗ NON (max diff: {max_max_diff:.2e})'}")
        
        results.append({
            'n_nodes': n_nodes,
            'm': m,
            'num_actions': avg_num_actions,
            'time_classical': avg_time_class,
            'time_incremental': avg_time_incr,
            'speedup': avg_speedup,
            'correct': all_correct,
            'max_diff': max_max_diff
        })
    
    return results


def save_results(results, output_file):
    """
    Sauvegarde les résultats dans un fichier CSV.
    
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✓ Résultats sauvegardés dans: {output_file}")


def main():
    """Point d'entrée principal du benchmark."""
    
    # Créer le dossier results s'il n'existe pas
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Configuration du benchmark
    # Format: (nombre_de_nœuds, m_arêtes_par_nouveau_nœud)
    graph_sizes = [
        (50, 3),
        (100, 3),
        (200, 3),
        (300, 3),
        (400, 3),
        (500, 3),
        (600, 3),
        (700, 3),
        (800, 3),
        (900, 3),
    ]
    
    num_runs = 1  # Nombre de runs par configuration
    
    print("\nConfiguration du benchmark:")
    print(f"  Tailles de graphes: {[n for n, _ in graph_sizes]}")
    print(f"  Runs par configuration: {num_runs}")
    print()
    
    # Exécuter le benchmark
    results = run_benchmark(graph_sizes, num_runs)
    
    # Sauvegarder les résultats
    output_file = results_dir / "benchmark_results.csv"
    save_results(results, output_file)
    
    # Afficher le résumé
    print("\n" + "="*80)
    print("RÉSUMÉ DES RÉSULTATS")
    print("="*80)
    print()
    print(f"{'Nœuds':<10} {'Actions':<12} {'T_class':<12} {'T_incr':<12} {'Speedup':<10} {'Correct'}")
    print("-"*80)
    for r in results:
        correct_str = "✓" if r['correct'] else "✗"
        print(f"{r['n_nodes']:<10} {r['num_actions']:<12.0f} {r['time_classical']:<12.4f} "
              f"{r['time_incremental']:<12.4f} {r['speedup']:<10.2f} {correct_str}")
    
    print()
    print("="*80)
    print(f"Pour tracer les courbes, exécutez: python plot_results.py")
    print("="*80)


if __name__ == "__main__":
    main()
