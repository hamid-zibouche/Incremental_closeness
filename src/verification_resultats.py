"""
Vérification étape par étape : compare les scores incrémentaux avec l'algorithme classique.

Pour chaque étape i:
1. Lit le graphe depuis evolution/graphe_nom_i.txt
2. Calcule la closeness avec l'algorithme classique
3. Compare avec les scores dans scores/graphe_nom_score_i.txt
4. Signale toute différence > seuil de tolérance
"""

from pathlib import Path
import networkx as nx
from classical_closeness import compute_all_closeness_classical
from lecteur_graphe import to_int
import time


def load_graph_from_evolution(filepath: Path):
	"""
	Charge un graphe depuis un fichier evolution/graphe_nom_i.txt
	
	Returns:
		nx.DiGraph: Graphe chargé (orienté, car on travaille avec DiGraph)
	"""
	G = nx.DiGraph()
	
	with open(filepath, 'r', encoding='utf-8') as f:
		lines = [line.strip() for line in f if line.strip()]
	
	# Parser le fichier
	mode = None
	for line in lines:
		if line.startswith('#'):
			if 'Nodes:' in line:
				mode = 'nodes'
			elif 'Edges:' in line:
				mode = 'edges'
			continue
		
		if mode == 'nodes':
			node = to_int(line)
			G.add_node(node)
		elif mode == 'edges':
			parts = line.split()
			if len(parts) == 2:
				u, v = to_int(parts[0]), to_int(parts[1])
				# Arête non orientée = 2 arcs
				G.add_edge(u, v)
				G.add_edge(v, u)
	
	return G


def load_scores_from_file(filepath: Path) -> dict:
	"""
	Charge les scores depuis scores/graphe_nom_score_i.txt
	
	Returns:
		dict: {node_id: closeness_value}
	"""
	scores = {}
	
	with open(filepath, 'r', encoding='utf-8') as f:
		for node_id, line in enumerate(f):
			line = line.strip()
			if line:
				value = float(line)
				if value > 0:  # Ignorer les nœuds supprimés (0.0)
					scores[node_id] = value
	
	return scores


def verify_single_step(base_name: str, step: int, evolution_dir: Path, scores_dir: Path, 
                       tolerance: float = 1e-9) -> dict:
	"""
	Vérifie une étape unique.
	
	Returns:
		dict: {
			'step': numéro d'étape,
			'nodes_count': nombre de nœuds,
			'edges_count': nombre d'arêtes,
			'max_diff': différence maximale trouvée,
			'mismatches': liste des nœuds avec différences > tolérance,
			'is_valid': True si tout correspond
		}
	"""
	# Charger le graphe et les scores
	graph_file = evolution_dir / f"{base_name}_{step}.txt"
	score_file = scores_dir / f"{base_name}_score_{step}.txt"
	
	if not graph_file.exists() or not score_file.exists():
		return {
			'step': step,
			'error': f"Fichiers manquants pour l'étape {step}"
		}
	
	# Charger
	G = load_graph_from_evolution(graph_file)
	incremental_scores = load_scores_from_file(score_file)
	
	# Calculer avec classique
	classical_scores = compute_all_closeness_classical(G)
	
	# Comparer
	mismatches = []
	max_diff = 0.0
	
	# Vérifier que tous les nœuds du graphe ont un score
	for node in G.nodes():
		classical_val = classical_scores.get(node, 0.0)
		incremental_val = incremental_scores.get(node, 0.0)
		
		diff = abs(classical_val - incremental_val)
		max_diff = max(max_diff, diff)
		
		if diff > tolerance:
			mismatches.append({
				'node': node,
				'classical': classical_val,
				'incremental': incremental_val,
				'diff': diff
			})
	
	return {
		'step': step,
		'nodes_count': G.number_of_nodes(),
		'edges_count': G.number_of_edges() // 2,  # Arêtes non orientées
		'max_diff': max_diff,
		'mismatches': mismatches,
		'is_valid': len(mismatches) == 0
	}


