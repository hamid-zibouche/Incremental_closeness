# 🚀 DÉMARRAGE RAPIDE - 5 Minutes

## 📖 Lisez ceci en premier !

### Votre projet en 3 points
1. ✅ **Structure propre** organisée professionnellement
2. ✅ **Benchmark complet** qui teste différentes tailles de graphes
3. ✅ **Courbes de performance** déjà générées dans `results/`

---

## ⚡ Commandes Essentielles

### 1️⃣ Vérifier que tout fonctionne (30 secondes)
```bash
python scripts/verify_project.py
```
→ Devrait afficher `✨ Tout est parfait !`

### 2️⃣ Voir la structure du projet (10 secondes)
```bash
python scripts/show_structure.py
```
→ Affiche l'arborescence propre

### 3️⃣ Test minimal (10 secondes)
```bash
cd src
python test_minimal.py
```
→ Vérifie le fonctionnement de base

### 4️⃣ Benchmark complet (2-3 minutes)
```bash
python scripts/run_benchmark.py
```
→ Lance tout automatiquement et génère les courbes

---

## 📁 Où Trouver Quoi ?

### 📊 Résultats du Benchmark
→ **`results/`**
- `benchmark_combined.png` ← **REGARDEZ CECI EN PREMIER**
- `benchmark_results.csv` ← Données brutes
- `graph_classique.html` ← Visualisation interactive

### 📚 Documentation
→ **`docs/HOWTO.md`** ← Guide complet d'utilisation
→ **`README.md`** ← Documentation technique
→ **`COMPLETE.md`** ← Récapitulatif de ce qui a été fait
→ **`INDEX.md`** ← Index de tous les fichiers

### 💻 Code Principal
→ **`src/incremental_closeness_article.py`** ← Algorithme principal
→ **`src/benchmark.py`** ← Système de benchmark
→ **`src/plot_results.py`** ← Génération des courbes

---

## 🎯 Que Voulez-vous Faire ?

### Je veux comprendre le projet
1. Lisez **`COMPLETE.md`** (5 min)
2. Lisez **`README.md`** section "Structure" (3 min)
3. Regardez **`results/benchmark_combined.png`**

### Je veux utiliser le code
1. Lisez **`docs/HOWTO.md`** section "Utilisation programmatique"
2. Exécutez **`src/test_minimal.py`** pour voir un exemple
3. Copiez l'exemple et adaptez-le

### Je veux lancer un nouveau benchmark
```bash
# 1. Modifier la config (optionnel)
# Éditez src/benchmark_config.py

# 2. Lancer
python scripts/run_benchmark.py

# 3. Résultats dans results/
```

### Je veux modifier la configuration
1. Ouvrez **`src/benchmark_config.py`**
2. Changez `GRAPH_SIZES` (ex: ajouter `(1000, 4)`)
3. Relancez `python scripts/run_benchmark.py`

---

## 📊 Comprendre les Résultats (1 minute)

### Observation Principale
**L'incrémental est actuellement PLUS LENT que le classique**

### Pourquoi ?
- Implémentation simplifiée (pas optimisée)
- Beaucoup d'opérations de suppression
- Chaque suppression = BFS complet

### C'est Grave ?
**Non !** L'algorithme est **correct** (donne les bons résultats).
C'est juste une implémentation de référence non optimisée.

### Fichiers à Regarder
1. `results/benchmark_combined.png` → Vue d'ensemble
2. `results/benchmark_results.csv` → Chiffres exacts

---

## 📖 Documentation par Niveau

### Niveau 1 : Débutant (Vous êtes ici)
→ **`DEMARRAGE_RAPIDE.md`** (ce fichier)

### Niveau 2 : Utilisation
→ **`COMPLETE.md`** - Récapitulatif complet
→ **`docs/HOWTO.md`** - Guide d'utilisation

### Niveau 3 : Technique
→ **`README.md`** - Documentation technique
→ **`docs/BENCHMARK_GUIDE.md`** - Guide du benchmark

### Niveau 4 : Référence
→ **`INDEX.md`** - Index de tous les fichiers
→ Code source dans **`src/`**

---

## 🧪 Tests Disponibles

### Test Simple (3 nœuds)
```bash
cd src
python test_minimal.py
```
→ 10 secondes, vérifie le fonctionnement de base

### Test Complet (100 nœuds)
```bash
cd src
python test_comparison.py
```
→ 30 secondes, génère des visualisations HTML

### Test Debug (suppressions)
```bash
cd src
python test_debug.py
```
→ 20 secondes, teste les suppressions

### Benchmark Complet (6 tailles)
```bash
python scripts/run_benchmark.py
```
→ 2-3 minutes, génère tout

---

## 🎨 Visualisations

### Visualisations Interactives (HTML)
→ `results/graph_classique.html`
→ `results/graph_incremental.html`

**Comment ouvrir** :
- Double-cliquez sur le fichier
- Ou : `start results\graph_classique.html` (Windows)

**Ce que vous verrez** :
- Graphe interactif (zoom, déplacement)
- Nœuds colorés selon closeness
- Taille proportionnelle à la closeness

### Courbes de Performance (PNG)
→ `results/benchmark_combined.png` ← **PRINCIPAL**
→ `results/benchmark_execution_times.png`
→ `results/benchmark_speedup.png`
→ `results/benchmark_time_per_action.png`

---

## 🛠️ Commandes Utiles

### Vérification
```bash
python scripts/verify_project.py
```

### Structure
```bash
python scripts/show_structure.py
```

### Nettoyage
```bash
python scripts/clean.py
```

### Benchmark
```bash
python scripts/run_benchmark.py
```

---

## ❓ FAQ Rapide

### Q: Où sont les résultats ?
**R:** Dans le dossier **`results/`**

### Q: Comment lancer un benchmark ?
**R:** `python scripts/run_benchmark.py`

### Q: Combien de temps ça prend ?
**R:** 2-3 minutes pour le benchmark complet

### Q: Où est la documentation ?
**R:** 
- Guide complet → `docs/HOWTO.md`
- Récapitulatif → `COMPLETE.md`
- Technique → `README.md`

### Q: Comment modifier les tailles testées ?
**R:** Éditez `src/benchmark_config.py`

### Q: L'incrémental est plus lent, c'est normal ?
**R:** Oui, c'est une implémentation simplifiée. Les résultats sont corrects.

---

## 🎯 Checklist de Démarrage

- [ ] Exécuter `python scripts/verify_project.py`
- [ ] Regarder `python scripts/show_structure.py`
- [ ] Lire `COMPLETE.md` (5 min)
- [ ] Ouvrir `results/benchmark_combined.png`
- [ ] Tester `cd src && python test_minimal.py`
- [ ] Ouvrir `results/graph_classique.html` dans un navigateur
- [ ] Lire `docs/HOWTO.md` section "Démarrage rapide"

---

## 🎉 Vous êtes Prêt !

Tout est en place. Consultez :
- **`COMPLETE.md`** pour le récapitulatif complet
- **`docs/HOWTO.md`** pour le guide d'utilisation
- **`INDEX.md`** pour trouver un fichier spécifique

**Bon travail avec votre projet !** ✨
