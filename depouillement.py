import json
import matplotlib.pyplot as plt
import numpy as np
import os
from math import *
from copy import deepcopy

## ======================================== Variables ========================================
roles = ["Présidence", "Vice-Présidence", "Trésorerie", "Vice-Trésorerie", "Secrétariat"]
candidatss = [ # La liste des candidats aux différents rôles
    ["Answer 1", "Answer 2", "Answer 3"],
    ["Answer 1", "Answer 2", "Answer 3"],
    ["Answer 1", "Answer 2", "Answer 3", "Answer 4"],
    ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"],
    ["Answer 1", "Answer 2"]
]
notes_label = ["Extrêmement Favorable", "Très Favorable", "Favorable", "Neutre", "Défavorable", "Très Défavorable", "Extrêmement Défavorable"]

''' /!\ ATTENTION /!\ 
La liste des rôles doit être la même que celle des questions posées sur Bélénios.
De même pour les candidats, qui doit être dans le même ordre que celle de Bélénios.
'''

## ======================================== Functions ========================================
## Process data
def extractData(data: list[list[int]]) -> list[list[int]]:
    ''' Cette fonction sert à extraire les données obtenues en json depuis Bélénios
    
    Input :     data -> Résultats de la question dont on veut extraire les données.

    Output :    resultats -> Liste du dépouillage de l'élection;
                nb_vote (int) -> Nombre de votes valides;
                nb_blanc (int) -> Nombre de votes blancs.'''
    global notes_label

    # Initialisation des résultats
    resultats = [[0 for candidat in data[0]] for note in notes_label]
    nb_vote = 0
    nb_blanc = 0

    for vote in data:
        for candidat in range(len(vote)):
            # vote[candidat] représente la note associé au candidat
            if vote[candidat] == 0: # Si la note est 0 c'est que le vote est blanc
                nb_blanc += 1
                break # Les notes de tou·te·s les autres candidat·e·s sont aussi 0
            
            else:
                nb_vote += 1
                resultats[vote[candidat] - 1][candidat] += 1 # -1 car les résultats de Bélénios commencent à 1

    # Fermer le fichier
    f.close()

    return resultats, nb_vote//len(resultats[0]), nb_blanc

def checkData(resultats: list[list[int]]):
    ''' Cette fonction sert à checker si les données obtenues sont cohérentes entre elles
    
    Input : resultats -> liste du dépouillage de l'élection.'''
    # Vérifie que tous les candidats ont bien le même nombre de votes
    nb_votant = [0 for i in resultats[0]]

    for note in resultats:
        for candidat in range(len(note)):
            nb_votant[candidat] += note[candidat]
    
    if [nb_votant[0] for i in resultats[0]] != nb_votant:
        raise ValueError("Tous les candidats n'ont pas le même nombre de votes")

def calculateMedianes(nb_vote: int, resultats: list[list[int]]) -> list[int]:
    ''' Cette fonction sert à calculer les médianes des candidats
    
    Input :     nb_vote -> Nombre de votes valides;
                resultats -> Liste du dépouillage de l'élection.
    
    Output :    medianes -> Liste des médianes des candidats.'''
    medianes = [0 for i in resultats[0]]

    # On cherche la note médiane de chaque candidat
    for candidat in range(len(medianes)):
        medianes[candidat] = calculateMediane(nb_vote, candidat, resultats)        
    
    return medianes

def calculateMediane(nb_vote: int, candidat: int, resultats: list[list[int]]) -> int:
    ''' Cette fonction sert à calculer la médiane d'un candidat
    
    Input :     nb_vote -> Nombre de votes valides;
                resultats -> Liste du dépouillage de l'élection.
    
    Output :    medianes -> Liste des médianes des candidats.'''
    somme = 0
    for note in range(len(resultats)):
            somme += resultats[note][candidat]

            if somme > nb_vote//2:
                return note

def sortResults(candidats: list[str], resultats: list[list[int]], medianes: list[int]):
    ''' Cette fonction sert à trier les candidats en fonction de leur médiane.
    
    Input : candidats -> La liste des noms des candidats;
            resultats -> Liste du dépouillage de l'élection;
            medianes -> Liste des médianes des candidats.'''

    for i in range(1, len(medianes)):
        mediane_save = medianes[i]
        candidat_save = candidats[i]
        resultat_save = saveResults(resultats, i)

        j = i
        while j > 0 and medianes[j-1] > mediane_save:
            medianes[j] = medianes[j-1]
            candidats[j] = candidats[j-1]
            swapResults(resultats, j, j-1)
            j -= 1

        medianes[j] = mediane_save
        candidats[j] = candidat_save
        setResults(resultats, j, resultat_save)

