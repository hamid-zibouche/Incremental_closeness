# Incremental Closeness Centrality

## 📋 Description

Ce projet implémente et compare deux approches pour calculer la **closeness centrality** dans des graphes dynamiques :

1. **Algorithme Classique** : Recalcule la closeness de tous les nœuds à chaque modification du graphe (complexité O(n²) par étape)
2. **Algorithme Incrémental** : Met à jour uniquement les closeness affectées par chaque modification (complexité O(n) par étape)

L'algorithme incrémental est basé sur l'article de **Kas et al.** et utilise des structures de données optimisées (distances, σ-valeurs) pour éviter les recalculs complets.

## 🎯 Objectifs

- Démontrer l'avantage de l'approche incrémentale sur les grands graphes dynamiques
- Valider la correction de l'algorithme incrémental par comparaison avec le classique
- Visualiser l'évolution des graphes et des scores de closeness
- Analyser les performances sur différents types de graphes (croissants, décroissants, denses, sparse, etc.)

## 📁 Structure du Projet

```
Incremental_closeness/
├── src/                                    # Code source
│   ├── incremental_closeness_article.py   # Algorithme incrémental (article Kas et al.)
│   ├── closeness.py                       # Algorithme classique (BFS complet)
│   ├── graph.py                           # Classe DynamicGraph avec visualisation
│   ├── lecteur_graphe.py                  # Utilitaires lecture/conversion
│   │
│   ├── generateur_graphs.py               # Génération graphes dynamiques variés
│   ├── run_incremental.py                 # Exécution incrémentale sur tous les graphes
│   ├── run_classical.py                   # Exécution classique sur tous les graphes
│   ├── benchmark_performance.py           # Benchmark sur graphes Barabási-Albert
│   │
│   ├── plot_comparison.py                 # Courbes de comparaison temps
│   ├── plot_results.py                    # Courbes d'évolution des graphes
│   ├── verification_resultats.py          # Vérification correction incrémental=classique
│   ├── test_comparison&visualisation.py   # Visualisations interactives PyVis
│                            # Point d'entrée principal
│
├── data/                                   # Graphes générés
│   ├── graphe_equilibre.txt               # Graphes dynamiques variés (10 types)
│   ├── graphe_forte_croissance.txt
│   ├── graphe_tres_dynamique.txt
│   ├── graphe_focus_noeuds.txt
│   ├── graphe_focus_aretes.txt
│   ├── graphe_croissance_stable.txt
│   ├── graphe_decroissance.txt
│   ├── graphe_petit_dense.txt
│   ├── graphe_grand_sparse.txt
│   ├── graphe_chaotique.txt
│   ├── test_graph.txt                     # Graphe de test barabasi_albert
│
├── results/                                # Résultats des expériences
│   ├── logs_graph/                        # Résultats des graphes dynamiques
│   │   ├── incremental_times.json         # Temps de l'algo incrémental
│   │   ├── classical_times.json           # Temps de l'algo classique
│   │   ├── evolution/                     # États du graphe à chaque étape
│   │   └── scores/                        # Scores de closeness à chaque étape
│   │
│   ├── time_curves/                       # Courbes de comparaison
│   │   ├── incremental_vs_classical.png   # Comparaison temps cumulés (10 graphes)
│   │   ├── time_per_step_all_graphs.png   # Temps par étape (10 graphes)
│   │   └── time_statistics.txt            # Statistiques détaillées + speedup
│   │
│   ├── visualisation/                     # Visualisations interactives HTML
│   │   ├── graphe_equilibre_classique.html
│   │   ├── graphe_equilibre_incremental.html
│   │   └── ... (20 fichiers au total)
│   │
│   └                         # Résultats benchmark Barabási-Albert
│   ├── benchmark_combined.png          # Courbes scaling (tailles 100-1000)
│
├── run_all.ps1                             # Script d'automatisation complet
├── requirements.txt                        # Dépendances Python
└── README.md                               # Ce fichier

```

## 🚀 Installation et Dépendances

### Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)

### Installation des dépendances

```powershell
pip install networkx matplotlib numpy pyvis
```

Ou via le fichier requirements.txt :

```powershell
pip install -r requirements.txt
```

## 📊 Types de Graphes Générés

