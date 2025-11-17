"""
Script de nettoyage pour supprimer les fichiers temporaires et les résultats.
"""

import os
import shutil
from pathlib import Path


def clean_pycache():
    """Supprime tous les dossiers __pycache__."""
    root = Path(__file__).parent.parent
    deleted = []
    
    for pycache in root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            deleted.append(str(pycache.relative_to(root)))
    
    return deleted


def clean_results(keep_readme=True):
    """Supprime tous les fichiers dans results/ (sauf README.md optionnel)."""
    results_dir = Path(__file__).parent.parent / "results"
    deleted = []
    
    if not results_dir.exists():
        return deleted
    
    for item in results_dir.iterdir():
        if item.is_file():
            if keep_readme and item.name == "README.md":
                continue
            item.unlink()
            deleted.append(str(item.name))
    
    return deleted


def main():
    """Point d'entrée principal."""
    print("="*80)
    print("NETTOYAGE DU PROJET")
    print("="*80)
    print()
    
    # Nettoyer __pycache__
    print("Suppression des dossiers __pycache__...")
    pycache_deleted = clean_pycache()
    if pycache_deleted:
        for p in pycache_deleted:
            print(f"  ✓ Supprimé: {p}")
    else:
        print("  (aucun dossier __pycache__ trouvé)")
    print()
    
    # Nettoyer results/
    print("Suppression des fichiers dans results/...")
    results_deleted = clean_results(keep_readme=True)
    if results_deleted:
        for r in results_deleted:
            print(f"  ✓ Supprimé: {r}")
    else:
        print("  (aucun fichier à supprimer)")
    print()
    
    print("="*80)
    print(f"✓ Nettoyage terminé!")
    print(f"  {len(pycache_deleted)} dossier(s) __pycache__ supprimé(s)")
    print(f"  {len(results_deleted)} fichier(s) de résultats supprimé(s)")
    print("="*80)


if __name__ == "__main__":
    main()
