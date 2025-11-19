import os
import random
from pathlib import Path
import networkx as nx

from classical_closeness import compute_all_closeness_classical, save_closeness_to_file


def project_paths():
	"""Retourne les chemins utiles (base, data)."""
	base = Path(__file__).resolve().parents[1]  # dossier Incremental_closeness
	data = base / "data"
	data.mkdir(parents=True, exist_ok=True)
	return base, data


def write_actions(lines: list[str], filepath: Path):
	"""Écrit un fichier d'actions ligne par ligne (addNode/addEdge/removeEdge/removeNode)."""
	filepath.parent.mkdir(parents=True, exist_ok=True)
	with open(filepath, "w", encoding="utf-8") as f:
		for line in lines:
			f.write(line.rstrip() + "\n")


def generate_social_graph(n_nodes: int = 1000, m: int = 3, seed: int | None = 42) -> nx.Graph:
	"""Génère un graphe de type réseau social (scale-free) via Barabási–Albert.

	Args:
		n_nodes: nombre de nœuds
		m: nombre d'arêtes ajoutées par nouveau nœud (>=1 et < n_nodes)
		seed: graine aléatoire
	"""
	if m < 1 or m >= n_nodes:
		raise ValueError("m doit être >= 1 et < n_nodes")
	return nx.barabasi_albert_graph(n=n_nodes, m=m, seed=seed)


def generate_dynamic_actions_reserved(G: nx.Graph, steps: int = 200, seed: int | None = 123) -> list[str]:
	"""Génère une suite d'actions avec les mots réservés attendus par lecteur_graphe:
	- addNode <id>
	- addEdge <u> <v>
	- removeEdge <u> <v>
	- removeNode <id>

	On commence par ajouter tous les nœuds et arêtes de G, puis on génère des
	opérations dynamiques aléatoires.
	"""
	rnd = random.Random(seed)

	nodes = set(G.nodes())
	edges = set(map(lambda e: tuple(sorted(e)), G.edges()))
	next_id = (max(nodes) + 1) if nodes else 0

	# Étape 1: script initial pour reconstruire G
	actions: list[str] = []
	# Utiliser des identifiants de type n0, n1 si les nœuds sont entiers
	def nid(x):
		return f"n{x}" if isinstance(x, int) else str(x)

	for n in sorted(nodes, key=lambda x: (isinstance(x, str), x)):
		actions.append(f"addNode {nid(n)}")
	for (u, v) in sorted(edges):
		actions.append(f"addEdge {nid(u)} {nid(v)}")

	# Créer des tables de correspondance entre ids internes et tags texte
	# Si G avait des entiers, on passe en n0, n1, ... pour le reste des actions
	int_mode = all(isinstance(n, int) for n in nodes) or len(nodes) == 0
	def to_tag(x):
		return nid(x) if int_mode else str(x)

	for _ in range(steps):
		# Probabilités grossières
		p = rnd.random()
		if p < 0.35:  # ajout arête
			if len(nodes) >= 2:
				u, v = rnd.sample(list(nodes), 2)
				if u != v:
					e = tuple(sorted((u, v)))
					if e not in edges:
						edges.add(e)
						actions.append(f"addEdge {to_tag(u)} {to_tag(v)}")
						continue
		elif p < 0.55:  # ajout nœud
			new_id = next_id
			next_id += 1
			nodes.add(new_id)
			actions.append(f"addNode {to_tag(new_id)}")
			# Connecter le nouveau nœud à un existant pour rester connexe-ish
			if len(nodes) > 1:
				u = rnd.choice(list(nodes - {new_id}))
				e = tuple(sorted((u, new_id)))
				edges.add(e)
				actions.append(f"addEdge {to_tag(u)} {to_tag(new_id)}")
			continue
		elif p < 0.75:  # supprime arête
			if edges:
				u, v = rnd.choice(list(edges))
				edges.remove((u, v))
				actions.append(f"removeEdge {to_tag(u)} {to_tag(v)}")
				continue
		else:  # supprime nœud
			removable = [n for n in nodes]
			if removable:
				x = rnd.choice(removable)
				# supprimer toutes ses arêtes d'abord
				incident = [e for e in edges if x in e]
				for e in incident:
					edges.remove(e)
					actions.append(f"removeEdge {to_tag(e[0])} {to_tag(e[1])}")
				nodes.remove(x)
				actions.append(f"removeNode {to_tag(x)}")
				continue

		# Si l'action choisie n'a pas pu être appliquée, retenter un ajout d'arête si possible
		if len(nodes) >= 2:
			u, v = rnd.sample(list(nodes), 2)
			if u != v:
				e = tuple(sorted((u, v)))
				if e not in edges:
					edges.add(e)
					actions.append(f"addEdge {to_tag(u)} {to_tag(v)}")

	return actions