Le projet génère 10 graphes dynamiques avec différentes caractéristiques pour tester divers scénarios d'évolution :

| Graphe | Étapes | Caractéristique | Utilité |
|--------|--------|----------------|---------|
| `graphe_equilibre` | 1500 | Ajouts/suppressions équilibrés | Cas général |
| `graphe_forte_croissance` | 1700 | Beaucoup d'ajouts (35%) | Montre l'avantage de l'incrémental |
| `graphe_tres_dynamique` | 2000 | Changements constants | Teste la robustesse |
| `graphe_focus_noeuds` | 1300 | Operations sur les nœuds | Teste add/remove node |
| `graphe_focus_aretes` | 2500 | Operations sur les arêtes | Teste add/remove edge |
| `graphe_croissance_stable` | 2300 | Croissance lente et stable | Graphe long terme |
| `graphe_decroissance` | 1900 | Plus de suppressions | Graphe qui rétrécit |
| `graphe_petit_dense` | 1100 | Petit graphe, beaucoup d'arêtes | Teste densité |
| `graphe_grand_sparse` | 3000 | Grand graphe, peu d'arêtes | Graphe réaliste |
| `graphe_chaotique` | 2200 | Probabilités égales | Comportement aléatoire |

## 🔧 Utilisation

### Option 1 : Script d'Automatisation (Recommandé)

Le script PowerShell `run_all.ps1` permet d'exécuter tout le pipeline automatiquement.

#### Exécution complète (tout le pipeline)

```powershell
.\run_all.ps1 -All
```

**Durée** : 20-35 minutes  
**Contenu** : Génération des graphes, traitement incrémental, traitement classique, comparaisons, vérifications, visualisations

#### Mode rapide (sans algorithme classique)

```powershell
.\run_all.ps1 -Quick
```

**Durée** : 5-8 minutes  
**Contenu** : Génération des graphes, traitement incrémental, visualisations limitées

#### Exécution par étapes

```powershell
# Générer les graphes
.\run_all.ps1 -GenerateGraphs

# Exécuter l'algorithme incrémental
.\run_all.ps1 -RunIncremental

# Exécuter l'algorithme classique (lent!)
.\run_all.ps1 -RunClassical

# Générer les courbes de comparaison
.\run_all.ps1 -PlotComparison

# Vérifier la correction
.\run_all.ps1 -Verify

# Générer les visualisations interactives
.\run_all.ps1 -Visualize

# Exécuter le benchmark Barabási-Albert
.\run_all.ps1 -Benchmark
```

#### Aide

```powershell
.\run_all.ps1 -Help
```

### Option 2 : Exécution Manuelle

#### 1. Générer les graphes dynamiques

```powershell
cd src
python generateur_graphs.py
```

#### 2. Exécuter l'algorithme incrémental

```powershell
python run_incremental.py
```

#### 3. Exécuter l'algorithme classique (optionnel, lent)

```powershell
python run_classical.py
```

#### 4. Générer les courbes de comparaison

```powershell
python plot_comparison.py
```

#### 5. Vérifier la correction des résultats

```powershell
python verification_resultats.py
```

#### 6. Générer les visualisations interactives

```powershell
python test_comparison&visualisation.py
```

#### 7. Exécuter le benchmark sur graphes Barabási-Albert (optionnel)

```powershell
python benchmark_performance.py
```

**Durée** : 10-15 minutes  
**Description** : Teste les deux algorithmes sur des graphes Barabási-Albert de tailles variées (50-900 nœuds) pour évaluer le scaling. Génère un fichier CSV avec les résultats dans `results/benchmark_results.csv`.

## 📈 Résultats Attendus

### Courbes de Comparaison

Les courbes dans `results/time_curves/` montrent :

1. **incremental_vs_classical.png** : Comparaison des temps cumulés
   - L'algorithme incrémental est **significativement plus rapide** sur les grands graphes croissants
   - Le speedup augmente avec la taille du graphe

2. **time_per_step_all_graphs.png** : Temps par étape pour chaque graphe
   - L'algorithme classique a un temps **croissant** (O(n²) avec la taille)
   - L'algorithme incrémental a un temps **quasi-constant** (O(n))

### Visualisations Interactives