def sortEqualities(nb_vote:int, candidats: list[str], resultats: list[list[int]], medianes: list[int]):
    ''' Cette fonction sert à trier les candidats qui sont à égalité sur leur médiane.
    
    Input : nb_vote -> Nombre de votes valides
            candidats -> La liste des noms des candidats;
            resultats -> Liste du dépouillage de l'élection;
            medianes -> Liste des médianes des candidats.'''
    global resume, debug
    
    fullPrint("===== Egalité =====")
    
    # On regarde si il y a des égalités
    i = 0
    while i < len(medianes) - 1:
        if medianes[i] == medianes[i+1]:
            equality = [i]

            while i < len(medianes) - 1 and medianes[i] == medianes[i+1]:
                equality.append(i + 1)
                i += 1

            # Si il y en a, on applique la Méthode récursive de retrait du vote médian
            # https://fr.wikipedia.org/wiki/Jugement_majoritaire#Méthode_récursive_de_retrait_du_vote_médian
            fullPrint(str(equality) + " Médiane : " + str(medianes[equality[0]]))

            subOrder = [0 for i in candidats]
            medianPointWithdraw(nb_vote, deepcopy(equality), medianes[i], deepcopy(resultats), 1, subOrder)

            fullPrint("sub-order avant tri : " + str(subOrder)) # Ce qui est en 0 dans le subOrder ne doit pas bouger

            for j in range(equality[0], equality[-1] + 1):
                subOrder_save = subOrder[j]
                mediane_save = medianes[j]
                candidat_save = candidats[j]
                resultat_save = saveResults(resultats, j)

                k = j
                while k > equality[0] and subOrder[k-1] > subOrder_save:
                    subOrder[k] = subOrder[k-1]
                    medianes[k] = medianes[k-1]
                    candidats[k] = candidats[k-1]
                    swapResults(resultats, k, k-1)
                    k -= 1

                subOrder[k] = subOrder_save
                medianes[k] = mediane_save
                candidats[k] = candidat_save
                setResults(resultats, k, resultat_save)
            
            fullPrint("sub-order après tri : " + str(subOrder) + "\n")
        
        else:
            i += 1

def medianPointWithdraw(nb_vote: int, equality: list[int], mediane: int, resultats_modif: list[list[int]], rank: int, subOrder: list[int]):
    ''' Cette fonction sert à mettre en oeuvre la méthode récursive de retrait du vote médian
    
    Input : nb_vote -> Nombre de votes valides;
            equality -> Liste des candidats à égalité;
            mediane -> Médiane de ces candidats;
            resultats_modif -> Copie de la liste du dépouillage de l'élection;
            rank -> Rang dans lequel les élément seront placés. Est modifié dans la fonction;
            subOrder -> Ordre dans lequel doivent être placé au sein de l'égalité. Est modifié dans la fonction.'''
    global debug
    
    # Conditions de fin
    if len(equality) == 0: # Si de longueur nulle --> S'arrếte
        return
    elif len(equality) == 1: # Si est de longueur 1 --> Affecte le rang
        subOrder[equality[0]] = rank
        # print(subOrder)
        return
    
    # On retire l'un des votes de la mention majoritaire et on recalcule la médiane
    nb_vote -= 1
    subMedianes = [mediane for i in equality]
    for i in range(len(equality)):
        candidat = equality[i]
        resultats_modif[mediane][candidat] -= 1
        subMedianes[i] = calculateMediane(nb_vote, candidat, resultats_modif)
    debug.write("       New mediane = " + str(subMedianes) + "\n")
    
    if (subMedianes == [None for i in subMedianes]):
        raise ValueError("Putain vous faîtes chier vous avez les même votes")

    # Si toutes les mentions ont la même valeur on ne peut rien conclure 
    if areValuesEquals(subMedianes):
        # On recommence (avec une nouvelle médiane si toutes les médianes ont changer) 
        medianPointWithdraw(nb_vote, equality, subMedianes[0], resultats_modif, rank, subOrder)

    # Si elle ne sont plus toutes de la même valeur
    else:
        # On trie les valeur et on applique medianPointWithdraw() aux valeur égales dans l'ordre

        for i in range(1, len(subMedianes)):
            subMediane_save = subMedianes[i]
            equality_save = equality[i]

            j = i
            while j > 0 and subMedianes[j-1] > subMediane_save:
                subMedianes[j] = subMedianes[j-1]
                equality[j] = equality[j-1]
                j -= 1

            subMedianes[j] = subMediane_save
            equality[j] = equality_save
        
        i = 0
        while i < len(subMedianes):
            subEquality = [equality[i]]
            while i < len(subMedianes) - 1 and subMedianes[i] == subMedianes[i+1]:
                subEquality.append(equality[i + 1])
                i += 1
            debug.write("Sous égalité :" + str(subEquality) + "\n")
            medianPointWithdraw(nb_vote, subEquality, subMedianes[i], resultats_modif, rank, subOrder)
            rank += len(subEquality)
            i += 1

