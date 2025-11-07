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

    g = lire_fichier(fichier)
        # Calculer la closeness
    closeness = compute_all_closeness_classical(g.G)
    g.visualize(closeness)
    print("nombres de noueds :",len(g.get_nodes()))
