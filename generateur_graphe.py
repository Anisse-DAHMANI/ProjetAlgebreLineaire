import numpy as np
import random

"""
fonction prenant en paramètre un entier 'n', une liste de mots-clés 'key_words',
un intervalle de nombre de voisin '(v_m,v_M)' et un intervalle de nombre de mots-clés '(kw_m,kw_M)'
et qui génère un graphe de 'n' sommets, où les sommets ont entre 'v_m' et 'v_M' voisins et entre
'kw_m' et 'kw_M' mots-clés associés (sous forme de fichier texte)
"""
def generateurGraphe(nom_fichier,n,key_words,v_m,v_M,kw_m,kw_M) :
    l_sommets = range(n)
    m = len(key_words)
    kw_sommets = [[]]*n
    v_sommets = [[]]*n
    data = str(n)+"\n"
    for i in l_sommets :
        nb_kw = random.randint(max(kw_m,1),min(kw_M,m))
        nb_v = random.randint(max(v_m,1),min(v_M,n))
        kw_sommets[i]=random.sample(key_words,nb_kw)
        for kw in kw_sommets[i] :
            data+=kw+" "
        data = data[:-1]+"\n"
        v_sommets[i]=random.sample(l_sommets,nb_v)
    for i in l_sommets :
        data = data+str(i)
        for v in v_sommets[i] :
            data+=" "+str(v)
        data = data+"\n"
    data = data[:-1]
    fichier = open(nom_fichier, "w")
    fichier.write(data)
    fichier.close()

# generateurGraphe("graph-genere2.txt",20,["a","b","c","d","e","f","g"],4,7,3,6)
# generateurGraphe("graph-genere3.txt",100,["a","b","c","d","e","f","g"],20,35,4,7)
# generateurGraphe("graph-genere4.txt",1000,["a","b","c","d","e","f","g"],200,300,4,7)
# generateurGraphe("graph-genere5.txt",2000,["a","b","c","d","e","f","g"],400,600,4,7)
