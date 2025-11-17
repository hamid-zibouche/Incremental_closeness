"""
Script pour tracer les courbes de performance à partir des résultats du benchmark.

Génère plusieurs graphiques :
1. Temps d'exécution en fonction de la taille du graphe
2. Speedup en fonction de la taille du graphe
3. Temps par action en fonction de la taille
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_results(csv_file):
    """
    Charge les résultats du benchmark depuis le fichier CSV.
    
    Args:
        csv_file: Chemin du fichier CSV
        
    Returns:
        dict: Données du benchmark
    """
    data = {
        'n_nodes': [],
        'num_actions': [],
        'time_classical': [],
        'time_incremental': [],
        'speedup': [],
        'correct': []
    }
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['n_nodes'].append(int(float(row['n_nodes'])))
            data['num_actions'].append(float(row['num_actions']))
            data['time_classical'].append(float(row['time_classical']))
            data['time_incremental'].append(float(row['time_incremental']))
            data['speedup'].append(float(row['speedup']))
            data['correct'].append(row['correct'] == 'True')
    
    return data


def plot_execution_times(data, output_dir):
    """
    Trace les temps d'exécution en fonction de la taille du graphe.
    
    Args:
        data: Données du benchmark
        output_dir: Dossier de sortie pour les graphiques
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(data['n_nodes'], data['time_classical'], 'o-', 
             label='Méthode Classique', linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(data['n_nodes'], data['time_incremental'], 's-', 
             label='Méthode Incrémentale', linewidth=2, markersize=8, color='#2ecc71')
    
    plt.xlabel('Nombre de nœuds', fontsize=12)
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=12)
    plt.title('Comparaison des temps d\'exécution\n(Closeness Centrality)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajouter les valeurs sur les points
    for i, (n, t_c, t_i) in enumerate(zip(data['n_nodes'], data['time_classical'], data['time_incremental'])):
        plt.annotate(f'{t_c:.2f}s', (n, t_c), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=8, color='#c0392b')
        plt.annotate(f'{t_i:.2f}s', (n, t_i), textcoords="offset points", 
                    xytext=(0,-15), ha='center', fontsize=8, color='#27ae60')
    
    plt.tight_layout()
    output_file = output_dir / 'benchmark_execution_times.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()


def plot_speedup(data, output_dir):
    """
    Trace le speedup en fonction de la taille du graphe.
    
    Args:
        data: Données du benchmark
        output_dir: Dossier de sortie pour les graphiques
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(data['n_nodes'], data['speedup'], 'D-', 
             linewidth=2, markersize=10, color='#3498db')
    plt.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Speedup = 1x (pas d\'amélioration)')
    
    plt.xlabel('Nombre de nœuds', fontsize=12)
    plt.ylabel('Speedup (Classique / Incrémental)', fontsize=12)
    plt.title('Speedup de la méthode incrémentale\n(valeurs > 1 indiquent une amélioration)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajouter les valeurs sur les points
    for n, s in zip(data['n_nodes'], data['speedup']):
        plt.annotate(f'{s:.2f}x', (n, s), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9, fontweight='bold', color='#2980b9')
    
    plt.tight_layout()
    output_file = output_dir / 'benchmark_speedup.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()


def plot_time_per_action(data, output_dir):
    """
    Trace le temps par action en fonction de la taille du graphe.
    
    Args:
        data: Données du benchmark
        output_dir: Dossier de sortie pour les graphiques
    """
    time_per_action_classical = [t / n * 1000 for t, n in zip(data['time_classical'], data['num_actions'])]
    time_per_action_incremental = [t / n * 1000 for t, n in zip(data['time_incremental'], data['num_actions'])]
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(data['n_nodes'], time_per_action_classical, 'o-', 
             label='Méthode Classique', linewidth=2, markersize=8, color='#e74c3c')
    plt.plot(data['n_nodes'], time_per_action_incremental, 's-', 
             label='Méthode Incrémentale', linewidth=2, markersize=8, color='#2ecc71')
    
    plt.xlabel('Nombre de nœuds', fontsize=12)
    plt.ylabel('Temps par action (millisecondes)', fontsize=12)
    plt.title('Temps moyen par action\n(Closeness Centrality)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_file = output_dir / 'benchmark_time_per_action.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()


def plot_combined(data, output_dir):
    """
    Crée un graphique combiné avec plusieurs sous-graphiques.
    
    Args:
        data: Données du benchmark
        output_dir: Dossier de sortie pour les graphiques
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Benchmark Closeness Centrality Incrémentale', 
                 fontsize=16, fontweight='bold')
    
    # 1. Temps d'exécution
    ax1 = axes[0, 0]
    ax1.plot(data['n_nodes'], data['time_classical'], 'o-', 
             label='Classique', linewidth=2, markersize=8, color='#e74c3c')
    ax1.plot(data['n_nodes'], data['time_incremental'], 's-', 
             label='Incrémental', linewidth=2, markersize=8, color='#2ecc71')
    ax1.set_xlabel('Nombre de nœuds', fontsize=11)
    ax1.set_ylabel('Temps (secondes)', fontsize=11)
    ax1.set_title('Temps d\'exécution total', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 2. Speedup
    ax2 = axes[0, 1]
    ax2.plot(data['n_nodes'], data['speedup'], 'D-', 
             linewidth=2, markersize=10, color='#3498db')
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.set_xlabel('Nombre de nœuds', fontsize=11)
    ax2.set_ylabel('Speedup', fontsize=11)
    ax2.set_title('Accélération (Classique / Incrémental)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    for n, s in zip(data['n_nodes'], data['speedup']):
        ax2.annotate(f'{s:.2f}x', (n, s), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=8, color='#2980b9')
    
    # 3. Temps par action
    ax3 = axes[1, 0]
    time_per_action_classical = [t / n * 1000 for t, n in zip(data['time_classical'], data['num_actions'])]
    time_per_action_incremental = [t / n * 1000 for t, n in zip(data['time_incremental'], data['num_actions'])]
    ax3.plot(data['n_nodes'], time_per_action_classical, 'o-', 
             label='Classique', linewidth=2, markersize=8, color='#e74c3c')
    ax3.plot(data['n_nodes'], time_per_action_incremental, 's-', 
             label='Incrémental', linewidth=2, markersize=8, color='#2ecc71')
    ax3.set_xlabel('Nombre de nœuds', fontsize=11)
    ax3.set_ylabel('Temps par action (ms)', fontsize=11)
    ax3.set_title('Temps moyen par action', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    # 4. Nombre d'actions
    ax4 = axes[1, 1]
    ax4.plot(data['n_nodes'], data['num_actions'], '^-', 
             linewidth=2, markersize=10, color='#9b59b6')
    ax4.set_xlabel('Nombre de nœuds', fontsize=11)
    ax4.set_ylabel('Nombre d\'actions', fontsize=11)
    ax4.set_title('Nombre d\'actions par graphe', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_file = output_dir / 'benchmark_combined.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique combiné sauvegardé: {output_file}")
    plt.close()


def main():
    """Point d'entrée principal du script de visualisation."""
    
    # Chemins
    results_dir = Path(__file__).parent.parent / "results"
    csv_file = results_dir / "benchmark_results.csv"
    
    if not csv_file.exists():
        print(f"❌ Erreur: Fichier de résultats introuvable: {csv_file}")
        print("   Veuillez d'abord exécuter: python benchmark.py")
        return
    
    print("\n" + "="*80)
    print("GÉNÉRATION DES GRAPHIQUES DE PERFORMANCE")
    print("="*80)
    print()
    
    # Charger les résultats
    print(f"Chargement des résultats depuis: {csv_file}")
    data = load_results(csv_file)
    print(f"✓ {len(data['n_nodes'])} configurations chargées")
    print()
    
    # Créer les graphiques
    print("Génération des graphiques...")
    plot_execution_times(data, results_dir)
    plot_speedup(data, results_dir)
    plot_time_per_action(data, results_dir)
    plot_combined(data, results_dir)
    
    print()
    print("="*80)
    print("✓ Tous les graphiques ont été générés avec succès!")
    print(f"  Emplacement: {results_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