def generate_dynamic_graph_with_probabilities(
	nom: str,
	etapes: int,
	p1: float,
	p2: float,
	p3: float,
	p4: float,
	seed: int | None = None
) -> Path:
	"""
	À chaque itération, on choisit si on ajoute un nœud, supprime un nœud, 
	ajoute une arête ou supprime une arête selon les probabilités p1, p2, p3 et p4.
	Si à un moment on ne peut pas effectuer l'opération, on recommence cette itération.
	Le fichier nom contient exactement 'etapes' lignes.
	
	Args:
		nom: Nom du fichier de sortie (sera stocké dans data/)
		etapes: Nombre d'étapes de construction du graphe
		p1: Probabilité d'insérer un nœud
		p2: Probabilité de supprimer un nœud
		p3: Probabilité d'insertion d'une arête
		p4: Probabilité de suppression d'une arête
		seed: Graine aléatoire
	
	Returns:
		Path: Chemin vers le fichier généré
	
	Raises:
		ValueError: Si p1 + p2 + p3 + p4 != 1
	"""
	# Vérifier que les probabilités somment à 1
	if abs(p1 + p2 + p3 + p4 - 1.0) > 1e-6:
		raise ValueError(f"Les probabilités doivent sommer à 1. Somme actuelle: {p1 + p2 + p3 + p4}")
	
	_, data_dir = project_paths()
	output_path = data_dir / nom
	
	rnd = random.Random(seed)
	
	nodes = set()
	edges = set()
	next_id = 0
	
	actions = []
	
	# Fonction pour formater les IDs
	def nid(x):
		return f"n{x}"
	
	# Générer exactement 'etapes' lignes
	i = 0
	while i < etapes:
		# Choisir une action selon les probabilités
		p = rnd.random()
		action_done = False
		
		if p < p1:  # Ajouter un nœud
			new_id = next_id
			next_id += 1
			nodes.add(new_id)
			actions.append(f"addNode {nid(new_id)}")
			action_done = True
		
		elif p < p1 + p2:  # Supprimer un nœud
			if len(nodes) > 0:
				x = rnd.choice(list(nodes))
				nodes.remove(x)
				# Supprimer toutes ses arêtes incidentes
				edges = {e for e in edges if x not in e}
				actions.append(f"removeNode {nid(x)}")
				action_done = True
			# Sinon on recommence cette itération (action_done reste False)
		
		elif p < p1 + p2 + p3:  # Ajouter une arête
			if len(nodes) >= 2:
				# Chercher deux nœuds différents
				u, v = rnd.sample(list(nodes), 2)
				e = tuple(sorted((u, v)))
				if e not in edges:
					edges.add(e)
					actions.append(f"addEdge {nid(u)} {nid(v)}")
					action_done = True
			# Sinon on recommence cette itération
		
		else:  # Supprimer une arête
			if len(edges) > 0:
				e = rnd.choice(list(edges))
				edges.remove(e)
				u, v = e
				actions.append(f"removeEdge {nid(u)} {nid(v)}")
				action_done = True
			# Sinon on recommence cette itération
		
		# Incrémenter seulement si l'action a été effectuée
		if action_done:
			i += 1
	
	# Écrire dans le fichier
	write_actions(actions, output_path)
	print(f"Graphe dynamique généré: {output_path}")
	print(f"  - Lignes: {len(actions)} (doit être {etapes})")
	print(f"  - Nœuds finaux: {len(nodes)}")
	print(f"  - Arêtes finales: {len(edges)}")
	
	return output_path


