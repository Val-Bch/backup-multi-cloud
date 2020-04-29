[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE) 
[![Python 3.7.3](https://img.shields.io/badge/Python-3.7.3-blue)](https://www.python.org/downloads/release/python-373/) 
[![Platform tested](https://img.shields.io/badge/Plateform%20tested-Win--32%20%7C%20Win--64%20%7C%20Linux--64-orange)](#) 
[![Last commit](https://img.shields.io/github/last-commit/Val-Bch/backup-multi-cloud?label=Last%20Modified)](https://img.shields.io/github/last-commit/Val-Bch/backup-multi-cloud?label=Last%20Modified)


---------------------

Ce script permet d'assister à la création, de faciliter et d'automatiser des plans de sauvegardes vers des stokages Cloud comme Azure Blob Storage.
Il est évolutif et vous permet d'intégrer des SDK Python sous forme de 'packages'. 
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
- [Log](#les-fichiers-logs)
- [Licence](#licence)
- [Contribution](#contribution)
<br/>

------------------
# Prérequis

- Microsoft ou Linux (Testé sous Debian, Ubuntu et Windows 10)
- Python 3 ou >
- Package Azure : {pip install azure-storage-blob}
- Compte Azure avec un abonnement actif. [Créez un compte gratuitement](https://azure.microsoft.com/free/?ref=microsoft.com&utm_source=microsoft.com&utm_medium=docs&utm_campaign=visualstudio).
- Un compte de stockage Azure (Blob pas DataLake). [Créer un compte de stockage](https://docs.microsoft.com/fr-fr/azure/storage/common/storage-account-create).
- Une variable d'environnement (AZURE_STORAGE_CONNECTION_STRING) contenant votre chaine de connexion --> [Voir ici](https://docs.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-python#configure-your-storage-connection-string)
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

 1. Tout d'abord, vérifiez les Prérequis ci-dessus.

2. Clonnez ensuite le dépot Github dans un dossier local. [Lien](https://github.com/Val-Bch/backup-multi-cloud.git)

3. Assurez vous que le script à bien le droit de s'éxécuter et qu'il à les droits R/W dans le repertoire où il se trouve.

4. Lancer le script avec Python. 
  Exemples : 
    - Windows : ```C:/Python/Python38-32/python.exe c:/Git/backup-multi-cloud/backup-multi-cloud.py```
    - Linux : ```./Git/backup-multi-cloud/backup-multi-cloud.py```  
           ou ```python3 /Git/backup-multi-cloud/backup-multi-cloud.py```

5. Laissez vous guider :) 

------------------
<br/>

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
|--quiet (-q)                 |                 | Empèche le print de fonctionner                       |
|--verbose (-v)               | (par défaut)    | Force le print à s'activer                            |
<br/>

Exemples :

```C:/Python/Python38-32/python.exe c:/Git/backup-multi-cloud/backup-multi-cloud.py -a save -p Plan-Azure-demo.cfg```<br/>
Cette commande (Windows) effectuera une sauvegarde, en utilisant les paramètres du plan "Plan-Azure-demo.cfg".

```./backup-multi-cloud.py -a create```<br/>
Cette commande (Linux) permettra d'assister pas à pas la création d'un nouveau plan de sauvegarde.
<br/>
<br/>

------------------
##   Automatisation

Le script backup-multi-cloud.py a pour objectif d'être automatisé pour effectuer des sauvegardes.
Pour ce faire, l'emplois de l'argument --quiet (-q) est obligatoire pour ne pas produire de sortie d'affichage (print).
<br/>

-------------
### -- Crontab

Pour un système Linux utilisant Crontab voici des exemples de réglages.

- En root lancé crontab -e puis saisir :

```05 2 * * * usr/local/bin/backup-multi-cloud/backup-multi-cloud.py -q -a save -p Plan-Azure-demo.cfg  >/dev/null 2>&1```

(Exécutera le script pour effectuer une sauvegarde tous les jours à 2h05) 

Si rien ne se produit, merci de consulter le fichier de log "/backup-multi-cloud/log/0-log-error.txt" pour comprendre l'origine de l'erreur.
<br/>

-----------------------
### -- Tâches Planifiées

Pour un système Windows utilisant le Planificateur de Taches.

1. Au clavier appuyer sur les touches "Windows + R" pour ouvrir "Exécuter".
2. Saisir "Taskschd.msc" et valider.
3. Sur la droite --> "Créer une tâche de base..."
4. Se laisser guider pour les options et choisir "Démarrer un programme".
5. Choisir le script "backup-multi-cloud.py" avec "Parcourir".
6. Saisir les arguments dans la case prévue : ```-q -a save -p Plan-Azure-demo.cfg```
<br/>
<br/>

----------------------
#  Log

Le script est multi plateforme (Windows/Linux) et utilise ses propres fichiers de logs.
Ces derniers sont contenus dans le sous-dossier "backup-multi-cloud//log" 

Il y a 4 types de logs.
0-log-error.txt >> contient les lancements/sorties de script provocants des erreurs liées souvent à de mauvais réglages.
Plan-Azure-nom-upload-YYYY.MM.txt >> 
<br/>

---------------------
#  License

 <p><a href="https://github.com/Val-Bch/backup-multi-cloud/blob/master/LICENSE">
 <img width=6% src="https://www.gnu.org/graphics/gplv3-or-later.svg"/>
 "backup-multi-cloud.py" et "sdk_azure.py" sont sous licence GNU General Public License v3.0 
 </a></p>
