import os
from graph import DynamicGraph
from closeness import compute_all_closeness_classical

def lire_fichier(nom_fichier):
    with open(nom_fichier , "r" , encoding="utf-8") as f :
        #initialiser le graph
        g = DynamicGraph()
        for ln,line in enumerate(f) :
            line = line.strip()
            if not line :
                continue
            try :
                args = len(line.split())
                
                if (args ==2 ) :
                    #dans le cas ou c'est soit addNode ou removeNode (2 args)
                    act ,n1 = map(str,line.split())
                    print("act :",act,", n1 :",n1)
                    if (act == "addNode"):
                        g.add_node(n1)
                    elif (act == "removeNode"):
                        g.remove_node(n1)
                    else : 
                        print("Erreur nom d'opreation incorrecte ")
                elif (args == 3):
                    #dans le cas ou c'est soit addEdge ou removeedge (3 args)
                    act ,n1,n2 = map(str,line.split())
                    print("act :",act,", n1 :",n1,"n2 :",n2)
                    if (act == "addEdge"):
                        g.add_edge(n1,n2)
                    elif (act == "removeEdge"):
                        g.remove_edge(n1,n2)
                    else : 
                        print("Erreur nom d'opreation incorrecte ")
                else :
                    print("Erreur de format d'entrée\\ '''par concéquence egnore la ligne")

            except ValueError :
                print ("erreur :")
    return g




if __name__ == "__main__":
    # Obtenir le chemin correct vers le fichier data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    fichier = os.path.join(data_dir, "test_graph.txt")

    print("\n=== Lecture du fichier d'actions ===")
    g = lire_fichier(fichier)
    
    print(f"\n=== Graphe final ===")
    print(f"Nombre de nœuds: {g.number_of_nodes()}")
    print(f"Nombre d'arêtes: {g.number_of_edges()}")
    
    print("\n=== Calcul de la Closeness Centrality ===")
    print("Cela peut prendre quelques secondes pour un grand graphe...")
    closeness = compute_all_closeness_classical(g.G, verbose=True)
    
    print(f"Closeness calculée pour {len(closeness)} nœuds")
    # Afficher les 5 nœuds avec les meilleures closeness
    if closeness:
        sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
        print("\nTop 5 nœuds par closeness centrality:")
        for i, (node, value) in enumerate(sorted_closeness[:5], 1):
            print(f"  {i}. Nœud {node}: {value:.6f}")
    
    # Visualisation interactive (PyVis -> HTML)
    print("\n=== Génération de la visualisation interactive ===")
    try:
        g.visualize_interactive(closeness, output_path="graph_interactive.html")
    except Exception as e:
        print("Visualisation interactive échouée:", e)
