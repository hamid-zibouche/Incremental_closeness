# 📚 Index des Fichiers du Projet

Ce document liste tous les fichiers importants du projet avec leur description et utilité.

## 🎯 Fichiers Principaux

### 📄 README.md
**Description** : Documentation principale du projet  
**Contenu** :
- Vue d'ensemble du projet
- Description des algorithmes (4 algorithmes de Kas et al.)
- Guide d'utilisation programmatique
- Résultats des benchmarks
- Références académiques

**Quand lire** : Commencez par là pour comprendre le projet

---

### 📄 GUIDE_STRUCTURE.md
**Description** : Récapitulatif de la structure propre créée  
**Contenu** :
- Organisation des dossiers
- Résultats des benchmarks
- Comment utiliser le système
- Observations et analyses

**Quand lire** : Pour comprendre l'organisation du projet

---

### 📄 requirements.txt
**Description** : Liste des dépendances Python  
**Contenu** :
```
networkx>=3.0
matplotlib>=3.5.0
pyvis>=0.3.0
```

**Comment utiliser** :
```bash
pip install -r requirements.txt
```

---

### 📄 .gitignore
**Description** : Fichiers à ignorer par Git  
**Contenu** :
- `__pycache__/`
- `*.pyc`
- `.ipynb_checkpoints/`
- Optionnel : `results/`

---

## 📂 Dossier `src/` - Code Source

### ⭐ incremental_closeness_article.py
**Description** : **FICHIER PRINCIPAL** - Implémentation des 4 algorithmes de l'article  
**Classe** : `IncrementalClosenessArticle`  
**Méthodes principales** :
- `add_node(node)` : Ajoute un nœud
- `add_edge(u, v)` : Ajoute une arête orientée
- `add_undirected_edge(u, v)` : Ajoute une arête non orientée (2 arêtes orientées)
- `remove_edge(u, v)` : Supprime une arête orientée
- `remove_undirected_edge(u, v)` : Supprime une arête non orientée
- `remove_node(node)` : Supprime un nœud et ses arêtes
- `get_closeness(node)` : Obtient la closeness d'un nœud
- `get_all_closeness()` : Obtient toutes les closeness

**Algorithmes implémentés** :
1. `INSERTEDGEGROWING` : Insertion d'arête
2. `INSERTUPDATEGROWING` : Mise à jour après insertion
3. `DELETEEDGESHRINKING` : Suppression d'arête
4. `DELETEUPDATESHRINKING` : Mise à jour après suppression (version simplifiée)

---

### 📊 closeness.py
**Description** : Méthode classique de calcul de closeness (baseline)  
**Fonction principale** : `compute_all_closeness_classical(G)`  
**Utilité** : Référence pour valider la méthode incrémentale

---

### 🔗 graph.py
**Description** : Classe `DynamicGraph` pour la méthode classique  
**Classe** : `DynamicGraph`  
**Méthodes** :
- `add_node(node)`
- `remove_node(node)`
- `add_edge(u, v)`
- `remove_edge(u, v)`

---

### 🎲 generator.py
**Description** : Générateur de graphes et d'actions dynamiques  
**Fonctions principales** :
- `generate_social_graph(n_nodes, m, seed)` : Génère un graphe Barabási-Albert
- `generate_dynamic_actions_reserved(G, steps, seed)` : Génère des actions (addNode, addEdge, removeNode, removeEdge)
- `generate_barabasi_albert_actions(num_nodes, m, num_actions, seed)` : Fonction complète pour le benchmark

**Probabilités** (dans `generate_dynamic_actions_reserved`) :
- 35% : Ajout d'arête
- 20% : Ajout de nœud
- 20% : Suppression d'arête
- 25% : Suppression de nœud

---

### 🚀 benchmark.py
**Description** : Système de benchmark complet  
**Fonctions principales** :
- `run_classical_benchmark(actions)` : Mesure temps méthode classique
- `run_incremental_benchmark(actions)` : Mesure temps méthode incrémentale
- `verify_correctness(clos_class, clos_incr)` : Vérifie la correction
- `run_benchmark(graph_sizes, num_runs)` : Lance le benchmark complet
- `main()` : Point d'entrée

