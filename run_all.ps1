# ============================================================================
# Script d'exécution complète du projet Incremental Closeness Centrality
# ============================================================================
# Ce script permet de reproduire tous les résultats du projet :
# 1. Génération des graphes dynamiques
# 2. Traitement avec l'algorithme incrémental
# 3. Traitement avec l'algorithme classique
# 4. Génération des courbes de comparaison
# 5. Vérification de la correction des résultats
# 6. Génération des visualisations interactives
# ============================================================================

param(
    [switch]$GenerateGraphs,
    [switch]$RunIncremental,
    [switch]$RunClassical,
    [switch]$PlotComparison,
    [switch]$Verify,
    [switch]$Visualize,
    [switch]$Benchmark,
    [switch]$All,
    [switch]$Quick,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$SrcDir = Join-Path $ProjectRoot "src"
$DataDir = Join-Path $ProjectRoot "data"
$ResultsDir = Join-Path $ProjectRoot "results"

# Fonction d'affichage
function Write-Section {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

# Fonction d'aide
function Show-Help {
    Write-Host @"
Usage: .\run_all.ps1 [OPTIONS]

OPTIONS:
    -GenerateGraphs    Genere les 10 graphes dynamiques
    -RunIncremental    Execute l'algorithme incremental sur tous les graphes
    -RunClassical      Execute l'algorithme classique sur tous les graphes
    -PlotComparison    Genere les courbes de comparaison des temps
    -Verify            Verifie la correction des resultats (echantillonnage)
    -Visualize         Genere les visualisations interactives PyVis
    -Benchmark         Execute le benchmark sur graphes Barabasi-Albert (tailles variees)
    -All               Execute tout le pipeline complet
    -Quick             Mode rapide : genere, traite et visualise (sans classique)
    -Help              Affiche cette aide

EXEMPLES:
    # Execution complete (recommande pour evaluation)
    .\run_all.ps1 -All

    # Mode rapide (sans algorithme classique, plus rapide)
    .\run_all.ps1 -Quick

    # Seulement la generation et le traitement incremental
    .\run_all.ps1 -GenerateGraphs -RunIncremental

    # Regenerer les visualisations
    .\run_all.ps1 -PlotComparison -Visualize

    # Executer le benchmark sur graphes Barabasi-Albert
    .\run_all.ps1 -Benchmark

NOTES:
    - L'option -All peut prendre 15-30 minutes (algorithme classique lent)
    - L'option -Quick prend environ 5 minutes
    - Les resultats sont sauvegardes dans ./results/

"@ -ForegroundColor White
}

# Vérifier Python
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python detecte: $pythonVersion"
        return $true
    } catch {
        Write-Error-Custom "Python n'est pas installe ou n'est pas dans le PATH"
        return $false
    }
}

# Vérifier les dépendances Python
function Test-Dependencies {
    Write-Section "VERIFICATION DES DEPENDANCES"
    
    $requiredPackages = @("networkx", "matplotlib", "numpy", "pyvis")
    $missing = @()
    
    foreach ($package in $requiredPackages) {
        $result = python -c "import $package" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$package installe"
        } else {
            Write-Error-Custom "$package manquant"
            $missing += $package
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Info "Installation des dependances manquantes..."
        pip install $missing
    }
}

# 1. Génération des graphes
function Invoke-GenerateGraphs {
    Write-Section "ETAPE 1: GENERATION DES GRAPHES DYNAMIQUES"
    Write-Info "Generation de 10 graphes avec differentes caracteristiques..."
    
    Push-Location $SrcDir
    python generateur_graphs.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Graphes generes dans $DataDir"
        $graphCount = (Get-ChildItem "$DataDir\graphe_*.txt").Count
        Write-Info "$graphCount fichiers graphe_*.txt crees"
    } else {
        Write-Error-Custom "Erreur lors de la generation des graphes"
        exit 1
    }
}

