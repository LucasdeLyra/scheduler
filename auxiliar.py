import os

"""https://panda.ime.usp.br/panda/static/pythonds_pt/05-OrdenacaoBusca/OQuickSort.html"""
def le_quantum(pasta):
    with open(rf"{pasta}/quantum.txt") as f:
        return int(f.readline().strip())

def le_prioridades(pasta):
    prioridades = []
    with open(rf"{pasta}/prioridades.txt") as f:
        for linha in f.readlines():
            prioridades.append(int(linha.strip()))
    return prioridades

def le_processos(diretorio_programas):
    log = []
    nomes = [ ]
    processos = []

    arquivos = os.listdir(diretorio_programas)
    arquivos.remove('prioridades.txt')
    arquivos.remove('quantum.txt')
    
    prioridades = le_prioridades(diretorio_programas)
    arquivos_com_prioridade = [[prioridade,arquivo] for prioridade, arquivo in zip(prioridades,arquivos)]
    
    arquivos_ordenados_por_prioridade = list(sorted(arquivos_com_prioridade, key=lambda x: -x[0]))
    
    

    for arquivo in arquivos_ordenados_por_prioridade:
        arquivo = arquivo[1]
        with open(rf"{diretorio_programas}/{arquivo}") as f:
            instrucoes = []
            for i, info in enumerate(f):
                if i != 0:
                    instrucoes.append(info.strip())
                else:
                    nome = info.strip()
                    nomes.append(nome)
                    log.append(f"Carregando {nome}")
            processos.append(instrucoes)
    return nomes, processos, log



#O QuickSort não foi feito por mim.
#FONTE: https://panda.ime.usp.br/panda/static/pythonds_pt/05-OrdenacaoBusca/OQuickSort.html
def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)
    return alist[::-1]

def quickSortHelper(alist,first,last):
    if first<last:
        splitpoint = partition(alist,first,last)

        quickSortHelper(alist,first,splitpoint-1)
        quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
    pivotvalue = alist[first].creditos

    leftmark = first+1
    rightmark = last

    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark].creditos <= pivotvalue:
            leftmark = leftmark + 1

        while alist[rightmark].creditos >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark -1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp

    return rightmark