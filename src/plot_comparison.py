"""
Génère les courbes de temps pour les graphes dynamiques.

Ce script lit les temps depuis les fichiers JSON et génère:
1. Comparaison incrémental vs classique (temps cumulé)
2. Temps par étape pour les deux méthodes (10 graphes)
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json


def load_times_from_json() -> tuple:
	"""
	Charge les temps depuis les fichiers JSON.
	
	Returns:
		tuple: (incremental_data, classical_data)
	"""
	results_dir = Path(__file__).parent.parent / "results" / "logs_graph"
	
	incremental_file = results_dir / "incremental_times.json"
	classical_file = results_dir / "classical_times.json"
	
	incremental_data = {}
	classical_data = {}
	
	if incremental_file.exists():
		with open(incremental_file, 'r', encoding='utf-8') as f:
			incremental_data = json.load(f)
		print(f"✓ Chargé: {incremental_file}")
	else:
		print(f"⚠️  Fichier manquant: {incremental_file}")
	
	if classical_file.exists():
		with open(classical_file, 'r', encoding='utf-8') as f:
			classical_data = json.load(f)
		print(f"✓ Chargé: {classical_file}")
	else:
		print(f"⚠️  Fichier manquant: {classical_file}")
	
	return incremental_data, classical_data


def plot_incremental_vs_classical(incremental_data: dict, classical_data: dict, output_dir: Path):
	"""
	Compare temps incrémental vs classique pour tous les graphes.
	"""
	# Créer une grille 2x5 pour les 10 graphes
	fig, axes = plt.subplots(2, 5, figsize=(20, 8))
	axes = axes.flatten()
	
	for idx, graph_name in enumerate(sorted(incremental_data.keys())):
		if idx >= 10:
			break
		
		ax = axes[idx]
		
		# Données incrémentales
		incr_stats = incremental_data[graph_name]
		steps = range(1, len(incr_stats['time_per_step']) + 1)
		incr_cumulative = np.cumsum(incr_stats['time_per_step'])
		
		# Données classiques (si disponibles)
		if graph_name in classical_data:
			class_stats = classical_data[graph_name]
			class_cumulative = np.cumsum(class_stats['time_per_step'])
			
			# Tracer les deux courbes
			ax.plot(steps, incr_cumulative, label='Incrémental', 
			        linewidth=2, color='green', marker='o', markersize=2, 
			        markevery=max(1, len(steps)//20))
			ax.plot(steps, class_cumulative, label='Classique', 
			        linewidth=2, color='red', linestyle='--', marker='s', 
			        markersize=2, markevery=max(1, len(steps)//20))
			
			# Calculer et afficher le speedup
			speedup = class_cumulative[-1] / incr_cumulative[-1]
			ax.text(0.5, 0.95, f'Speedup: {speedup:.2f}x', 
			        transform=ax.transAxes, fontsize=9, 
			        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
			        verticalalignment='top', horizontalalignment='center')
		else:
			# Seulement l'incrémental
			ax.plot(steps, incr_cumulative, label='Incrémental', 
			        linewidth=2, color='green', marker='o', markersize=2,
			        markevery=max(1, len(steps)//20))
			ax.text(0.5, 0.95, 'Classique non disponible', 
			        transform=ax.transAxes, fontsize=8, 
			        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5),
			        verticalalignment='top', horizontalalignment='center')
		
		ax.set_xlabel('Étape', fontsize=9)
		ax.set_ylabel('Temps cumulé (s)', fontsize=9)
		ax.set_title(f'{graph_name}', fontsize=10, fontweight='bold')
		ax.legend(loc='upper left', fontsize=8)
		ax.grid(True, alpha=0.3)
		ax.tick_params(labelsize=8)
	
	plt.suptitle('Comparaison Incrémental vs Classique - Temps Cumulé', 
	             fontsize=14, fontweight='bold')
	plt.tight_layout()
	
	output_file = output_dir / "incremental_vs_classical.png"
	plt.savefig(output_file, dpi=300, bbox_inches='tight')
	print(f"✓ Sauvegardé: {output_file}")
	plt.close()


def plot_time_per_step_comparison(incremental_data: dict, classical_data: dict, output_dir: Path):
	"""
	Trace le temps par étape pour les deux méthodes (10 graphes).
	"""
	fig, axes = plt.subplots(2, 5, figsize=(20, 8))
	axes = axes.flatten()
	
	for idx, graph_name in enumerate(sorted(incremental_data.keys())):
		if idx >= 10:
			break
		
		ax = axes[idx]
		
		# Données incrémentales
		incr_stats = incremental_data[graph_name]
		steps = range(1, len(incr_stats['time_per_step']) + 1)
		incr_times_ms = [t * 1000 for t in incr_stats['time_per_step']]
		
		# Tracer incrémental
		ax.plot(steps, incr_times_ms, linewidth=1, color='green', 
		        alpha=0.7, label='Incrémental')
		ax.fill_between(steps, incr_times_ms, alpha=0.2, color='green')
		
		# Données classiques (si disponibles)
		if graph_name in classical_data:
			class_stats = classical_data[graph_name]
			class_times_ms = [t * 1000 for t in class_stats['time_per_step']]
			
			# Tracer classique
			ax.plot(steps, class_times_ms, linewidth=1, color='red', 
			        alpha=0.7, label='Classique', linestyle='--')
			ax.fill_between(steps, class_times_ms, alpha=0.2, color='red')
		
		ax.set_xlabel('Étape', fontsize=9)
		ax.set_ylabel('Temps (ms)', fontsize=9)
		ax.set_title(graph_name, fontsize=10, fontweight='bold')
		ax.legend(loc='upper left', fontsize=8)
		ax.grid(True, alpha=0.3)
		ax.tick_params(labelsize=8)
		
		# Échelle log si les valeurs varient beaucoup
		if graph_name in classical_data:
			ratio = max(class_times_ms) / max(incr_times_ms) if max(incr_times_ms) > 0 else 1
			if ratio > 10:
				ax.set_yscale('log')
	
	plt.suptitle('Temps par Étape - Comparaison des Deux Méthodes', 
	             fontsize=14, fontweight='bold')
	plt.tight_layout()
	
	output_file = output_dir / "time_per_step_all_graphs.png"
	plt.savefig(output_file, dpi=300, bbox_inches='tight')
	print(f"✓ Sauvegardé: {output_file}")
	plt.close()


def generate_summary_stats(incremental_data: dict, classical_data: dict, output_dir: Path):
	"""
	Génère un fichier de statistiques récapitulatives.
	"""
	output_file = output_dir / "time_statistics.txt"
	
	with open(output_file, 'w', encoding='utf-8') as f:
		f.write("="*80 + "\n")
		f.write("STATISTIQUES DE TEMPS - COMPARAISON INCRÉMENTAL VS CLASSIQUE\n")
		f.write("="*80 + "\n\n")
		
		for graph_name in sorted(incremental_data.keys()):
			incr_stats = incremental_data[graph_name]
			
			f.write(f"{graph_name}:\n")
			f.write(f"  Nombre d'étapes: {incr_stats['total_steps']}\n\n")
			
			f.write(f"  INCRÉMENTAL:\n")
			f.write(f"    Temps total: {incr_stats['cumulative_time']:.4f}s\n")
			f.write(f"    Temps moyen/étape: {np.mean(incr_stats['time_per_step'])*1000:.4f}ms\n")
			f.write(f"    Temps médian/étape: {np.median(incr_stats['time_per_step'])*1000:.4f}ms\n")
			f.write(f"    Temps max/étape: {max(incr_stats['time_per_step'])*1000:.4f}ms\n\n")
			
			if graph_name in classical_data:
				class_stats = classical_data[graph_name]
				speedup = class_stats['cumulative_time'] / incr_stats['cumulative_time']
				
				f.write(f"  CLASSIQUE:\n")
				f.write(f"    Temps total: {class_stats['cumulative_time']:.4f}s\n")
				f.write(f"    Temps moyen/étape: {np.mean(class_stats['time_per_step'])*1000:.4f}ms\n")
				f.write(f"    Temps médian/étape: {np.median(class_stats['time_per_step'])*1000:.4f}ms\n")
				f.write(f"    Temps max/étape: {max(class_stats['time_per_step'])*1000:.4f}ms\n\n")
				
				f.write(f"  SPEEDUP: {speedup:.2f}x\n")
			else:
				f.write(f"  CLASSIQUE: Non calculé\n")
			
			f.write("\n" + "-"*80 + "\n\n")
	
	print(f"✓ Statistiques sauvegardées: {output_file}")


def main():
	"""Point d'entrée principal."""
	print("\n" + "="*80)
	print("GÉNÉRATION DES COURBES DE TEMPS")
	print("="*80 + "\n")
	
	# Créer le dossier de sortie
	output_dir = Path(__file__).parent.parent / "results" / "time_curves"
	output_dir.mkdir(parents=True, exist_ok=True)
	
	# Charger les données depuis les JSON
	print("Chargement des données...\n")
	incremental_data, classical_data = load_times_from_json()
	
	if not incremental_data:
		print("\n❌ Aucune donnée incrémentale trouvée!")
		print("   Exécutez d'abord: python incremental_closeness_file.py")
		return
	
	if not classical_data:
		print("\n⚠️  Aucune donnée classique trouvée!")
		print("   Pour générer: python classical_closeness_file.py")
		print("   (⚠️  Attention: peut prendre plusieurs minutes!)\n")
	
	print(f"\n✓ {len(incremental_data)} graphes incrémentaux chargés")
	if classical_data:
		print(f"✓ {len(classical_data)} graphes classiques chargés\n")
	
	# Générer les courbes
	print("Génération des visualisations...\n")
	
	print("1. Comparaison incrémental vs classique (temps cumulé)...")
	plot_incremental_vs_classical(incremental_data, classical_data, output_dir)
	
	print("\n2. Temps par étape (comparaison)...")
	plot_time_per_step_comparison(incremental_data, classical_data, output_dir)
	
	print("\n3. Statistiques récapitulatives...")
	generate_summary_stats(incremental_data, classical_data, output_dir)
	
	print("\n" + "="*80)
	print(f"✓ Toutes les visualisations générées dans: {output_dir}")
	print("="*80 + "\n")
	
	print("Fichiers générés:")
	for file in sorted(output_dir.glob("*.png")):
		print(f"  - {file.name}")
	print(f"  - time_statistics.txt\n")


if __name__ == "__main__":
	main()
