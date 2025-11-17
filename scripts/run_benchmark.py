"""
Script de démarrage rapide pour lancer un benchmark complet.

Ce script exécute automatiquement:
1. Le benchmark sur différentes tailles de graphes
2. La génération des courbes de performance
3. L'affichage de la structure du projet

Usage:
    python scripts/run_benchmark.py
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Point d'entrée principal."""
    print("\n" + "="*80)
    print("PIPELINE COMPLET DE BENCHMARK")
    print("="*80 + "\n")
    
    # Étape 1: Exécuter le benchmark
    print("➤ ÉTAPE 1/2: Exécution du benchmark...")
    print("-"*80)
    try:
        import benchmark
        # Le module benchmark exécute déjà son main() à l'import si on l'appelle
        # Donc on l'importe et appelle sa fonction main()
        benchmark.main()
    except Exception as e:
        print(f"✗ Erreur lors du benchmark: {e}")
        return 1
    
    print("\n")
    
    # Étape 2: Générer les graphiques
    print("➤ ÉTAPE 2/2: Génération des graphiques...")
    print("-"*80)
    try:
        import plot_results
        plot_results.main()
    except Exception as e:
        print(f"✗ Erreur lors de la génération des graphiques: {e}")
        return 1
    
    print("\n" + "="*80)
    print("✓ PIPELINE TERMINÉ AVEC SUCCÈS!")
    print("="*80)
    print(f"\nRésultats disponibles dans: {project_root / 'results'}")
    print("\nFichiers générés:")
    print("  • benchmark_results.csv         - Données brutes du benchmark")
    print("  • benchmark_execution_times.png - Courbes de temps d'exécution")
    print("  • benchmark_speedup.png         - Courbe de speedup")
    print("  • benchmark_time_per_action.png - Temps par action")
    print("  • benchmark_combined.png        - Graphique combiné")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
