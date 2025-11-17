# Results / Résultats

Ce dossier contient tous les résultats générés par les différents scripts de test et de benchmark.

## Structure

### Visualisations des graphes
- `graph_classique.html` - Visualisation interactive du graphe avec méthode classique
- `graph_incremental.html` - Visualisation interactive du graphe avec méthode incrémentale

### Résultats de benchmark
- `benchmark_results.csv` - Données brutes du benchmark (temps, speedup, etc.)
- `benchmark_execution_times.png` - Graphique des temps d'exécution
- `benchmark_speedup.png` - Graphique du speedup (accélération)
- `benchmark_time_per_action.png` - Graphique du temps par action
- `benchmark_combined.png` - Graphique combiné avec tous les résultats

## Comment utiliser

### Lancer un test de comparaison
```bash
cd src
python test_comparison.py
```
Cela génère `graph_classique.html` et `graph_incremental.html` dans ce dossier.

### Lancer le benchmark complet
```bash
cd src
python benchmark.py
```
Cela génère `benchmark_results.csv` avec les données de performance.

### Tracer les courbes
```bash
cd src
python plot_results.py
```
Cela génère tous les graphiques PNG à partir des données du benchmark.

## Notes
- Les fichiers HTML peuvent être ouverts directement dans un navigateur
- Les graphiques PNG sont en haute résolution (300 DPI)
- Le benchmark peut prendre plusieurs minutes selon la configuration
