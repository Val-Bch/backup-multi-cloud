Ce script permet d'assister à la création, de faciliter et d'automatiser des plans de sauvegardes vers des stokages Cloud comme Azure Blob Storage.
Il est évolutif et vous permet d'intégrer des SDK Python sous forme de 'packages'. 
Est inclus ici le SDK Python 'Stockage Blob Azure v12' de Microsoft.

Prérequis : 
===========
- Microsoft ou Linux (Testé sous Debian, Ubuntu et Windows 10)
- Python 3 ou >
- Package Azure : {pip install azure-storage-blob}
- Compte Azure avec un abonnement actif. [Créez un compte gratuitement](https://azure.microsoft.com/free/?ref=microsoft.com&utm_source=microsoft.com&utm_medium=docs&utm_campaign=visualstudio).
- Un compte de stockage Azure (Blob pas DataLake). [Créer un compte de stockage](https://docs.microsoft.com/fr-fr/azure/storage/common/storage-account-create).
- Une variable d'environnement (AZURE_STORAGE_CONNECTION_STRING) contenant votre chaine de connexion --> [Voir ici](https://docs.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-python#configure-your-storage-connection-string)


Fonctionnalités principales : 
=============================
* Guide pas à pas à chaque étape avec de l'aide disponible.
* Script écrit de manière à anticiper/détecter/corriger les erreurs.
* Création d'un plan de sauvegarde, selon les SDK présentes.
* Sauvegarde en ligne avec gestion des rotations (automatisable via Cron ou Planificateur Windows).
* Restauration avec choix de la date selon les sauvegardes disponibles en ligne.

Table des matières
==================

    Démarrage Rapide
    Caractéristiques
    Installation
    Notes IMPORTANTES

Démarrage Rapide
----------------

Tout d'abord, vérifiez les Prérequis ci-dessus.

Clonnez ensuite le dépot Github dans un dossier local. [Lien](https://github.com/Val-Bch/backup-multi-cloud.git)

Assurez vous que le script à bien le droit de s'éxécuter et qu'il à les droits R/W dans le repertoire où il se trouve.

Lancer le script avec Python. Exemples : 
    Windows : `C:/Users/name/AppData/Local/Programs/Python/Python38-32/python.exe c:/Git/backup-multi-cloud/backup-multi-cloud.py`
    Linux : ``

Laissez vous guider :) 