**Configuration** : Lit `benchmark_config.py`  
**Sortie** : `results/benchmark_results.csv`

---

### ⚙️ benchmark_config.py
**Description** : Configuration du benchmark  
**Variables** :
- `GRAPH_SIZES` : Liste de tuples `(num_nodes, m)`
- `NUM_ACTIONS_RATIO` : Multiplicateur pour le nombre d'actions
- `NUM_RUNS` : Nombre de répétitions par configuration
- `RESULTS_DIR` : Dossier de sortie

**Exemple** :
```python
GRAPH_SIZES = [
    (50, 2),
    (100, 2),
    (200, 2),
    (300, 3),
    (400, 3),
    (500, 3),
]
```

---

### 📈 plot_results.py
**Description** : Génération des courbes de performance  
**Fonctions principales** :
- `load_results(csv_path)` : Charge le CSV
- `plot_execution_time(df, output_path)` : Courbe temps d'exécution
- `plot_speedup(df, output_path)` : Courbe speedup
- `plot_time_per_action(df, output_path)` : Courbe temps par action
- `plot_combined(df, output_path)` : Vue combinée

**Entrée** : `results/benchmark_results.csv`  
**Sorties** : 4 fichiers PNG dans `results/`

---

### 🧪 test_minimal.py
**Description** : Test simple sur 3 nœuds  
**Opérations testées** :
1. Ajout de 3 nœuds
2. Ajout arête 0--1
3. Ajout arête 0--2

**Usage** :
```bash
cd src
python test_minimal.py
```

---

### 🧪 test_comparison.py
**Description** : Test complet avec visualisation  
**Opérations** :
1. Génère un graphe Barabási-Albert (100 nœuds, 500 actions)
2. Compare méthode classique vs incrémentale
3. Génère des visualisations HTML interactives

**Sorties** :
- `results/graph_classique.html`
- `results/graph_incremental.html`

**Usage** :
```bash
cd src
python test_comparison.py
```

---

### 🧪 test_debug.py
**Description** : Test avec suppressions  
**Opérations testées** :
- Suppressions d'arêtes
- Suppressions de nœuds
- Vérification de la correction

---

## 📂 Dossier `docs/` - Documentation

### 📖 HOWTO.md
**Description** : Guide d'utilisation complet  
**Sections** :
1. Installation
2. Démarrage rapide
3. Tests de validation
4. Utilisation programmatique
5. Interprétation des résultats
6. Configuration
7. Dépannage

**Quand lire** : Pour utiliser le projet

---

### 📚 BENCHMARK_GUIDE.md
**Description** : Guide complet du système de benchmark  
**Sections** :
1. Introduction
2. Configuration
3. Exécution
4. Interprétation des résultats
5. Personnalisation
6. Troubleshooting

**Quand lire** : Pour comprendre le système de benchmark

---

## 📂 Dossier `scripts/` - Scripts Utilitaires

### 🚀 run_benchmark.py
**Description** : Pipeline complet automatique  
**Actions** :
1. Exécute `benchmark.py`
2. Exécute `plot_results.py`
3. Affiche un résumé

**Usage** :
```bash
python scripts/run_benchmark.py
```

---

### 📋 show_structure.py
**Description** : Affiche l'arborescence du projet  
**Fonction** : `print_tree(directory)`  
**Ignore** : `__pycache__/`, `.git/`, etc.

**Usage** :
```bash
python scripts/show_structure.py
```

---

### 🧹 clean.py
**Description** : Nettoyage des fichiers temporaires  
**Fonctions** :
- `clean_pycache()` : Supprime `__pycache__/`
- `clean_results()` : Supprime résultats
- `clean_data()` : Supprime données temporaires
- `clean_all()` : Tout nettoyer

**Usage** :
```bash
python scripts/clean.py
```

---

### ✅ verify_project.py
**Description** : Vérification de l'intégrité du projet  
**Vérifications** :
1. Structure des dossiers
2. Fichiers de configuration
3. Imports Python
4. Dépendances
5. Scripts utilitaires
6. Résultats (optionnel)

**Usage** :
```bash
python scripts/verify_project.py
```

