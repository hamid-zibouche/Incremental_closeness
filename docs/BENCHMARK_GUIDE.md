# Guide d'utilisation du Benchmark

Ce guide explique comment utiliser le système de benchmark pour évaluer les performances de l'algorithme incrémental de closeness centrality.

## 🎯 Objectif

Le benchmark permet de :
1. Mesurer les temps d'exécution sur différentes tailles de graphes
2. Comparer la méthode classique vs incrémentale
3. Calculer le speedup (accélération)
4. Générer des graphiques de performance

## 📊 Étape 1 : Lancer le benchmark

```bash
cd src
python benchmark.py
```

### Configuration par défaut

Le benchmark teste sur 6 configurations différentes :
- 50 nœuds (m=2)
- 100 nœuds (m=2)
- 200 nœuds (m=2)
- 300 nœuds (m=3)
- 400 nœuds (m=3)
- 500 nœuds (m=3)

Où `m` est le nombre d'arêtes ajoutées par nouveau nœud (paramètre Barabási-Albert).

### Personnaliser le benchmark

Éditez `benchmark.py` et modifiez la liste `graph_sizes` :

```python
graph_sizes = [
    (100, 2),   # 100 nœuds, m=2
    (200, 3),   # 200 nœuds, m=3
    (500, 4),   # 500 nœuds, m=4
]
```

### Durée d'exécution

- Configuration par défaut : **5-10 minutes**
- Graphes de 500+ nœuds : ajouter ~2 minutes par configuration

### Résultat

Un fichier CSV est généré : `results/benchmark_results.csv`

Exemple de contenu :
```csv
n_nodes,m,num_actions,time_classical,time_incremental,speedup,correct,max_diff
50,2,151.0,0.4812,0.1654,2.91,True,0.0
100,2,301.0,1.9234,0.6543,2.94,True,0.0
...
```

## 📈 Étape 2 : Générer les courbes

```bash
cd src
python plot_results.py
```

### Graphiques générés

Le script génère 4 fichiers PNG dans `results/` :

1. **`benchmark_execution_times.png`**
   - Temps d'exécution en fonction du nombre de nœuds
   - Compare classique vs incrémental

2. **`benchmark_speedup.png`**
   - Speedup (accélération) en fonction du nombre de nœuds
   - Montre l'amélioration de performance

3. **`benchmark_time_per_action.png`**
   - Temps moyen par action (en millisecondes)
   - Utile pour comprendre la scalabilité

4. **`benchmark_combined.png`**
   - Graphique combiné avec tous les résultats
   - Vue d'ensemble complète

### Ouvrir les graphiques

Les fichiers PNG sont en haute résolution (300 DPI) et peuvent être :
- Ouverts dans n'importe quel visualiseur d'images
- Insérés dans des rapports/présentations
- Publiés dans des articles

## 🔧 Options avancées

### Modifier le nombre de runs

Par défaut, chaque configuration est exécutée 3 fois pour moyenner les résultats.

Pour changer cela, éditez `benchmark.py` :

```python
num_runs = 5  # Augmenter pour plus de précision
```

### Ajouter plus de tailles

Pour tester des graphes encore plus grands :

```python
graph_sizes = [
    # ... configurations existantes ...
    (1000, 3),  # Très grand graphe (attention : lent !)
    (2000, 4),  # Énorme graphe (peut prendre 30+ minutes)
]
```

⚠️ **Attention** : Les graphes de 1000+ nœuds peuvent prendre beaucoup de temps !

### Tolérance de correction

La tolérance pour vérifier que les résultats sont identiques est définie dans `verify_correctness()` :

```python
tolerance = 1e-5  # 0.001% de différence acceptée
```

## 📊 Interpréter les résultats

### Speedup

- **Speedup = 1** : Pas d'amélioration
- **Speedup = 2** : 2× plus rapide (50% du temps)
- **Speedup = 3** : 3× plus rapide (33% du temps)

### Correction

- **True** : Les deux méthodes donnent des résultats identiques (à la tolérance près)
- **False** : Il y a des différences → bug potentiel

### Temps par action

Montre le temps moyen pour traiter une action (addNode, addEdge, etc.).

Un temps croissant avec la taille du graphe indique une complexité non-linéaire.

## 🐛 Dépannage

### Erreur : `benchmark_results.csv` introuvable

➡️ Lancez d'abord `python benchmark.py` avant `python plot_results.py`

### Benchmark trop lent

➡️ Réduisez le nombre de configurations ou la taille maximale des graphes

### Résultats incorrects (correct=False)

➡️ Vérifiez qu'il n'y a pas de bug dans l'implémentation
➡️ La différence max_diff devrait être < 1e-5

### Graphiques ne s'affichent pas

➡️ Assurez-vous que matplotlib est installé : `pip install matplotlib`

## 📝 Exemple de workflow complet

```bash
# 1. Lancer le benchmark
cd src
python benchmark.py

# Sortie attendue :
# ================================================================================
# BENCHMARK CLOSENESS CENTRALITY INCRÉMENTALE
# ================================================================================
# ...
# ✓ Résultats sauvegardés dans: results/benchmark_results.csv

# 2. Générer les courbes
python plot_results.py

# Sortie attendue :
# ================================================================================
# GÉNÉRATION DES GRAPHIQUES DE PERFORMANCE
# ================================================================================
# ✓ Graphique sauvegardé: results/benchmark_execution_times.png
# ✓ Graphique sauvegardé: results/benchmark_speedup.png
# ✓ Graphique sauvegardé: results/benchmark_time_per_action.png
# ✓ Graphique combiné sauvegardé: results/benchmark_combined.png

# 3. Visualiser les résultats
# Ouvrir les fichiers PNG dans results/
```

## 💡 Conseils

1. **Premier run** : Testez d'abord avec de petites tailles pour valider
2. **Sauvegarder** : Les résultats peuvent être versionnés avec git
3. **Comparer** : Gardez les anciens CSV pour comparer les versions
4. **Analyser** : Utilisez Excel/Python pour analyses plus poussées

## 📚 Références

Voir `README.md` principal pour plus d'informations sur les algorithmes et l'implémentation.
