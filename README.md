[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python 3.7.3](https://img.shields.io/badge/Python-3.7.3-blue)](https://www.python.org/downloads/release/python-373/)
[![Platform tested](https://img.shields.io/badge/Plateform%20tested-Win--32%20%7C%20Win--64%20%7C%20Linux--64-orange)](#)
[![Last commit](https://img.shields.io/github/last-commit/Val-Bch/backup-multi-cloud?label=Last%20Modified)](https://img.shields.io/github/last-commit/Val-Bch/backup-multi-cloud?label=Last%20Modified) 


---------------------

Ce script permet d'assister la création, de faciliter et d'automatiser des plans de sauvegardes vers des Cloud comme Azure Blob Storage, AWS, OVH...
Il est évolutif et permet d'intégrer des SDK Python sous forme de 'packages'. 
Est inclus ici le SDK Python 'Stockage Blob Azure v12' de Microsoft.
<br/>

---------------------
# Table des matières

- [Prérequis](#Prérequis)
- [Fonctionnalités principales](#Fonctionnalités-principales)
  - [Lancement Rapide](#lancement-Rapide)
  - [Lancement Avancé](#lancement-avancé)
    - [Arguments](#arguments)
    - [Automatisation](#automatisation)
  - [Ajouter un SDK](#Ajouter-un-SDK)
- [Log](#les-fichiers-logs)
- [Contribution](#contribution)
- [Licence](#licence)

<br/>

------------------
# Prérequis

- Microsoft ou Linux (Testé sous Debian, Ubuntu et Windows 10)
- Python 3 ou +
- Package Azure : {pip3 install azure-storage-blob} ou {pip install -r requirements.txt}
- Compte Azure avec un abonnement actif. [Créez un compte gratuitement](https://azure.microsoft.com/free/?ref=microsoft.com&utm_source=microsoft.com&utm_medium=docs&utm_campaign=visualstudio).
- Un compte de stockage Azure (Blob pas DataLake). [Créer un compte de stockage](https://docs.microsoft.com/fr-fr/azure/storage/common/storage-account-create).
- Variable d'environnement (AZURE_STORAGE_CONNECTION_STRING) contenant la chaine de connexion --> [Voir ici](https://docs.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-python#configure-your-storage-connection-string)
<br/>

------------------
# Fonctionnalités principales

* Guide pas à pas à chaque étape avec de l'aide disponible.
* Script écrit de manière à anticiper/détecter/corriger les erreurs.
* Création d'un plan de sauvegarde, selon les SDK présentes.
* Sauvegarde en ligne avec gestion des rotations (automatisable via Cron ou Planificateur Windows).
* Restauration avec choix de la date selon les sauvegardes disponibles en ligne.
<br/>

------------------
# Lancement Rapide

1. Tout d'abord, vérifiez les [Prérequis](#Prérequis) ci-dessus.

2. Clonez ensuite le dépôt Github dans un dossier local. [Lien](https://github.com/Val-Bch/backup-multi-cloud.git)

3. Assurez-vous que le script à bien le droit de s'exécuter et qu'il à les droits R/W dans le répertoire où il se trouve.

4. Lancez le script avec Python3. 
  Exemples : 
    - Windows : ```C:/Python38-32/python.exe c:/backup-multi-cloud/backup-multi-cloud.py```
    - Linux : ```./backup-multi-cloud/backup-multi-cloud.py```  
           ou ```python3 /backup-multi-cloud/backup-multi-cloud.py```

5. Laissez-vous guider :) 
<br/>

------------------

# Lancement Avancé

## Arguments 


Le script backup-multi-cloud.py prend en charge la liste des arguments suivants :
<br/>
<br/>

| Argument                    | Option          | Fonction                                              |
|-----------------------------|-----------------|-------------------------------------------------------|
|--action (-a)                | create          | Assiste la création d'un nouveau plan de sauvegarde   |
|--action (-a)                | save            | Exécute un plan de sauvegarde existant                |
|--action (-a)                | restore         | Restaure une sauvegarde                               |
|--plan (-p)                  | nomduplan.cfg   | Cible un plan existant                                |
|--quiet (-q)                 |                 | Empêche le print de fonctionner                       |
|--verbose (-v)               | (par défaut)    | Force le print à s'activer                            |
<br/>

**Exemples :**

```C:/Python38-32/python.exe c:/backup-multi-cloud/backup-multi-cloud.py -a save -p Plan-Azure-demo.cfg```<br/>
Cette commande (Windows) effectuera une sauvegarde, en utilisant les paramètres du plan "Plan-Azure-demo.cfg" (préalablement créé)

```./backup-multi-cloud.py -a create```<br/>
Cette commande (Linux) permettra de créer de manière assistée un nouveau plan de sauvegarde.
<br/>
<br/>

------------------
##   Automatisation

Le script backup-multi-cloud.py a pour objectif d'être automatisé pour effectuer des sauvegardes.
Pour ce faire, l'emplois de l'argument ```--quiet (-q)``` est **obligatoire** pour ne pas produire de sortie d'affichage (print).
<br/>

-------------
### -- Crontab

Pour un système Linux utilisant Crontab voici des exemples de réglages.

1. En root lancé `crontab -e`

2. Saisir :  ```05 2 * * * usr/backup-multi-cloud/backup-multi-cloud.py -q -a save -p Plan-Azure-demo.cfg  >/dev/null 2>&1```  
(Exécutera le script pour effectuer une sauvegarde tous les jours à 2h05) 

3. Sauvegarder et quitter l'éditeur choisi

Si rien ne se produit, merci de consulter le fichier de log ```/backup-multi-cloud/log/0-log-error.txt``` pour comprendre l'origine de l'erreur.
<br/>

-----------------------
### -- Tâches Planifiées

Pour un système Windows utilisant le Planificateur de Taches.

1. Au clavier appuyer sur les touches ```Windows + R``` pour ouvrir ```Exécuter```

2. Saisir ```Taskschd.msc``` et valider.

3. Sur la droite --> ```Créer une tâche de base...```

4. Se laisser guider pour les options et choisir ```Démarrer un programme```

5. Choisir le script ```backup-multi-cloud.py``` avec ```Parcourir```

6. Saisir les arguments dans la case prévue : ```-q -a save -p Plan-Azure-demo.cfg```
<br/>
<br/>

----------------------
#  Ajouter un SDK
<br/>

Voir le détail dans le [fichier contributing.md](https://github.com/Val-Bch/backup-multi-cloud/blob/master/contributing.md#Ajouter-un-SDK).

<br/>
<br/>

----------------------
#  Log
Le script est multi plateforme (Windows/Linux) et utilise ses propres fichiers de logs.
Ces derniers sont contenus dans le sous-dossier "backup-multi-cloud//log" 

Il y a 4 types de logs.
1. ```0-log-error.txt``` >> contient les lancements/sorties de script provocants des erreurs liées souvent à de mauvais réglages.

2. ```Plan-Azure-nom-upload-YYYY.MM.txt``` >> contient la liste de tous les uploads réalisés durant le mois "MM"

3. ```Plan-Azure-nom-delete-YYYY.MM.txt``` >> contient la liste de tous les fichiers en lignes supprimés durant le mois "MM" (selon la rotation des sauvegardes paramétrée)

4. ```Plan-Azure-nom-restore-YYYY.MM.txt``` >> contient la liste de tous les fichiers restaurés durant le mois "MM"

<br/>
<br/>

---------------------
#  Contribution
<br />

Pour contribuer à améliorer ou corriger ce projet, merci de vous référez au [fichier contributing.md](https://github.com/Val-Bch/backup-multi-cloud/blob/master/contributing.md).

<br/>
<br/>

---------------------
#  License

 <p><a href="https://github.com/Val-Bch/backup-multi-cloud/blob/master/LICENSE">
 <img width=6% src="https://www.gnu.org/graphics/gplv3-or-later.svg"/>  
 "backup-multi-cloud.py" et "sdk_azure.py" sont sous licence GNU General Public License v3.0 
 </a></p>
