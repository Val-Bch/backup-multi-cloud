# Contribuer

Vous souhaitez contribuer à ce projet ? Merci pour votre intérêt ! 

Ce projet utilise Git. Pour l'installer et l'utiliser, rendez-vous sur [le site officiel](https://git-scm.com). 

1. La première chose à faire est de [forker le repository](https://help.github.com/articles/fork-a-repo/).

2. Récupérez le code de votre fork et faites-le évoluer selon vos idées.
<br />
<br />

----------------------
# Signaler des bugs ou suggérer des améliorations

Si vous trouvez un bug dans les scripts, ou souhaitez participer à l'amélioration du programme : 

1. Merci de créer une [nouvelle issue](https://github.com/Val-Bch/backup-multi-cloud/issues/new/choose) 

2. Ou merci de me faire part de vos idées par mail --> [valentin-boucher+bmc@pm.me](mailto:valentin-boucher+bmc@pm.me)
<br />
<br />

----------------------
#  Ajouter un SDK
<br/>

Pour ajouter un nouveau SDK Python afin de cibler un autre cloud, il convient de respecter ces conditions : 

1. Créer un sous-dossier comportant le nom du Cloud dans le dossier ```package``` (Ex : pour AWS --> ```/package/AWS/```)

2. Placer dedans le fichier.py du SDK en respectant cette syntaxe : ```sdk_xxxx.py``` (Ex : pour AWS --> ```/package/AWS/sdk_aws.py```)

3. Ajouter les 3 fonctions suivantes dans le fichier ```sdk_xxxx.py``` où ```xxxx``` est le nom du cloud : 
    - ```def create_xxxx(file_conf, path_conf, path_log):```
    - ```def save_xxxx(file_path, choix_plan, init_path, path_log):```
    - ```def restore_xxxx(file_path, choix_plan, init_path, path_log):```

    +. La fonction create :  
      - Permet d'ajouter au fichier de configuration du plan (Ex : Plan-AWS-demo.cfg) les particularités de connexions et d'utilisation du Cloud ciblé.  
        Pour Azure par exemple, il est recommandé d'utiliser une variable d'environnement nommée "AZURE_STORAGE_CONNECTION_STRING" qui contient la chaine de connexion au compte et les conteneurs doivent respecter certains critères de nommage.
      
    +. La fonction save :  
      - Permet d'exécuter une sauvegarde. Cela comprend les particularités d'usage du SDK du Cloud ciblé, la gestion des rotations de sauvegardes, et le log dans un fichier.txt.  
      Il faut s'appuyer sur les fonctions d'upload et de suppression en ligne du SDK.

    +. La fonction restore :  
      - Permet de lister les sauvegardes présentent en ligne et de proposer d'en choisir une a restaurer puis de logger le résultat.  
      Il faut s'appuyer sur une fonction de listage et une fonction de download du SDK.

4. Adapter les paramètres requis par le SDK en fonction des paramètres transmis à l'appel des fonctions create, save et restore.
