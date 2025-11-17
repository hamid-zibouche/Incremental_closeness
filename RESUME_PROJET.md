# Résumé du Projet - Closeness Centrality Incrémentale

## ✅ Fichiers Nettoyés et Finaux

### Structure du projet
```
src/
├── incremental_closeness.py    # Algorithme principal (classique + incrémental Ramalingam & Reps)
├── test_comparison.py          # Tests de comparaison
├── exemple.py                  # Exemples d'utilisation
├── closeness.py                # Fonctions de base (BFS, calcul classique)
├── generator.py                # Génération de graphes
├── graph.py                    # Classe DynamicGraph
└── lecteur_graphe.py           # Lecture de fichiers
```

## 📝 Fichiers Supprimés

Les fichiers suivants ont été supprimés car obsolètes ou dupliqués :
- `incremental_closeness_clean.py` → renommé en `incremental_closeness.py`
- `incremental_closeness_final.py` (doublon)
- `ramalingam_reps.py` (intégré dans incremental_closeness.py)
- `test_comparison_final.py` (doublon)
- `test_clean.py` → renommé en `test_comparison.py`
- `test_small.py`, `test_small_final.py` (tests obsolètes)
- `test_medium.py` (test obsolète)
- `test_ramalingam_reps.py` (test obsolète)
- `debug_algo.py` (fichier de debug temporaire)
- `execute_actions.py` (non nécessaire)

## 🔧 Utilisation Recommandée

### Mode Classique (RECOMMANDÉ - Fiable)

```python
import networkx as nx
from incremental_closeness import IncrementalCloseness

# Créer un graphe
graph = nx.Graph()
graph.add_edges_from([(0, 1), (1, 2), (2, 3)])

# Utiliser le mode classique (recalcule tout, toujours correct)
inc = IncrementalCloseness(graph, mode='classical')

# Effectuer des modifications
inc.add_edge(0, 3)
inc.remove_edge(1, 2)

# Obtenir les closeness
closeness = inc.get_closeness()
```

### Mode Incrémental (Ramalingam & Reps)

⚠️ **Note** : L'implémentation du mode incrémental contient encore des bugs dans certains cas. 
Le mode classique est plus fiable pour une utilisation en production.

```python
# Mode incrémental (plus rapide mais peut avoir des bugs)
inc = IncrementalCloseness(graph, mode='incremental')
```

## ⚙️ Algorithmes Implémentés

### 1. **Mode Classical**
- Recalcule toutes les closeness après chaque modification
- **Avantages** : Simple, fiable, toujours correct
- **Inconvénients** : O(n²) à chaque modification
- **Utilisation** : Production, petits graphes, validation

### 2. **Mode Incremental (Ramalingam & Reps)**
- Met à jour uniquement les nœuds affectés
- **Avantages** : Théoriquement plus rapide pour graphes épars
- **Inconvénients** : Implémentation complexe, bugs potentiels, O(n²) mémoire
- **Utilisation** : Recherche, optimisation, graphes très grands

## 📊 Structures de Données

```python
class IncrementalCloseness:
    self.G              # Graphe dirigé (NetworkX DiGraph)
    self.D              # Matrice des distances D[(x,y)] = distance de x à y
    self.closeness      # Closeness centrality de chaque nœud
    self.sum_distances  # Somme des distances depuis chaque nœud
    self.stats          # Statistiques (temps, nombre de mises à jour)
```

## 🧪 Tests et Exemples

### Exécuter l'exemple simple
```bash
cd src
python exemple.py
```

### Exécuter les tests de comparaison
```bash
cd src
python test_comparison.py
```

**⚠️ Attention** : Les tests montrent que le mode incrémental a des erreurs. 
Utilisez le mode classique pour des résultats fiables.

## 📚 Formule de Closeness

```
CC(x) = (reachable / sum_distances) × (reachable / (n-1))
```

Où :
- `reachable` = nombre de nœuds atteignables depuis x
- `sum_distances` = somme des distances de x vers tous les nœuds atteignables
- `n` = nombre total de nœuds

Cette formule gère correctement les graphes non-connexes.

## 🔍 Problèmes Connus

### Mode Incrémental
1. **Bugs dans les mises à jour** : Les closeness calculées ne correspondent pas toujours au mode classique
2. **Initialisation lente** : O(n²) pour calculer toutes les distances initiales
3. **Mémoire** : O(n²) pour stocker la matrice des distances
4. **Complexité du code** : L'algorithme de Ramalingam & Reps est difficile à débugger

### Recommandation
**Utilisez le mode classique** pour toute application en production. Le mode incrémental 
est à considérer comme expérimental.

## 📖 Références

1. **Ramalingam, G., & Reps, T. (1996)**. On the computational complexity of dynamic graph problems. 
   *Theoretical Computer Science*, 158(1-2), 233-277.

2. **Kas, M., Carley, K. M., & Carley, L. R. (2013)**. Incremental Closeness Centrality for 
   Dynamically Changing Social Networks. *Proceedings of ASONAM 2013*, 1250-1258.

## 👨‍💻 Développement Futur

Pour améliorer le mode incrémental :
1. Debugger les algorithmes `_insert_update_growing` et `_delete_update_shrinking`
2. Ajouter plus de tests unitaires
3. Valider sur des graphes plus complexes
4. Optimiser l'utilisation mémoire (matrices creuses)

---

**Date de nettoyage** : 17 novembre 2025
**Projet** : M2-STL AGAA - Algorithmique pour les Graphes et Applications Avancées
