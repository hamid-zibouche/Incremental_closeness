import os
import random
from pathlib import Path
import networkx as nx

from closeness import compute_all_closeness_classical, save_closeness_to_file


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


def main():
	base, data = project_paths()

	# 1) Générer un graphe de base type réseau social
	G = generate_social_graph(n_nodes=4000, m=1, seed=2)

	# 2) Générer le script d'actions compatible avec lecteur_graphe
	actions = generate_dynamic_actions_reserved(G, steps=500, seed=7)

	# 3) Écrire dans data/test_graph.txt (fichier attendu par lecteur_graphe)
	actions_path = data / "test_graph.txt"
	write_actions(actions, actions_path)
	print(f"Fichier d'actions généré: {actions_path}")


if __name__ == "__main__":
	main()