def generate_barabasi_albert_actions(num_nodes: int = 100, m: int = 3, 
                                      num_actions: int = 200, seed: int | None = None) -> tuple[list[str], int, int]:
	"""
	Génère un graphe Barabási-Albert et une séquence d'actions dynamiques.
	(Fonction conservée pour compatibilité avec le benchmark existant)
	
	Args:
		num_nodes: Nombre de nœuds initiaux
		m: Nombre d'arêtes ajoutées par nouveau nœud (>=1 et < num_nodes)
		num_actions: Nombre d'actions dynamiques à générer
		seed: Graine aléatoire
	
	Returns:
		(actions, num_nodes_final, num_edges_final): Liste d'actions, nombre final de nœuds et arêtes
	"""
	# Générer le graphe initial
	G = generate_social_graph(n_nodes=num_nodes, m=m, seed=seed)
	
	# Générer les actions dynamiques
	actions = generate_dynamic_actions_reserved(G, steps=num_actions, seed=seed)
	
	# Compter les nœuds et arêtes finaux
	nodes = set()
	edges = set()
	
	for action in actions:
		parts = action.split()
		cmd = parts[0]
		
		if cmd == "addNode":
			nodes.add(parts[1])
		elif cmd == "addEdge":
			u, v = parts[1], parts[2]
			if u in nodes and v in nodes:
				edges.add(tuple(sorted((u, v))))
		elif cmd == "removeEdge":
			u, v = parts[1], parts[2]
			e = tuple(sorted((u, v)))
			if e in edges:
				edges.remove(e)
		elif cmd == "removeNode":
			n = parts[1]
			if n in nodes:
				nodes.remove(n)
				# Supprimer les arêtes incidentes
				edges = {e for e in edges if n not in e}
	
	return actions, len(nodes), len(edges)


def main():
	"""Fonction principale pour générer 10 graphes dynamiques avec des paramètres différents."""
	print("\n" + "="*80)
	print("GÉNÉRATION DE 10 GRAPHES DYNAMIQUES - Noms descriptifs")
	print("="*80 + "\n")

	# Configuration des 10 graphes avec des paramètres variés
	# Format: (nom, étapes, p1, p2, p3, p4, seed)
	configurations = [
		# Graphe équilibré
		("graphe_equilibre.txt", 1500, 0.25, 0.15, 0.40, 0.20, 42),
		
		# Forte croissance (beaucoup d'ajouts)
		("graphe_forte_croissance.txt", 1700, 0.35, 0.05, 0.50, 0.10, 123),
		
		# Très dynamique (ajouts/suppressions équilibrés)
		("graphe_tres_dynamique.txt", 2000, 0.20, 0.20, 0.30, 0.30, 456),
		
		# Focus sur les nœuds (beaucoup d'ajouts/suppressions de nœuds)
		("graphe_focus_noeuds.txt", 1600, 0.30, 0.25, 0.25, 0.20, 789),
		
		# Focus sur les arêtes (beaucoup d'ajouts/suppressions d'arêtes)
		("graphe_focus_aretes.txt", 2500, 0.15, 0.10, 0.45, 0.30, 101),
		
		# Croissance lente et stable
		("graphe_croissance_stable.txt", 2300, 0.30, 0.10, 0.45, 0.15, 202),
		
		# Décroissance (plus de suppressions que d'ajouts)
		("graphe_decroissance.txt", 1900, 0.15, 0.30, 0.20, 0.35, 303),
		
		# Petit graphe dense
		("graphe_petit_dense.txt", 1100, 0.20, 0.10, 0.50, 0.20, 404),
		
		# Grand graphe sparse
		("graphe_grand_sparse.txt", 3000, 0.35, 0.15, 0.35, 0.15, 505),
		
		# Très chaotique (changements constants)
		("graphe_chaotique.txt", 2200, 0.25, 0.25, 0.25, 0.25, 606),
	]
	
	# Générer tous les graphes
	for i, (nom, etapes, p1, p2, p3, p4, seed) in enumerate(configurations, 1):
		print(f"\n{i}. Génération de {nom}...")
		print(f"   Étapes: {etapes}, p_add_node={p1:.2f}, p_del_node={p2:.2f}, "
		      f"p_add_edge={p3:.2f}, p_del_edge={p4:.2f}")
		
		generate_dynamic_graph_with_probabilities(
			nom=nom,
			etapes=etapes,
			p1=p1,
			p2=p2,
			p3=p3,
			p4=p4,
			seed=seed
		)
	
	_, data_dir = project_paths()
	print("\n" + "="*80)
	print(f"✓ Génération terminée - 10 graphes générés dans: {data_dir}")
	print("="*80 + "\n")


if __name__ == "__main__":
	main()