# 2. Algorithme incrémental
function Invoke-RunIncremental {
    Write-Section "ETAPE 2: EXECUTION DE L'ALGORITHME INCREMENTAL"
    Write-Info "Traitement de tous les graphes avec l'algorithme incremental..."
    Write-Info "Cela peut prendre 2-5 minutes..."
    
    Push-Location $SrcDir
    python run_incremental.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Algorithme incremental termine"
        Write-Info "Resultats sauvegardes dans $ResultsDir\logs_graph\"
        Write-Info "  - incremental_times.json (temps de calcul)"
        Write-Info "  - evolution/ (etats du graphe)"
        Write-Info "  - scores/ (scores de closeness)"
    } else {
        Write-Error-Custom "Erreur lors de l'execution de l'algorithme incremental"
        exit 1
    }
}

# 3. Algorithme classique
function Invoke-RunClassical {
    Write-Section "ETAPE 3: EXECUTION DE L'ALGORITHME CLASSIQUE"
    Write-Info "Traitement de tous les graphes avec l'algorithme classique..."
    Write-Info "ATTENTION: Cela peut prendre 15-30 minutes (algorithme O(n²))..."
    
    $confirm = Read-Host "Voulez-vous continuer? (O/N)"
    if ($confirm -ne "O" -and $confirm -ne "o") {
        Write-Info "Algorithme classique ignore"
        return
    }
    
    Push-Location $SrcDir
    python run_classical.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Algorithme classique termine"
        Write-Info "Resultats sauvegardes dans $ResultsDir\logs_graph\classical_times.json"
    } else {
        Write-Error-Custom "Erreur lors de l'execution de l'algorithme classique"
        exit 1
    }
}

# 4. Génération des courbes
function Invoke-PlotComparison {
    Write-Section "ETAPE 4: GENERATION DES COURBES DE COMPARAISON"
    Write-Info "Creation des visualisations de temps..."
    
    Push-Location $SrcDir
    python plot_comparison.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Courbes generees"
        Write-Info "Fichiers crees dans $ResultsDir\time_curves\"
        Write-Info "  - incremental_vs_classical.png"
        Write-Info "  - time_per_step_all_graphs.png"
        Write-Info "  - time_statistics.txt"
    } else {
        Write-Error-Custom "Erreur lors de la generation des courbes"
        exit 1
    }
}

# 5. Vérification des résultats
function Invoke-Verify {
    Write-Section "ETAPE 5: VERIFICATION DE LA CORRECTION"
    Write-Info "Verification que incremental == classique (echantillonnage)..."
    Write-Info "Cela peut prendre 5-10 minutes..."
    
    Push-Location $SrcDir
    python verification_resultats.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Verification terminee"
    } else {
        Write-Error-Custom "Erreur lors de la verification"
        exit 1
    }
}

# 6. Visualisations interactives
function Invoke-Visualize {
    Write-Section "ETAPE 6: GENERATION DES VISUALISATIONS INTERACTIVES"
    Write-Info "Creation des graphes interactifs PyVis..."
    Write-Info "Cela peut prendre 10-15 minutes..."
    
    Push-Location $SrcDir
    python "test_comparison&visualisation.py"
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Visualisations generees"
        Write-Info "Fichiers HTML crees dans $ResultsDir\visualisation\"
        $htmlCount = (Get-ChildItem "$ResultsDir\visualisation\*.html").Count
        Write-Info "$htmlCount fichiers HTML generes"
    } else {
        Write-Error-Custom "Erreur lors de la generation des visualisations"
        exit 1
    }
}

# 7. Benchmark
function Invoke-Benchmark {
    Write-Section "ETAPE 7: BENCHMARK SUR GRAPHES BARABASI-ALBERT"
    Write-Info "Test sur graphes de tailles variees (50-900 noeuds)..."
    Write-Info "Cela peut prendre 10-15 minutes..."
    
    Push-Location $SrcDir
    python benchmark_performance.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Benchmark termine"
        Write-Info "Resultats sauvegardes dans $ResultsDir\benchmark_results.csv"
    } else {
        Write-Error-Custom "Erreur lors de l'execution du benchmark"
        exit 1
    }
}

