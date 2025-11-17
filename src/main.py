from lecteur_graphe import incremental_closeness_file

if __name__ == "__main__":
    print("=== Lancement complet de l'algorithme incrémental ===")
    incremental_closeness_file("data/test_graph.txt", output_dir="output")