---

## 📂 Dossier `results/` - Résultats

### 📊 benchmark_results.csv
**Description** : Données brutes du benchmark  
**Colonnes** :
- `graph_size` : Nombre de nœuds initial
- `nodes` : Nombre final de nœuds
- `edges` : Nombre final d'arêtes
- `actions` : Nombre total d'actions
- `time_classical` : Temps classique (s)
- `time_incremental` : Temps incrémental (s)
- `speedup` : Ratio temps_classical / temps_incremental
- `correct` : Validation (True/False)

---

### 📈 benchmark_execution_times.png
**Description** : Courbe temps d'exécution vs taille  
**Axes** :
- X : Taille du graphe (nœuds)
- Y : Temps d'exécution (secondes)

**Lignes** :
- Bleue : Méthode classique
- Rouge : Méthode incrémentale

---

### 📈 benchmark_speedup.png
**Description** : Courbe speedup vs taille  
**Axes** :
- X : Taille du graphe (nœuds)
- Y : Speedup (ratio)

**Interprétation** :
- Speedup > 1 : Incrémental plus rapide
- Speedup < 1 : Classique plus rapide

---

### 📈 benchmark_time_per_action.png
**Description** : Temps moyen par action vs taille  
**Utilité** : Comprendre la scalabilité

---

### 📈 benchmark_combined.png
**Description** : Vue combinée des 3 graphiques  
**Utilité** : Vue d'ensemble rapide

---

### 🌐 graph_classique.html
**Description** : Visualisation interactive (méthode classique)  
**Technologie** : pyvis (vis.js)  
**Contenu** :
- Nœuds colorés selon closeness
- Taille proportionnelle à la closeness
- Interactif (zoom, pan, sélection)

**Ouverture** : Dans un navigateur web

---

### 🌐 graph_incremental.html
**Description** : Visualisation interactive (méthode incrémentale)  
**Identique à** : `graph_classique.html`  
**Utilité** : Vérification visuelle que les deux méthodes donnent le même résultat

---

### 📝 README.md
**Description** : Documentation du dossier results  
**Contenu** : Explication de chaque type de fichier

---

## 📂 Dossier `data/` - Données de Test

### 📄 test_graph.txt
**Description** : Fichier d'actions de test  
**Format** :
```
addNode n0
addNode n1
addEdge n0 n1
removeEdge n0 n1
removeNode n0
```

**Génération** : `generator.py main()`

---

## 🎯 Fichiers par Cas d'Usage

### Je veux comprendre le projet
1. `README.md` → Vue d'ensemble
2. `GUIDE_STRUCTURE.md` → Structure
3. `docs/HOWTO.md` → Utilisation

### Je veux utiliser le code
1. `docs/HOWTO.md` → Guide complet
2. `src/incremental_closeness_article.py` → Code principal
3. `src/test_minimal.py` → Exemple simple

### Je veux lancer des benchmarks
1. `docs/BENCHMARK_GUIDE.md` → Guide benchmark
2. `scripts/run_benchmark.py` → Lancement automatique
3. `src/benchmark_config.py` → Configuration

### Je veux modifier le code
1. `src/incremental_closeness_article.py` → Algorithmes
2. `src/generator.py` → Génération de graphes
3. `src/benchmark.py` → Système de test

### Je veux comprendre les résultats
1. `results/benchmark_results.csv` → Données
2. `results/benchmark_combined.png` → Vue graphique
3. `docs/HOWTO.md` section "Interpréter les Résultats"

---

## 🔧 Maintenance

### Vérifier l'intégrité
```bash
python scripts/verify_project.py
```

### Nettoyer
```bash
python scripts/clean.py
```

### Afficher la structure
```bash
python scripts/show_structure.py
```

---

## 📊 Workflow Typique

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test rapide**
   ```bash
   cd src
   python test_minimal.py
   ```

3. **Benchmark complet**
   ```bash
   python scripts/run_benchmark.py
   ```

4. **Analyse des résultats**
   - Ouvrir `results/benchmark_combined.png`
   - Consulter `results/benchmark_results.csv`

5. **Vérification**
   ```bash
   python scripts/verify_project.py
   ```
