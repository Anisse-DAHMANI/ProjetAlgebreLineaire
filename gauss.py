import numpy as np

"""
fonction auxiliaire de 'affichage'
"""
def get_number_rep(x) :
    if x == int(x) :
        return str(int(x))
    else :
        return "%.2f" % x
"""
fonction auxiliaire de 'affichage'
"""
def get_str_rep(x,max_size,i,first,print0) :
    str_x = get_number_rep(abs(x))
    n = len(str_x)
    if x == -1. :
        if i == first :
            return " "*(max_size)+"-x_"+str(i+1)
        else :
            return "-"+" "*(max_size)+"x_"+str(i+1)
    elif x == 1. :
        if i == first :
            return " "*(1+max_size)+"x_"+str(i+1)
        else :
            return "+"+" "*(max_size)+"x_"+str(i+1)
    elif x == 0.:
        if print0 :
            return " "*(max_size+3)+"0"
        else :
            return " "*(max_size+1+3)
    elif x < 0 :
        if i == first :
            return " "*(max_size-n)+"-"+str_x+"x_"+str(i+1)
        else :
            return "-"+" "*(max_size-n)+str_x+"x_"+str(i+1)
    elif i == first :
        return " "*(1+max_size-n)+str_x+"x_"+str(i+1)
    else :
        return "+"+" "*(max_size-n)+str_x+"x_"+str(i+1)

"""
fonction permettant l'affichage des systèmes linéaires
"""
def affichage(A,y) :
    res = ""
    max_size = 0
    first = [-1]*len(A)
    for i in range(len(A)) :
        for j in range(len(A[i])) :
            max_size = max(max_size,len(get_number_rep(A[i][j])))
            if first[i] ==-1 and A[i][j] != 0 :
                first[i] = j
    for i in range(len(A)) :
        res+="|"
        for j in range(len(A[i])) :
            res+=get_str_rep(A[i][j],max_size,j,first[i],first[i]==-1 and
j ==
len(A[i])-1)
        res=res+" = "+(get_number_rep(y[i]))+"\n"
    print(res)

"""
fonction retournant le système représenté par A et y dans lequel les
lignes i et
k ont été permutées.
"""
def permutation(A,y,i,k) :
    line_i = A[i].copy()
    y_i = y[i]
    A[i] = A[k]
    A[k] = line_i

    y[i] = y[k]
    y[k] = y_i
    return A,y

"""
fonction retournant le système représenté par A et y dans lequel la
variable n°j
a été supprimée des lignes
n°i+1 à n en utilisant la ligne n°i
"""
def elimination(A,y,i,j) :
    for k in range(i+1,len(A)) :
        y[k] = y[k]-A[k,j]*y[i]/A[i,j]
        A[k] = A[k]-A[k,j]*A[i]/A[i,j]
    return A,y

def next_pivot(A,i,j) :
    n,p = A.shape
    k = i
    l = j
    while l<p and np.isclose(A[k,l],0) :
        if k < n-1 :
            k+=1
        else :
            k=i
            l+=1
    return k,l

def Gauss(A,y) :
    n,p = A.shape
    i=0
    j=0
    while i < n and j < p :
        k,j = next_pivot(A,i,j)
        if j < p :
            if k != i :
                permutation(A,y,i,k)
            A,y = elimination(A,y,i,j)
            i = i+1
            j = j+1
    return A,y

def first_non_zero(L) :
    for i in range(len(L)) :
        if not np.isclose(L[i], 0) :
            return i
    return -1

def solveTriSup(A,y):
    (n,p) = A.shape
    nb_eq = n
    res = np.zeros(p)
    for i in range(n-1,-1,-1) :
        k = first_non_zero(A[i])
        if(k != -1) :
            t = y[i]
            for l in range(k+1,p) :
                t = t-A[i,l]*res[l]
            res[k] = t/A[i,k]
        else :
            if not np.isclose(y[i],0) :
                print("Pas de solution")
            else :
                nb_eq = nb_eq-1
    if nb_eq < p :
        print("Infinité de solutions")
    else :
        print("Unique solution")
    return res
