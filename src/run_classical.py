"""
Calcule les temps de l'algorithme CLASSIQUE et les sauvegarde dans des logs.

Ce script traite chaque graphe dynamique avec l'algorithme classique
(recalcul complet à chaque étape) et sauvegarde les temps dans un fichier JSON.
"""

import time
import json
from pathlib import Path
from graph import DynamicGraph
from classical_closeness import compute_all_closeness_classical
from lecteur_graphe import to_int


def classical_closeness_file(nom: str, input_dir: Path = None) -> dict:
	"""
	Traite un graphe dynamique avec l'algorithme CLASSIQUE.
	À chaque étape, recalcule la closeness complète et mesure le temps.
	
	Args:
		nom: Nom du fichier (ex: "graphe_1.txt")
		input_dir: Dossier d'entrée (par défaut: data/)
	
	Returns:
		dict: {
			'total_steps': nombre d'étapes,
			'time_per_step': liste des temps par étape,
			'cumulative_time': temps total
		}
	"""
	# Déterminer les chemins
	if input_dir is None:
		input_dir = Path(__file__).parent.parent / "data"
	
	input_file = input_dir / nom
	base_name = nom.replace('.txt', '')
	
	if not input_file.exists():
		raise FileNotFoundError(f"Fichier {input_file} introuvable")
	
	print(f"\n{'='*80}")
	print(f"TRAITEMENT CLASSIQUE: {nom}")
	print(f"{'='*80}\n")
	
	# Créer le graphe
	G = DynamicGraph()
	
	# Lire toutes les lignes
	with open(input_file, 'r', encoding='utf-8') as f:
		lines = [line.strip() for line in f if line.strip()]
	
	total_steps = len(lines)
	time_per_step = []
	cumulative_time = 0
	
	print(f"Nombre d'étapes: {total_steps}")
	print(f"Traitement en cours...\n")
	
	# Traiter chaque ligne
	for i, line in enumerate(lines, start=1):
		parts = line.split()
		if not parts:
			continue
		
		cmd = parts[0]
		
		# Mesurer le temps de cette étape
		start_time = time.time()
		
		# Exécuter l'action
		if cmd == "addNode":
			node = to_int(parts[1])
			G.add_node(node)
		
		elif cmd == "removeNode":
			node = to_int(parts[1])
			G.remove_node(node)
		
		elif cmd == "addEdge":
			u, v = to_int(parts[1]), to_int(parts[2])
			G.add_edge(u, v)
		
		elif cmd == "removeEdge":
			u, v = to_int(parts[1]), to_int(parts[2])
			G.remove_edge(u, v)
		
		# ⚠️ RECALCUL COMPLET de la closeness à chaque étape!
		_ = compute_all_closeness_classical(G.G)
		
		step_time = time.time() - start_time
		time_per_step.append(step_time)
		cumulative_time += step_time
		
		# Afficher la progression tous les 10%
		if i % max(1, total_steps // 10) == 0:
			print(f"  Étape {i}/{total_steps} ({i*100//total_steps}%) - "
			      f"Nœuds: {G.G.number_of_nodes()}, "
			      f"Arêtes: {G.G.number_of_edges()}, "
			      f"Temps cumulé: {cumulative_time:.3f}s")
	
	print(f"\n{'='*80}")
	print(f"✓ Traitement terminé")
	print(f"  - Étapes totales: {total_steps}")
	print(f"  - Nœuds finaux: {G.G.number_of_nodes()}")
	print(f"  - Arêtes finales: {G.G.number_of_edges()}")
	print(f"  - Temps total: {cumulative_time:.3f}s")
	print(f"  - Temps moyen par étape: {cumulative_time/total_steps*1000:.2f}ms")
	print(f"{'='*80}\n")
	
	return {
		'total_steps': total_steps,
		'time_per_step': time_per_step,
		'cumulative_time': cumulative_time
	}


def main():
	"""Traite tous les graphes avec l'algorithme classique."""
	data_dir = Path(__file__).parent.parent / "data"
	results_dir = Path(__file__).parent.parent / "results" / "logs_graph"
	results_dir.mkdir(parents=True, exist_ok=True)
	
	# Traiter les 10 graphes avec noms descriptifs
	test_files = [
		"graphe_equilibre.txt",
		"graphe_forte_croissance.txt",
		"graphe_tres_dynamique.txt",
		"graphe_focus_noeuds.txt",
		"graphe_focus_aretes.txt",
		"graphe_croissance_stable.txt",
		"graphe_decroissance.txt",
		"graphe_petit_dense.txt",
		"graphe_grand_sparse.txt",
		"graphe_chaotique.txt",
	]
	
	all_results = {}
	
	for filename in test_files:
		filepath = data_dir / filename
		if filepath.exists():
			try:
				stats = classical_closeness_file(filename)
				base_name = filename.replace('.txt', '')
				all_results[base_name] = stats
			except Exception as e:
				print(f"❌ Erreur lors du traitement de {filename}: {e}\n")
	
	# Sauvegarder tous les temps dans un fichier JSON
	output_file = results_dir / "classical_times.json"
	with open(output_file, 'w', encoding='utf-8') as f:
		json.dump(all_results, f, indent=2)
	
	print("\n" + "="*80)
	print("RÉSUMÉ DES TRAITEMENTS CLASSIQUES")
	print("="*80)
	for filename, stats in all_results.items():
		print(f"\n{filename}:")
		print(f"  Étapes: {stats['total_steps']}")
		print(f"  Temps total: {stats['cumulative_time']:.3f}s")
		print(f"  Temps moyen/étape: {stats['cumulative_time']/stats['total_steps']*1000:.2f}ms")
	
	print(f"\n✓ Temps sauvegardés dans: {output_file}")
	print("="*80 + "\n")


if __name__ == "__main__":
	main()
