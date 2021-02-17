import numpy as np
import time
import gauss

"""
fonction prenant en paramètre un nom de fichier 'file_name' et retournant la représentation
d'un ensemble de pages web codée dans le fichier :
- 'key_words' représente le tableau des mots-clés contenus dans les pages
- 'm_adj' représente la matrice d'adjacence du graphe formé par les liens entre les pages
"""
def get_matrix_from_file(file_name) :
    file = open(file_name,'r')
    lines = file.readlines()
    n = int(lines[0])
    key_words=[]
    m_adj=np.zeros((n,n))
    for i in range(1,n+1) :
        kws = lines[i].split()
        key_words.append(kws)
    for i in range(n+1,2*n+1) :
        l = lines[i].split()
        for j in range(1,len(l)) :
            m_adj[int(l[0]),int(l[j])] = 1
    return key_words,m_adj

"""
fonction prenant en paramètre un graphe représenté par la liste des mots clés contenus dans les pages 'k_words'
et la matrice d'adjacence 'm_adj'
"""
def affiche_graphe(k_words,m_adj) :
    for i in range(len(k_words)) :
        print("mots-clés de la page",i," :",k_words[i])
    print("matrice d'adjacence :")
    print(m_adj)

"""
fonction prenant en paramètre un tableau de liste de mots clés contenus dans les pages web 'key_words'
et une liste de mots clés recherchés 'key_words_searched'
et retournant la liste des indices des pages contenant au moins un des mots cherchés.
"""
def select_pages(key_words,key_words_searched) :
    pages=[]
    for i in range(0, len(key_words_searched)):
        for j in range(0, len(key_words)):
            if key_words_searched[i] in key_words[j]:
                if j in pages:
                    pass
                else:
                    pages.append(j)
    pages.sort()
    return pages

"""
fonction prenant en paramètre une matrice d'adjacence 'm_adj' et une liste d'indices de pages sélectionnées 'pages'
et retournant la sous-matrice d'adjacence correspondant aux liens entre les pages sélectionnées.
"""
def select_matrix(m_adj,pages) :
    taille_pages=len(pages)
    mx=np.zeros([taille_pages,taille_pages])
    for i in range(0, taille_pages):
        for j in range(0, taille_pages):
            mx[i,j]=m_adj[pages[i],pages[j]];
    return mx

"""
fonction prenant en paramètre une matrice d'adjacence 'm_adj'
et retournant la matrice de transition correspondante
"""
def get_transition_matrix(m_adj) :
    taille_m=len(m_adj)
    mxt=np.zeros([taille_m,taille_m])
    for i in range(0, taille_m):
        sum = np.sum(m_adj[i])
        for j in range(0, taille_m):
            if sum!=0:
                mxt[i,j]=0.8*(m_adj[i,j]/sum)+0.2/taille_m
            else:
                mxt[i,j]=1/taille_m
    return mxt

"""
fonction prenant en paramètre une matrice de transition 'm_transi' et calculant un vecteur de score r vérifiant r*mat=r
selon la méthode du premier algorithme.
"""

def page_rank1(m_transi) :
    taille_p=len(m_transi)
    m_n=m_transi-np.identity(taille_p)
    m_n=np.transpose(m_n)
    ligne_a_ajouter=np.ones((1,taille_p))
    y=np.zeros((taille_p,1))
    m_n=np.concatenate((m_n,ligne_a_ajouter))
    y=np.concatenate((y,np.array([[1]])))
    m_n,y=gauss.Gauss(m_n,y)
    res=gauss.solveTriSup(m_n,y)
    return res
#
"""
fonction prenant en paramètre une matrice de transition 'm_transi' ainsi qu'un seuil 'eps' et calculant un vecteur de score
r vérifiant r*mat=r selon la méthode du second algorithme.
"""
def page_rank2(m_transi,eps) :
    n=len(m_transi)
    r0=np.zeros(n)
    for x in range(0, n):
        r0[x]=1/n
    r1=np.dot(r0,m_transi)
    while max(abs(r1-r0))>eps:
        r0=r1
        r1=np.dot(r0,m_transi)
    return r1

"""
fonction prenant en paramètre une liste 'pages' d'indices de pages sélectionnées et un vecteur 'rank' contenant leur score
correspondant et retournant la liste des indices des pages triées dans par ordre décroissant de score.
"""
def sort_pages(pages,rank) :
    if len(pages) == len(rank) !=0 :
        ind = rank.argsort()
        res = []
        for i in ind[::-1] :
            res.append(pages[i])
        return res
    else :
        return []

key_w,m_adj = get_matrix_from_file("example-graph2.txt")
# key_w,m_adj = get_matrix_from_file("example-graph2.txt")
# key_w,m_adj = get_matrix_from_file("example-graph3.txt")
# key_w,m_adj = get_matrix_from_file("example-graph4.txt")
affiche_graphe(key_w,m_adj)

print("\n\nRecherche de 'a' ou 'b' :\n----------------------")
pages = select_pages(key_w,['a','b'])
print("  pages sélectionnées : ",pages)
s_m_adj = select_matrix(m_adj,pages)
print("  matrice sélectionnée : \n",s_m_adj)
m_transi = get_transition_matrix(s_m_adj)
print("  matrice de transition : \n",m_transi)
#Cetst normal que ca te mette faux car la méthode 2 est bcp moins precise que la & dcp qquand ya trop de page
print("\n>>>>>>>>>> Méthode 1 <<<<<<<<<<<")
start_time = time.time()
r = page_rank1(m_transi)
print("  rank1 trouvé : ",r)
pages_triees_1 = sort_pages(pages,r)
print("  pages indexées 1: ",pages_triees_1)
print("  --- en %s seconds ---" % (time.time() - start_time))

print("\n>>>>>>>>>> Méthode 2 <<<<<<<<<<<")

start_time = time.time()

r2 = page_rank2(m_transi,10**(-5))
print("  rank2 trouvé : ",r2)
pages_triees_2 = sort_pages(pages,r2)
print("  pages indexées 2: ",pages_triees_2)
print("  --- en %s seconds ---" % (time.time() - start_time))

print("pages indexées identiques par les méthodes ? : ",pages_triees_1==pages_triees_2)