# Résumé final
function Show-Summary {
    Write-Section "RESUME DES RESULTATS"
    
    Write-Host "Structure des resultats:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "results/" -ForegroundColor Cyan
    Write-Host "├── logs_graph/" -ForegroundColor Cyan
    Write-Host "│   ├── incremental_times.json" -ForegroundColor White
    Write-Host "│   ├── classical_times.json" -ForegroundColor White
    Write-Host "│   ├── evolution/    (etats des graphes)" -ForegroundColor Gray
    Write-Host "│   └── scores/       (scores de closeness)" -ForegroundColor Gray
    Write-Host "├── time_curves/" -ForegroundColor Cyan
    Write-Host "│   ├── incremental_vs_classical.png" -ForegroundColor White
    Write-Host "│   ├── time_per_step_all_graphs.png" -ForegroundColor White
    Write-Host "│   └── time_statistics.txt" -ForegroundColor White
    Write-Host "└── visualisation/" -ForegroundColor Cyan
    Write-Host "    ├── graphe_equilibre_classique.html" -ForegroundColor White
    Write-Host "    ├── graphe_equilibre_incremental.html" -ForegroundColor White
    Write-Host "    └── ..." -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Fichiers principaux a consulter:" -ForegroundColor Yellow
    Write-Host "  1. results/time_curves/incremental_vs_classical.png" -ForegroundColor Green
    Write-Host "     -> Comparaison des temps cumules" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. results/time_curves/time_statistics.txt" -ForegroundColor Green
    Write-Host "     -> Statistiques detaillees (speedup, etc.)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. results/visualisation/*.html" -ForegroundColor Green
    Write-Host "     -> Graphes interactifs (ouvrir dans un navigateur)" -ForegroundColor Gray
    Write-Host ""
}

# ============================================================================
# MAIN
# ============================================================================

Write-Host @"

████████████████████████████████████████████████████████████████████████████████
█                                                                              █
█            INCREMENTAL CLOSENESS CENTRALITY - PROJET M2 STL                 █
█                                                                              █
████████████████████████████████████████████████████████████████████████████████

"@ -ForegroundColor Cyan

if ($Help) {
    Show-Help
    exit 0
}

# Vérifier Python
if (-not (Test-Python)) {
    exit 1
}

# Vérifier les dépendances
Test-Dependencies

# Exécution selon les options
if ($All) {
    Write-Info "Mode COMPLET active (toutes les etapes)"
    Invoke-GenerateGraphs
    Invoke-RunIncremental
    Invoke-RunClassical
    Invoke-PlotComparison
    Invoke-Verify
    Invoke-Visualize
    Show-Summary
}
elseif ($Quick) {
    Write-Info "Mode RAPIDE active (sans algorithme classique)"
    Invoke-GenerateGraphs
    Invoke-RunIncremental
    Write-Info "Visualisations (limite aux 3 premiers graphes)..."
    Invoke-Visualize
    Write-Success "Mode rapide termine"
}
else {
    $executed = $false
    
    if ($GenerateGraphs) {
        Invoke-GenerateGraphs
        $executed = $true
    }
    
    if ($RunIncremental) {
        Invoke-RunIncremental
        $executed = $true
    }
    
    if ($RunClassical) {
        Invoke-RunClassical
        $executed = $true
    }
    
    if ($PlotComparison) {
        Invoke-PlotComparison
        $executed = $true
    }
    
    if ($Verify) {
        Invoke-Verify
        $executed = $true
    }
    
    if ($Visualize) {
        Invoke-Visualize
        $executed = $true
    }
    
    if ($Benchmark) {
        Invoke-Benchmark
        $executed = $true
    }
    
    if (-not $executed) {
        Write-Info "Aucune option specifiee. Utilisez -Help pour voir les options disponibles."
        Write-Info "Exemple: .\run_all.ps1 -All"
    }
}

Write-Host "`n" -NoNewline
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "TERMINE" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""
