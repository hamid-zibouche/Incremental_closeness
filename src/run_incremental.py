from pathlib import Path
from incremental_closeness_article import IncrementalClosenessArticle
from classical_closeness import compute_all_closeness_classical
from graph import DynamicGraph
import time


def to_int(s: str) -> int:
	"""Convertit 'n0' en 0, 'n1' en 1, etc."""
	if s.startswith('n'):
		return int(s[1:])
	return int(s)


def write_graph_state(graphe, filename: Path):
	"""
	Écrit la forme du graphe dans un fichier.
	Format: Une ligne par arête "u v"
	"""
	with open(filename, 'w', encoding='utf-8') as f:
		# Écrire les nœuds
		nodes = sorted(graphe.G.nodes())
		f.write(f"# Nodes: {len(nodes)}\n")
		for node in nodes:
			f.write(f"n{node}\n")
		
		# Écrire les arêtes (non orientées = une seule fois)
		f.write(f"# Edges: {graphe.G.number_of_edges() // 2}\n")
		edges_seen = set()
		for u, v in graphe.G.edges():
			edge = tuple(sorted((u, v)))
			if edge not in edges_seen:
				edges_seen.add(edge)
				f.write(f"n{u} n{v}\n")


def write_closeness_scores(closeness: dict, filename: Path):
	"""
	Écrit les scores de closeness dans un fichier.
	Ligne j contient la closeness du nœud j.
	"""
	with open(filename, 'w', encoding='utf-8') as f:
		if not closeness:
			return
		
		# Trouver le nœud max pour savoir combien de lignes écrire
		max_node = max(closeness.keys()) if closeness else -1
		
		# Écrire une ligne par nœud (même si le nœud n'existe pas)
		for node_id in range(max_node + 1):
			if node_id in closeness:
				f.write(f"{closeness[node_id]:.10f}\n")
			else:
				f.write("0.0\n")  # Nœud supprimé ou inexistant


def incremental_closeness_file(nom: str, input_dir: Path = None) -> dict:
	"""
	Lit le fichier nom contenant un graphe dynamique et construit le graphe
	en mettant à jour la closeness à chaque étape.
	
	Args:
		nom: Nom du fichier contenant le graphe dynamique (ex: "graphe.txt")
		input_dir: Dossier d'entrée (par défaut: data/)
	
	Returns:
		dict: Statistiques {
			'total_steps': nombre d'étapes,
			'final_nodes': nombre de nœuds finaux,
			'final_edges': nombre d'arêtes finales,
			'time_per_step': liste des temps par étape,
			'cumulative_time': temps cumulé total
		}
	"""
	# Déterminer les chemins
	if input_dir is None:
		input_dir = Path(__file__).parent.parent / "data"
	
	input_file = input_dir / nom
	base_name = nom.replace('.txt', '')
	
	# Créer les dossiers de sortie dans results/logs_graph/
	results_dir = Path(__file__).parent.parent / "results" / "logs_graph"
	evolution_dir = results_dir / "evolution"
	scores_dir = results_dir / "scores"
	
	evolution_dir.mkdir(parents=True, exist_ok=True)
	scores_dir.mkdir(parents=True, exist_ok=True)
	
	if not input_file.exists():
		raise FileNotFoundError(f"Fichier {input_file} introuvable")
	
	print(f"\n{'='*80}")
	print(f"TRAITEMENT: {nom}")
	print(f"{'='*80}\n")
	
	# Créer l'objet incrémental
	incr = IncrementalClosenessArticle()
	
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
			incr.add_node(node)
		
		elif cmd == "removeNode":
			node = to_int(parts[1])
			incr.remove_node(node)
		
		elif cmd == "addEdge":
			u, v = to_int(parts[1]), to_int(parts[2])
			incr.add_undirected_edge(u, v)
		
		elif cmd == "removeEdge":
			u, v = to_int(parts[1]), to_int(parts[2])
			incr.remove_undirected_edge(u, v)
		
		step_time = time.time() - start_time
		time_per_step.append(step_time)
		cumulative_time += step_time
		
		# Obtenir la closeness actuelle
		closeness = incr.get_all_closeness()
		
		# Sauvegarder l'état du graphe dans evolution/
		graph_file = evolution_dir / f"{base_name}_{i}.txt"
		
		# Créer un DynamicGraph pour l'export
		export_graph = DynamicGraph()
		for node in incr.G.nodes():
			export_graph.add_node(node)
		# Ajouter les arêtes (DiGraph -> Graph)
		edges_added = set()
		for u, v in incr.G.edges():
			edge = tuple(sorted((u, v)))
			if edge not in edges_added:
				edges_added.add(edge)
				export_graph.add_edge(u, v)
		
		write_graph_state(export_graph, graph_file)
		
		# Sauvegarder les scores dans scores/
		score_file = scores_dir / f"{base_name}_score_{i}.txt"
		write_closeness_scores(closeness, score_file)
		
		# Afficher la progression tous les 10%
		if i % max(1, total_steps // 10) == 0 or i == total_steps:
			progress = (i / total_steps) * 100
			print(f"  Étape {i}/{total_steps} ({progress:.0f}%) - "
			      f"Nœuds: {len(incr.G.nodes())}, "
			      f"Arêtes: {incr.G.number_of_edges()//2}, "
			      f"Temps cumulé: {cumulative_time:.3f}s")
	
	final_nodes = len(incr.G.nodes())
	final_edges = incr.G.number_of_edges() // 2
	
	print(f"\n{'='*80}")
	print(f"✓ Traitement terminé")
	print(f"  - Étapes totales: {total_steps}")
	print(f"  - Nœuds finaux: {final_nodes}")
	print(f"  - Arêtes finales: {final_edges}")
	print(f"  - Temps total: {cumulative_time:.3f}s")
	print(f"  - Temps moyen par étape: {cumulative_time/total_steps*1000:.2f}ms")
	print(f"{'='*80}\n")
	
	return {
		'total_steps': total_steps,
		'final_nodes': final_nodes,
		'final_edges': final_edges,
		'time_per_step': time_per_step,
		'cumulative_time': cumulative_time
	}


def main():
	"""Fonction de test."""
	import json
	
	# Traiter les graphes générés
	data_dir = Path(__file__).parent.parent / "data"
	results_dir = Path(__file__).parent.parent / "results" / "logs_graph"
	
	# Traiter les 10 graphes générés avec noms descriptifs
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
	
	results = {}
	for filename in test_files:
		filepath = data_dir / filename
		if filepath.exists():
			try:
				stats = incremental_closeness_file(filename)
				base_name = filename.replace('.txt', '')
				results[base_name] = stats
			except Exception as e:
				print(f"Erreur lors du traitement de {filename}: {e}\n")
	
	# Sauvegarder les temps dans un fichier JSON
	output_file = results_dir / "incremental_times.json"
	with open(output_file, 'w', encoding='utf-8') as f:
		json.dump(results, f, indent=2)
	
	# Afficher le résumé
	print("\n" + "="*80)
	print("RÉSUMÉ DES TRAITEMENTS")
	print("="*80)
	for filename, stats in results.items():
		print(f"\n{filename}:")
		print(f"  Étapes: {stats['total_steps']}")
		print(f"  Temps total: {stats['cumulative_time']:.3f}s")
		print(f"  Temps moyen/étape: {stats['cumulative_time']/stats['total_steps']*1000:.2f}ms")
	
	print(f"\n✓ Temps sauvegardés dans: {output_file}")


if __name__ == "__main__":
	main()
