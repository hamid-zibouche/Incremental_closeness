# Guide d'utilisation - Closeness Centrality Incrémentale

Ce guide vous explique comment utiliser le projet étape par étape.

## 📦 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
cd "Incremental Closeness Centrality/Incremental_closeness"
pip install -r requirements.txt
```

Les packages nécessaires :
- `networkx` : Manipulation de graphes
- `matplotlib` : Génération de courbes
- `pyvis` : Visualisation interactive de graphes

## 🚀 Démarrage Rapide

### Option 1 : Pipeline complet automatique
```bash
python scripts/run_benchmark.py
```

Ce script exécute automatiquement :
1. Le benchmark sur différentes tailles de graphes
2. La génération des courbes de performance
3. Affichage des résultats

### Option 2 : Étape par étape

#### 1. Test simple de comparaison
```bash
cd src
python test_comparison.py
```

**Ce que ça fait** :
- Génère un graphe de test avec 100 nœuds
- Applique 500 actions (ajouts/suppressions)
- Compare méthode classique vs incrémentale
- Génère des visualisations HTML dans `results/`

**Résultats** :
- `results/graph_classique.html` : Visualisation interactive (classique)
- `results/graph_incremental.html` : Visualisation interactive (incrémental)
- Statistiques de comparaison dans le terminal

#### 2. Lancer le benchmark
```bash
cd src
python benchmark.py
```

**Ce que ça fait** :
- Teste 6 configurations de graphes (50 à 500 nœuds)
- Pour chaque configuration : 3 runs
- Mesure temps d'exécution pour les deux méthodes
- Vérifie la correction des résultats

**Résultat** :
- `results/benchmark_results.csv` : Données brutes

**Temps d'exécution** : ~2-3 minutes

#### 3. Générer les courbes
```bash
cd src
python plot_results.py
```

**Ce que ça fait** :
- Lit `results/benchmark_results.csv`
- Génère 4 graphiques PNG

**Résultats** :
- `benchmark_execution_times.png` : Temps d'exécution vs taille
- `benchmark_speedup.png` : Speedup vs taille
- `benchmark_time_per_action.png` : Temps par action vs taille
- `benchmark_combined.png` : Vue combinée

## 🧪 Tests de Validation

### Test minimal (3 nœuds)
```bash
cd src
python test_minimal.py
```

Teste les opérations de base sur un graphe très simple :
- Ajout de 3 nœuds
- Ajout de 2 arêtes
- Vérification que classique = incrémental

### Test avec suppressions
```bash
cd src
python test_debug.py
```

Teste les opérations de suppression :
- Suppression d'arêtes
- Suppression de nœuds
- Vérification de la correction

## 💻 Utilisation Programmatique

### Exemple basique
```python
from incremental_closeness_article import IncrementalClosenessArticle

# Créer l'objet
incr = IncrementalClosenessArticle()

# Ajouter des nœuds
incr.add_node(0)
incr.add_node(1)
incr.add_node(2)

# Ajouter des arêtes non orientées
incr.add_undirected_edge(0, 1)
incr.add_undirected_edge(1, 2)

# Obtenir la closeness de tous les nœuds
closeness = incr.get_all_closeness()
print(closeness)
# {0: 0.666..., 1: 1.0, 2: 0.666...}

# Obtenir la closeness d'un nœud spécifique
c1 = incr.get_closeness(1)
print(f"Closeness du nœud 1: {c1}")
# Closeness du nœud 1: 1.0
```

### Exemple avec suppressions
```python
from incremental_closeness_article import IncrementalClosenessArticle

incr = IncrementalClosenessArticle()

# Construire un graphe
incr.add_node(0)
incr.add_node(1)
incr.add_node(2)
incr.add_undirected_edge(0, 1)
incr.add_undirected_edge(1, 2)

print("Avant suppression:", incr.get_all_closeness())
# {0: 0.666..., 1: 1.0, 2: 0.666...}

# Supprimer une arête
incr.remove_undirected_edge(0, 1)
print("Après suppression arête:", incr.get_all_closeness())
# {0: 0.0, 1: 0.5, 2: 0.5}

# Supprimer un nœud
incr.remove_node(2)
print("Après suppression nœud:", incr.get_all_closeness())
# {0: 0.0, 1: 0.0}
```

### Lire un fichier d'actions
```python
from lecteur_graphe import read_actions_file
from incremental_closeness_article import IncrementalClosenessArticle

# Lire le fichier
actions = read_actions_file("data/test_graph.txt")