## Results modification
def saveResults(resultats: list[list[int]], i:int) -> list[int]:
    '''Sauvegarde les résultats d'index i'''
    return [resultats[note_index][i] for note_index in range(len(resultats))]

def swapResults(resultats: list[list[int]], i: int, j:int):
    ''' Transfert les résultats d'index j à l'index i'''
    for note_index in range(len(resultats)):
        resultats[note_index][i] = resultats[note_index][j]

def setResults(resultats: list[list[int]], i: int, save_results: list[int]):
    '''Set les résultats d'index i'''
    for note_index in range(len(resultats)):
        resultats[note_index][i] = save_results[note_index]

## Utilities
def areValuesEquals(liste: list):
    ''' Cette fonction sert savoir si une liste est composée d'une valeur unique
    
    Input :     liste -> Liste à tester
    
    Output:     True si la liste est composée d'une seule valeur, False sinon'''
    i_prec = liste[0]
    for i in liste:
        if i != i_prec:
            return False
    
    return True

def fullPrint(texte: str):
    ''' Cette fonction permet de print et de rajouter les données dans les fichiers resume et debug
    
    Input :     texte -> texte à print'''
    global resume, debug
    
    print(texte)
    resume.write(texte + "\n")
    debug.write(texte + "\n")

## Show graph
def showGraph(role: str, candidats: list[str], resultats: list[list[int]], medianes: list[int], nb_blanc: int, nb_vote: int):
    ''' Cette fonction permet de créer le graphique des résultats
    
    Input : role -> Poste qui correspond aux résultats;
            candidats -> Liste des canditats au poste;
            resultats -> Liste du dépouillage de l'élection;
            medianes -> Médianes de chaque candidat;
            nb_blanc -> Nombre de votes blanc;
            nb_vote -> Nombre de votes valides.'''  
    global notes_label

    largeur_barre = 0.1 # Largeur de chaque barre : attention si valeur trop grande, il n'y aura pas de différence entre chaque paquet de barres

    # Valeurs pour chaque catégories de notes
    extremementFavorable = resultats[0]
    tresFavorable = resultats[1]
    favorable = resultats[2]
    neutre = resultats[3]
    defavorable = resultats[4]
    tresDefavorable = resultats[5]
    extremementDéfavorable = resultats[6]


    x1 = range(len(extremementFavorable))
    x2 = [i + largeur_barre for i in x1]
    x3 = [i + 2*largeur_barre for i in x1]
    x4 = [i + 3*largeur_barre for i in x1]
    x5 = [i + 4*largeur_barre for i in x1]
    x6 = [i + 5*largeur_barre for i in x1]
    x7 = [i + 6*largeur_barre for i in x1]

    plt.figure(num="Résultat des votes : " + role, figsize=(20,10))

    # Tracer les rectangles
    plt.bar(x1, extremementFavorable, width = largeur_barre, color = '#0f7b11', edgecolor = 'black', linewidth = 1)
    plt.bar(x2, tresFavorable, width = largeur_barre, color = '#2eb230', edgecolor = 'black', linewidth = 1)
    plt.bar(x3, favorable, width = largeur_barre, color = '#7dd161', edgecolor = 'black', linewidth = 1)
    plt.bar(x4, neutre, width = largeur_barre, color = '#f5c724', edgecolor = 'black', linewidth = 1)    
    plt.bar(x5, defavorable, width = largeur_barre, color = '#ff9d00', edgecolor = 'black', linewidth = 1)
    plt.bar(x6, tresDefavorable, width = largeur_barre, color = '#ff6505', edgecolor = 'black', linewidth = 1)
    plt.bar(x7, extremementDéfavorable, width = largeur_barre, color = '#b32a00', edgecolor = 'black', linewidth = 1)

    # Ajoute le nombre de vote sur les barres
    for i in range(len(extremementFavorable)):
        plt.text(x1[i], extremementFavorable[i], str(extremementFavorable[i]), ha='center', va='bottom')
        plt.text(x2[i], tresFavorable[i], str(tresFavorable[i]), ha='center', va='bottom')
        plt.text(x3[i], favorable[i], str(favorable[i]), ha='center', va='bottom')
        plt.text(x4[i], neutre[i], str(neutre[i]), ha='center', va='bottom')
        plt.text(x5[i], defavorable[i], str(defavorable[i]), ha='center', va='bottom')
        plt.text(x6[i], tresDefavorable[i], str(tresDefavorable[i]), ha='center', va='bottom')
        plt.text(x7[i], extremementDéfavorable[i], str(extremementDéfavorable[i]), ha='center', va='bottom')


    # Placer les médianes des candidats
    largeur_mediane = largeur_barre/5
    x_med = [i + medianes[i]*largeur_barre for i in x1]
    y_med = [resultats[medianes[i]][i] for i in range(len(x_med))]

    plt.bar(x_med, y_med, width = largeur_mediane, color = 'red', edgecolor = 'black', linewidth = 0.5)
    
    # Placer les labels des candidats
    nb_candidat = len(candidats)
    plt.xticks([r + largeur_barre*2.5 + largeur_barre / nb_candidat for r in range(len(extremementFavorable))], candidats)

    maxResult = max([max(note) for note in resultats])
    plt.ylim(bottom = 0,top = maxResult + 1) # Place le maximum des ordonnées
    plt.title("Résultat des votes : " + role, fontsize=18, fontweight = 'semibold') # Ajoute un titre
    
    plt.figlegend(notes_label, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=3) # Ajoute une légende
    #plt.subplots_adjust(bottom=0.25) # Ajuste la taille du graphique pour ne pas se supperposer à la légende

    # Ajoute les informations des votes blancs/valides
    plt.text(0, maxResult + 0.5, "Votes : " + str(nb_vote) + "\n" + "Votes blancs : " + str(nb_blanc), fontsize=10, ha='left', va='top', fontweight = 'bold')

    graphForlder = 'graphs'
    if not os.path.exists(os.path.join(os.path.dirname(__file__), graphForlder)):
        os.makedirs(os.path.join(os.path.dirname(__file__), graphForlder))
    plt.savefig(os.path.join(os.path.join(os.path.dirname(__file__), graphForlder), role + '.png'), dpi=300, bbox_inches='tight') # Sauvegarde

    #plt.subplots_adjust(bottom=0.125, top=0.95, left=0.05, right=0.95) # Ajuste la taille du graphique pour ne pas se supperposer à la légende
    plt.show()


