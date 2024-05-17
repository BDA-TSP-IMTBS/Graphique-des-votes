# Dépouillage des votes

<span>
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</span>


Ceci est un code qui permet de mettre en forme les résultats de votes récupérés suite à un vote utilisant Bélénios. <br />
Le vote se fait par la méthode du vote majoritaire, et le départage des égalité se fait par la méthode récursive de retrait du vote médian : <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://fr.wikipedia.org/wiki/Jugement_majoritaire#Méthode_récursive_de_retrait_du_vote_médian


## Installation

Clonez le git, lancez le programme :+1:

## Explications

### Le format des votes

Une fois récupérez sur Bélénios, les votes sont récupérés sous cette forme :
```
[[[note * nombre de candidat] * nombre de votes] * nombre de questions]
```
Vous pouvez trouvez un exemple avec le fichier [result.json](./result.json)

## Utiliser l'application

A la fin de la page de dépouillage des votes de Bélénios, vous trouvez un bouton `raw results` qui permet de télécharger le fichier des résultats ([result.json](./result.json)) et il vous faudra le mettre dans le dossier racine à côté du programme.

Pour paramètrer la liste des rôles et des candidats, cela se passe dans le fichier [config.json](./config.json)
``` json
{
    "notes_label": ["Extrêmement Favorable", "Très Favorable", "Favorable", "Neutre", "Défavorable", "Très Défavorable", "Extrêmement Défavorable"],
    "roles": [
        { "nom": "Présidence", "candidats": ["Answer1", "Answer2", "Answer3"] },
        { "nom": "Vice-Présidence", "candidats": ["Answer1", "Answer2", "Answer3"] },
        { "nom": "Trésorerie", "candidats": ["Answer1", "Answer2", "Answer3", "Answer4"] },
        { "nom": "Vice-Trésorerie", "candidats": ["Answer1", "Answer2", "Answer3", "Answer4", "Answer5"] },
        { "nom": "Secrétariat", "candidats": ["Answer1", "Answer2"] }
    ]
}
```
- `notes_label` : Liste des labels des notes mises, de la meilleure à la pire;
- `roles` : Liste des postes concernés par l'élection. <b> /!\ L'ordre des postes doit être le même que celui des questions sur Bélénios /!\ </b>
``` json
{ "nom": "Présidence", "candidats": ["Answer1", "Answer2", "Answer3"] },
```
- `nom` : Intitulé du poste;
- `candidats` : Liste des candidats à ce poste. <b> /!\ L'ordre des candidats doit être le même que celui des propositions sur Bélénios /!\ </b>

### Les résultats

Les résultats sont donnés sous trois formes

- Un fichier [resume.txt](./debug/resume.txt) qui est l'équivalent des `print` du terminal;
- Un fichier [debug.txt](./debug//resume.txt) qui est le même  que le fichier précédent, mais avec plus de précision sur certains points (notament la gestion des égalités entre médianes);
- Des [graphiques](./graphs/) crée par le programme donnant les résultats avec les candidats classés et divers autres informations. Résultat avec les données de test :

![Vice-Trésorerie.png](./graphs/Vice-Trésorerie.png "Résultat des votes")