# Appliquer les actions
incr = IncrementalClosenessArticle()
for action in actions:
    parts = action.split()
    cmd = parts[0]
    
    if cmd == "addNode":
        incr.add_node(int(parts[1][1:]))  # Enlever le 'n' de 'n0'
    elif cmd == "addEdge":
        u, v = int(parts[1][1:]), int(parts[2][1:])
        incr.add_edge(u, v)
    # ... etc
```

## 📊 Interpréter les Résultats

### Fichier CSV
Le fichier `results/benchmark_results.csv` contient :
- `graph_size` : Nombre de nœuds
- `nodes` : Nombre final de nœuds
- `edges` : Nombre final d'arêtes
- `actions` : Nombre total d'actions
- `time_classical` : Temps classique (secondes)
- `time_incremental` : Temps incrémental (secondes)
- `speedup` : Ratio temps_classical / temps_incremental
- `correct` : Validation (True/False)

### Graphiques

#### 1. Execution Times
Montre l'évolution du temps d'exécution en fonction de la taille du graphe.
- Ligne bleue : Méthode classique
- Ligne rouge : Méthode incrémentale

**Observation actuelle** : L'incrémental est plus lent (implémentation simplifiée).

#### 2. Speedup
Montre le ratio temps_classique / temps_incremental.
- Speedup > 1 : Incrémental plus rapide
- Speedup < 1 : Classique plus rapide (cas actuel)

#### 3. Time per Action
Temps moyen par action en fonction de la taille.
Utile pour comprendre la scalabilité.

#### 4. Combined
Vue d'ensemble avec les 3 graphiques précédents.

## 🛠️ Utilitaires

### Afficher la structure du projet
```bash
python scripts/show_structure.py
```

### Nettoyer les fichiers temporaires
```bash
cd src
python ../scripts/clean.py
```

Options :
- Nettoie `__pycache__`
- Peut nettoyer `results/` (optionnel)
- Peut nettoyer `data/` temporaires (optionnel)

## ⚙️ Configuration

### Modifier les tailles de benchmark
Éditez `src/benchmark_config.py` :

```python
# Tailles de graphes à tester
GRAPH_SIZES = [
    (50, 2),    # 50 nœuds, m=2
    (100, 2),   # 100 nœuds, m=2
    (200, 2),   # 200 nœuds, m=2
    # Ajouter vos propres tailles...
]

# Nombre d'actions = NUM_ACTIONS_RATIO * nombre_de_nœuds
NUM_ACTIONS_RATIO = 5.0

# Nombre de runs par configuration
NUM_RUNS = 3
```

### Modifier le générateur de graphes
Éditez `src/generator.py` → fonction `generate_dynamic_actions_reserved` :

```python
# Probabilités des opérations
if p < 0.35:  # 35% ajout arête
    ...
elif p < 0.55:  # 20% ajout nœud
    ...
elif p < 0.75:  # 20% suppression arête
    ...
else:  # 25% suppression nœud
    ...
```

## 🐛 Dépannage

### Problème : "Module not found"
```bash
cd src
python test_comparison.py  # Assurez-vous d'être dans le dossier src/
```

### Problème : "No module named 'networkx'"
```bash
pip install -r requirements.txt
```

### Problème : Le benchmark prend trop de temps
Réduisez les tailles dans `benchmark_config.py` ou utilisez moins de runs :
```python
GRAPH_SIZES = [(50, 2), (100, 2)]  # Seulement 2 tailles
NUM_RUNS = 1  # 1 seul run
```

### Problème : Erreurs de correction dans le benchmark
C'est normal ! Quelques nœuds peuvent avoir des différences minimes (< 0.0002) dues à :
- Ordre des opérations flottantes
- Implémentation simplifiée de DELETEUPDATESHRINKING

## 📚 Pour Aller Plus Loin

### Lire la documentation complète
- `README.md` : Vue d'ensemble
- `docs/BENCHMARK_GUIDE.md` : Guide complet du benchmarking
- `results/README.md` : Structure des résultats

### Comprendre les algorithmes
Voir section "Algorithmes Implémentés" dans `README.md` pour :
- Algorithm 1: INSERTEDGEGROWING
- Algorithm 2: INSERTUPDATEGROWING
- Algorithm 3: DELETEEDGESHRINKING
- Algorithm 4: DELETEUPDATESHRINKING

### Contribuer
- Implémenter la version complète de DELETEUPDATESHRINKING
- Optimiser avec Cython/numba
- Ajouter plus de tests
- Améliorer la visualisation

## 📧 Support

Pour toute question ou problème :
1. Consultez d'abord la documentation
2. Vérifiez les issues GitHub (si applicable)
3. Contactez l'auteur du projet