## ======================================== Main ========================================

## Ouvre le JSON
f = open(os.path.join(os.path.dirname(__file__), 'result.json'))

## Ouvre les fichiers de debug

debugFolder = 'debug'
if not os.path.exists(os.path.join(os.path.dirname(__file__), debugFolder)):
    os.makedirs(os.path.join(os.path.dirname(__file__), debugFolder))

resume = open(os.path.join(os.path.join(os.path.dirname(__file__), debugFolder), 'resume.txt'), "w")
debug = open(os.path.join(os.path.join(os.path.dirname(__file__), debugFolder), 'debug.txt'), "w")

# Renvoie un object JSON en tant que dictionnaire
datas = json.load(f)["result"]

for i in range(0, len(roles)):
    fullPrint("======================================== " + roles[i] + " ========================================\n")        

    # Extraction des données
    resultats, nb_vote, nb_blanc = extractData(datas[i])
    fullPrint("Résultats : " + str(resultats) + "\n"
        + "Nombre de votes valides : " + str(nb_vote) + "; \n"
        + "Nombre de votes blancs : " + str(nb_blanc) + "\n")
    # Vérification de la cohérence des données
    checkData(resultats)

    # Calcul des médianes des candidats
    medianes = calculateMedianes(nb_vote, resultats)
    fullPrint("Candidats : " + str(candidatss[i]) + "\n"
              + "Médianes des candidats : " + str(medianes) + "\n")

    # Trie les candidats en fonction de leur médiane
    sortResults(candidatss[i], resultats, medianes)
    fullPrint("Liste pré-triées : \n" + 
        "   - Candidats : " + str(candidatss[i]) + "\n"
        "   - Médianes : " + str(medianes) + "\n"
        "   - Résultats : " + str(resultats) + "\n")
    
    # Trie les candidats à égalité    
    sortEqualities(nb_vote, candidatss[i], resultats, medianes)
    fullPrint("Liste triées : \n" + 
        "   - Candidats : " + str(candidatss[i]) + "\n"
        "   - Médianes : " + str(medianes) + "\n"
        "   - Résultats : " + str(resultats) + "\n")
    
    # Affiche le graph
    showGraph(roles[i], candidatss[i], resultats, medianes, nb_blanc, nb_vote)

f.close()
resume.close()
debug.close()