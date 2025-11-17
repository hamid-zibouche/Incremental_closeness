"""
Affiche l'arborescence du projet de manière propre.
"""

from pathlib import Path


def print_tree(directory, prefix="", ignore_dirs=None, ignore_files=None):
    """
    Affiche l'arborescence d'un répertoire.
    
    Args:
        directory: Répertoire racine
        prefix: Préfixe pour l'indentation
        ignore_dirs: Liste de noms de dossiers à ignorer
        ignore_files: Liste de noms de fichiers à ignorer
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', '.vscode', '.idea', 'venv', 'env'}
    if ignore_files is None:
        ignore_files = {'.DS_Store', 'Thumbs.db', '*.pyc'}
    
    directory = Path(directory)
    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        
        # Ignorer certains dossiers/fichiers
        if item.is_dir() and item.name in ignore_dirs:
            continue
        if item.is_file() and any(item.name == ign or item.match(ign) for ign in ignore_files):
            continue
        
        print(prefix + current + item.name)
        
        if item.is_dir():
            print_tree(item, prefix + extension, ignore_dirs, ignore_files)


def main():
    """Point d'entrée principal."""
    root = Path(__file__).parent.parent
    
    print()
    print("="*80)
    print(f"STRUCTURE DU PROJET: {root.name}")
    print("="*80)
    print()
    print(root.name + "/")
    print_tree(root, "")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
