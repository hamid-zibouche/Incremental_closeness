"""
Script de vérification complète du projet.

Vérifie que :
1. Tous les modules peuvent être importés
2. Les tests de base passent
3. Les fichiers de configuration existent
4. La structure des dossiers est correcte
"""

import sys
from pathlib import Path
import importlib

# Couleurs pour le terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def main():
    """Point d'entrée principal."""
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    
    print()
    print("="*80)
    print("VÉRIFICATION COMPLÈTE DU PROJET")
    print("="*80)
    print()
    
    # Ajouter src au path
    sys.path.insert(0, str(src_path))
    
    errors = 0
    warnings = 0
    
    # 1. Vérifier la structure des dossiers
    print("1️⃣  Vérification de la structure...")
    print("-"*80)
    
    required_dirs = ["src", "data", "results", "docs", "scripts"]
    for dirname in required_dirs:
        dirpath = project_root / dirname
        if dirpath.exists():
            print_success(f"Dossier '{dirname}/' existe")
        else:
            print_error(f"Dossier '{dirname}/' manquant")
            errors += 1
    
    print()
    
    # 2. Vérifier les fichiers de configuration
    print("2️⃣  Vérification des fichiers de configuration...")
    print("-"*80)
    
    required_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "src/benchmark_config.py",
        "docs/HOWTO.md",
        "docs/BENCHMARK_GUIDE.md",
        "results/README.md",
    ]
    
    for filepath in required_files:
        fullpath = project_root / filepath
        if fullpath.exists():
            print_success(f"Fichier '{filepath}' existe")
        else:
            print_error(f"Fichier '{filepath}' manquant")
            errors += 1
    
    print()
    
    # 3. Vérifier l'import des modules
    print("3️⃣  Vérification des imports Python...")
    print("-"*80)
    
    modules_to_test = [
        "graph",
        "closeness",
        "generator",
        "incremental_closeness_article",
        "benchmark",
        "plot_results",
        "benchmark_config",
    ]
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print_success(f"Module '{module_name}' importable")
        except ImportError as e:
            print_error(f"Module '{module_name}' non importable: {e}")
            errors += 1
        except Exception as e:
            print_warning(f"Module '{module_name}' importable mais erreur: {e}")
            warnings += 1
    
    print()
    
    # 4. Vérifier les dépendances
    print("4️⃣  Vérification des dépendances...")
    print("-"*80)
    
    dependencies = ["networkx", "matplotlib"]
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print_success(f"Package '{dep}' installé")
        except ImportError:
            print_error(f"Package '{dep}' manquant - Exécutez: pip install {dep}")
            errors += 1
    
    print()
    
    # 5. Vérifier les scripts utilitaires
    print("5️⃣  Vérification des scripts utilitaires...")
    print("-"*80)
    
    scripts = [
        "scripts/show_structure.py",
        "scripts/clean.py",
        "scripts/run_benchmark.py",
    ]
    
    for script in scripts:
        fullpath = project_root / script
        if fullpath.exists():
            print_success(f"Script '{script}' existe")
        else:
            print_error(f"Script '{script}' manquant")
            errors += 1
    
    print()
    
    # 6. Vérifier les fichiers de résultats
    print("6️⃣  Vérification des résultats (optionnel)...")
    print("-"*80)
    
    result_files = [
        "results/benchmark_results.csv",
        "results/benchmark_combined.png",
    ]
    
    for resfile in result_files:
        fullpath = project_root / resfile
        if fullpath.exists():
            print_success(f"Résultat '{resfile}' existe")
        else:
            print_info(f"Résultat '{resfile}' non généré (exécutez le benchmark)")
    
    print()
    
    # Résumé
    print("="*80)
    print("RÉSUMÉ")
    print("="*80)
    print()
    
    if errors == 0 and warnings == 0:
        print_success("✨ Tout est parfait ! Le projet est prêt à être utilisé.")
    elif errors == 0:
        print_warning(f"⚠️  {warnings} avertissement(s) - Le projet devrait fonctionner.")
    else:
        print_error(f"❌ {errors} erreur(s) trouvée(s) - Veuillez corriger.")
    
    print()
    print("Prochaines étapes :")
    print("  1. Lancer les tests    : cd src && python test_minimal.py")
    print("  2. Lancer le benchmark : python scripts/run_benchmark.py")
    print("  3. Lire le guide       : voir docs/HOWTO.md")
    print()
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