def verify_all_steps(base_name: str, total_steps: int, tolerance: float = 1e-9, 
                     sample_rate: int = 1) -> dict:
	"""
	Vérifie toutes les étapes d'un graphe dynamique.
	
	Args:
		base_name: Nom de base du graphe (ex: "graphe_equilibre")
		total_steps: Nombre total d'étapes
		tolerance: Seuil de tolérance pour la comparaison
		sample_rate: Vérifier 1 étape sur N (1 = toutes, 10 = 1/10)
	
	Returns:
		dict: Statistiques complètes de la vérification
	"""
	results_dir = Path(__file__).parent.parent / "results" / "logs_graph"
	evolution_dir = results_dir / "evolution"
	scores_dir = results_dir / "scores"
	
	print(f"\n{'='*80}")
	print(f"VÉRIFICATION: {base_name} ({total_steps} étapes)")
	print(f"{'='*80}\n")
	
	all_results = []
	errors = []
	total_valid = 0
	total_invalid = 0
	
	steps_to_check = range(1, total_steps + 1, sample_rate)
	
	start_time = time.time()
	
	for i, step in enumerate(steps_to_check, 1):
		result = verify_single_step(base_name, step, evolution_dir, scores_dir, tolerance)
		
		if 'error' in result:
			errors.append(result)
			print(f" Étape {step}: {result['error']}")
		else:
			all_results.append(result)
			
			if result['is_valid']:
				total_valid += 1
			else:
				total_invalid += 1
				print(f"⚠️  Étape {step}: {len(result['mismatches'])} différences trouvées "
				      f"(max: {result['max_diff']:.2e})")
				# Afficher les 3 premières différences
				for mismatch in result['mismatches'][:3]:
					print(f"   - Nœud {mismatch['node']}: "
					      f"classique={mismatch['classical']:.10f}, "
					      f"incrémental={mismatch['incremental']:.10f}, "
					      f"diff={mismatch['diff']:.2e}")
				if len(result['mismatches']) > 3:
					print(f"   ... et {len(result['mismatches']) - 3} autres")
		
		# Progression tous les 10%
		if i % max(1, len(list(steps_to_check)) // 10) == 0 or i == len(list(steps_to_check)):
			progress = (i / len(list(steps_to_check))) * 100
			print(f"  Progression: {progress:.0f}% (étape {step}/{total_steps})")
	
	elapsed_time = time.time() - start_time
	
	# Résumé
	print(f"\n{'='*80}")
	print(f"RÉSUMÉ DE LA VÉRIFICATION")
	print(f"{'='*80}")
	print(f"  Étapes vérifiées: {len(all_results)}")
	print(f"  ✓ Valides: {total_valid}")
	print(f"  ✗ Invalides: {total_invalid}")
	print(f"  Erreurs: {len(errors)}")
	print(f"  Temps total: {elapsed_time:.3f}s")
	
	if total_invalid == 0 and len(errors) == 0:
		print(f"\n  🎉 SUCCÈS: Tous les scores correspondent! 🎉")
	else:
		print(f"\n  ⚠️  ATTENTION: Des différences ont été détectées!")
	
	print(f"{'='*80}\n")
	
	return {
		'base_name': base_name,
		'total_steps': total_steps,
		'steps_checked': len(all_results),
		'valid_steps': total_valid,
		'invalid_steps': total_invalid,
		'errors': errors,
		'all_results': all_results,
		'elapsed_time': elapsed_time
	}


def main():
	"""Fonction de test."""
	# Vérifier les 10 graphes générés avec noms descriptifs
	test_cases = [
		("graphe_equilibre", 1500),
		("graphe_forte_croissance", 1700),
		("graphe_tres_dynamique", 2000),
		("graphe_focus_noeuds", 1300),
		("graphe_focus_aretes", 2500),
		("graphe_croissance_stable", 2300),
		("graphe_decroissance", 1900),
		("graphe_petit_dense", 1100),
		("graphe_grand_sparse", 3000),
		("graphe_chaotique", 2200),
	]
	
	all_stats = {}
	
	for base_name, total_steps in test_cases:
		stats = verify_all_steps(base_name, total_steps, tolerance=1e-9, sample_rate=10)  # Échantillonner 1/10 pour être plus rapide
		all_stats[base_name] = stats
	
	# Résumé global
	print("\n" + "="*80)
	print("RÉSUMÉ GLOBAL")
	print("="*80)
	for base_name, stats in all_stats.items():
		print(f"\n{base_name}:")
		print(f"  Étapes vérifiées: {stats['steps_checked']}")
		print(f"  Valides: {stats['valid_steps']}")
		print(f"  Invalides: {stats['invalid_steps']}")
		print(f"  Temps: {stats['elapsed_time']:.3f}s")
		
		if stats['invalid_steps'] == 0:
			print(f"  Statut: ✓ VALIDE")
		else:
			print(f"  Statut: ✗ INVALIDE")


if __name__ == "__main__":
	main()
