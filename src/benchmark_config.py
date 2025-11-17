# Configuration du Benchmark
# ===========================

# Tailles de graphes à tester (nombre_de_nœuds, m_arêtes_par_nouveau_nœud)
GRAPH_SIZES = [
    (50, 3),
    (100, 3),
    (200, 3),
    (300, 3),
    (400, 3),
    (500, 3),
    (600, 3),
    (700, 3),
    (800, 3),
    (900, 3),
]

# Nombre de runs par configuration (pour moyenner les résultats)
NUM_RUNS = 1

# Tolérance pour la vérification de correction (différence acceptée)
TOLERANCE = 1e-5

# Dossier de sortie pour les résultats
RESULTS_DIR = "../results"

# Options d'affichage
VERBOSE = True  # Afficher les détails pendant l'exécution
SHOW_PROGRESS = True  # Afficher la barre de progression