Les fichiers HTML dans `results/visualisation/` permettent de :
- Visualiser le graphe final avec les scores de closeness
- Les nœuds sont colorés selon leur score (rouge = haute closeness, bleu = basse)
- La taille des nœuds reflète leur importance
- Interaction : zoom, déplacement, sélection de nœuds

### Benchmark sur Graphes de Grande Taille

**Pour des tests plus sérieux sur des graphes réalistes**, nous avons implémenté le **modèle Barabási-Albert** dans `generateur_graphs.py`. Ce modèle produit des graphes à invariance d'échelle (scale-free) avec une distribution de degrés en loi de puissance, typique des **réseaux sociaux réels**.

Le fichier `benchmark_performance.py` génère et teste les deux algorithmes sur des **graphes Barabási-Albert de différentes tailles** (50 à 900 nœuds) pour évaluer le comportement à l'échelle.

**Comment exécuter le benchmark :**

```powershell
cd src
python benchmark_performance.py
```

**Ce que fait le benchmark :**
1. Génère des graphes Barabási-Albert de tailles variées (50, 100, 200, ..., 900 nœuds)
2. Pour chaque taille, exécute les deux algorithmes (classique et incrémental)
3. Mesure les temps d'exécution et vérifie la correction des résultats
4. Calcule le speedup (rapport temps_classique / temps_incrémental)
5. Sauvegarde les résultats dans `results/benchmark_results.csv`

**Résultats attendus :**
- `results/benchmark_results.csv` : Tableau complet avec temps, speedup, correction pour chaque taille
- Le CSV peut ensuite être utilisé pour générer des courbes de performance

Ce benchmark démontre que l'algorithme incrémental **scale beaucoup mieux** que le classique sur les grands graphes réalistes de type réseau social.

## ✅ Vérification de la Correction

Le script `verification_resultats.py` compare les scores incrémentaux avec les scores classiques sur un échantillon d'étapes (1/10) pour valider que :

```
closeness_incremental[node] ≈ closeness_classique[node] ∀ node
```

## 🔬 Algorithme Incrémental - Détails

L'algorithme incrémental (basé sur l'article Kas et al.) maintient pour chaque nœud :

1. **Distances** : `dist[s][v]` = distance de `s` à `v`
2. **Sigma** : `σ[s][v]` = nombre de plus courts chemins de `s` à `v`
3. **Closeness** : `C[s]` = (reachable / sum_distances) × (reachable / (n-1))

### Opérations Supportées

- `add_node(v)` : Ajoute un nœud isolé, recalcule toutes les closeness (normalisation n)
- `remove_node(v)` : Supprime un nœud et ses arêtes, met à jour les closeness affectées
- `add_edge(u, v)` : Ajoute une arête, met à jour les distances via BFS depuis u et v
- `remove_edge(u, v)` : Supprime une arête, recalcule les distances si nécessaire

## 📝 Format des Fichiers

### Graphes Dynamiques (`data/graphe_*.txt`)

```
addNode n0
addNode n1
addEdge n0 n1
removeEdge n0 n1
removeNode n1
```

### Scores de Closeness (`results/logs_graph/scores/*.txt`)

```
0.0       # Node 0
0.333333  # Node 1
0.5       # Node 2
...
```

### Temps de Calcul (`results/logs_graph/*_times.json`)

```json
{
  "graphe_equilibre": {
    "total_steps": 1000,
    "time_per_step": [0.001, 0.0012, ...],
    "cumulative_time": 1.234
  }
}
```

## 📚 Références

- **Article de référence** : Kas, M., et al. "Incremental algorithms for closeness centrality" (2013)
- **NetworkX Documentation** : https://networkx.org/
- **PyVis Documentation** : https://pyvis.readthedocs.io/


### Commandes Rapides

```powershell
# Exécution complète (recommandé)
.\run_all.ps1 -All

# Ou mode rapide si besoin
.\run_all.ps1 -Quick

# Voir les résultats
start results\time_curves\incremental_vs_classical.png
start results\visualisation\graphe_forte_croissance_incremental.html
```

### Points Clés à Vérifier

✅ L'algorithme incrémental est **plus rapide** que le classique (voir courbes)  
✅ Les scores sont **identiques** (voir vérification)  
✅ Le speedup **augmente** avec la taille du graphe  
✅ Les visualisations montrent correctement les scores de closeness
