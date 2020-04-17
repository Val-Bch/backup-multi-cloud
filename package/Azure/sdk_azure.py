#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, uuid, configparser, unicodedata, re, sys, time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime, timedelta

cfg = configparser.ConfigParser()

class DirectoryClient:
  """
   Class extraite du sdk python pour Microsoft Azure Blob Storage V12.\n
   - FILE: blob_samples_directory_interface.py\n
   # -------------------------------------------------------------------------\n
   # Copyright (c) Microsoft Corporation. All rights reserved.\n
   # Licensed under the MIT License. See License.txt in the project root for license information.\n
   # --------------------------------------------------------------------------
  """
  def __init__(self, connection_string, container_name):
    service_client = BlobServiceClient.from_connection_string(connection_string)
    self.client = service_client.get_container_client(container_name)

  def upload(self, source, dest):
    '''
    Upload a file or directory to a path inside the container
    '''
    if (os.path.isdir(source)):
      self.upload_dir(source, dest)
    else:
      self.upload_file(source, dest)

  def upload_file(self, source, dest):
    '''
    Upload a single file to a path inside the container
    '''
    print(f'Uploading {source} to {dest}')
    with open(source, 'rb') as data:
      self.client.upload_blob(name=dest, data=data)

  def upload_dir(self, source, dest):
    '''
    Upload a directory to a path inside the container
    '''
    prefix = '' if dest == '' else dest + '/'
    prefix += os.path.basename(source) + '/'
    for root, dirs, files in os.walk(source):
      for name in files:
        dir_part = os.path.relpath(root, source)
        dir_part = '' if dir_part == '.' else dir_part + '/'
        file_path = os.path.join(root, name)
        blob_path = prefix + dir_part + name
        self.upload_file(file_path, blob_path)

  def download(self, source, dest):
    '''
    Download a file or directory to a path on the local filesystem
    '''
    if not dest:
      raise Exception('A destination must be provided')

    blobs = self.ls_files(source, recursive=True)
    if blobs:
      # if source is a directory, dest must also be a directory
      if not source == '' and not source.endswith('/'):
        source += '/'
      if not dest.endswith('/'):
        dest += '/'
      # append the directory name from source to the destination
      dest += os.path.basename(os.path.normpath(source)) + '/'

      blobs = [source + blob for blob in blobs]
      for blob in blobs:
        blob_dest = dest + os.path.relpath(blob, source)
        self.download_file(blob, blob_dest)
    else:
      self.download_file(source, dest)

  def download_file(self, source, dest):
    '''
    Download a single file to a path on the local filesystem
    '''
    # dest is a directory if ending with '/' or '.', otherwise it's a file
    if dest.endswith('.'):
      dest += '/'
    blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

    print(f'Downloading {source} to {blob_dest}')
    os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
    bc = self.client.get_blob_client(blob=source)
    with open(blob_dest, 'wb') as file:
      data = bc.download_blob()
      file.write(data.readall())

  def ls_files(self, path, recursive=False):
    '''
    List files under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
      path += '/'

    blob_iter = self.client.list_blobs(name_starts_with=path)
    files = []
    for blob in blob_iter:
      relative_path = os.path.relpath(blob.name, path)
      if recursive or not '/' in relative_path:
        files.append(relative_path)
    return files

  def ls_dirs(self, path, recursive=True):
    '''
    List directories under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
      path += '/'

    blob_iter = self.client.list_blobs(name_starts_with=path)
    dirs = []
    for blob in blob_iter:
      relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
      if relative_dir and (recursive or not '/' in relative_dir) and not relative_dir in dirs:
        dirs.append(relative_dir)

    return dirs

  def rm(self, path, recursive=False):
    '''
    Remove a single file, or remove a path recursively
    '''
    if recursive:
      self.rmdir(path)
    else:
      print(f'Deleting {path}')
      self.client.delete_blob(path)

  def rmdir(self, path):
    '''
    Remove a directory and its contents recursively
    '''
    blobs = self.ls_files(path, recursive=True)
    if not blobs:
      return

    if not path == '' and not path.endswith('/'):
      path += '/'
    blobs = [path + blob for blob in blobs]
    print(f'Deleting {", ".join(blobs)}')
    self.client.delete_blobs(*blobs)


#############################
#  Fonctions Personnalisées #

def create_azure(file_conf, path_conf):
    """
    Fonction appelée par le script principal pour la création d'un plan de sauvegarde avec Azure Storage Blob.\n
    Met à jour le fichier.cfg avec les particularités de connexions liées à cette plateforme Cloud (ici la variable 'connect-str' qui contient la chaine de connexion Azure).\n
    Utilise les paramètres : \n
    - file_conf = le nom du plan sur lequel travailler.
    - path_conf = chemin absolu du fichier de configuration .cfg qui sera utilisé.
    """
    # Construction du chemin absolu du fichier de conf.cfg
    file_path = os.path.join(path_conf, file_conf)

    # Demande les détails pour la sauvegarde Azure (Clé d'accès, nom du conteneur)
    while True:
      if not os.getenv('AZURE_STORAGE_CONNECTION_STRING'):
        print("\n####################\n! ATTENTION !  Aucune variable d'environnement 'AZURE_STORAGE_CONNECTION_STRING' n'est détectée.")
        print("- Veuillez vérifier cette variable d'environnement (voir prérequis du README).")
        print("- Après avoir ajouté la variable d’environnement, redémarrez tous les programmes en cours d’exécution qui devront la lire.")
        print("- Par exemple, redémarrez votre environnement de développement ou éditeur avant de continuer.\n####################")
        sys.exit()
      else:
        # Test la connexion pour savoir si la clé est valide avec petite animation
        try: 
          CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
          BlobServiceClient.from_connection_string(CONNECTION_STRING)
          print("----------------")
          print("\nTest de connexion au compte Azure Storage en cours", end=" ")
          for i in range(70):
            if i%10==0:
              time.sleep(.400)
              print(".", end=" ", flush=True)
          print("Réussi !\n")     
          break
        except Exception as ex:
          print('Erreur de connexion :')
          print(ex)

    while True:  # Boucle pour définir le nom du conteneur selon les restrictions éditées par Azure
        container_name =  input("----------------\nEntrer le nom du conteneur d'objet Blob Azure à créer/utiliser (help) : ") 
        if container_name == "help":    # Affiche l'aide selon les informations Azure
            print("###########################\n|\t    AIDE\n|")
            print("| ~~ Prérequis Azure ~~\n|- Le nom doit avoir entre 3 et 63 caractères.\n| - Ce nom peut contenir seulement des lettres MINUSCULES, des chiffres et des traits d'union.")
            print("|- Il doit commencer par une lettre ou un chiffre.")
            print("|- Chaque trait d'union doit être précédé et suivi d'un caractère autre qu'un trait d'union.")
            print("|- Il doit terminer par une lettre ou un chiffre.")
            print("###########################")
        else:   
            # Sinon on essaie de nettoyer la saisie en supprimant les accents, les majuscules, les caractères spéciaux, les espaces...
            container_name_correct = unicodedata.normalize('NFKD', container_name)
            container_name_correct = container_name_correct.encode('ascii', 'ignore').decode('ascii').lower()
            
            # Test sur le nombre de caractères attendus
            if len(container_name_correct) < 3 or len(container_name_correct) > 63:
                print("Erreur : \n - Merci de respecter le nombre de caractères (min=3 max=63).")
                pass
            else: 
                # Boucle pour corriger tous les caractères saisis et notamment les suites de + de 2 tirets/underscore
                for caracters in container_name_correct: 
                    caracters = re.sub('[^A-z0-9 -]', '', container_name_correct).replace(" ", "").replace("--", "-").replace("^", "").replace("[", "").replace("]", "").replace("\\", "").replace("_", "-")
                    container_name_correct = caracters

                container_name = container_name_correct
                
                # Test si container_name n'est pas vide ou ne commence/termine par un tiret
                if not container_name or container_name.startswith('-') or container_name.endswith('-'):  
                    print("Erreur le nom est vide ou invalide.")
                    pass
                else:
                    print("Le contenaire utilisé sera : ""'"+container_name+"'")
                    try: 
                        alerte = input("Continuer ? (o/n) : ")  # Propose de confirmer pour éviter toute erreur rendu à la fin du script
                        if alerte == "o":
                            break
                        elif alerte == "n":
                            pass
                    except Exception as ex:
                        print('Exception:')
                        print(ex)


    # Ouverture du fichier.cgf cible, inscription des variables saisies dans des clés de la section principale, puis sauvegarde du fichier
    cfg.read(file_path)
    cfg.set(file_conf, 'container_name', str(container_name))
    cfg.write(open(file_path,'w'))



def save_azure(file_path, choix_plan, init_path, path_log):
    """ 
    Fonction appelée lors de l'exécution d'une sauvegarde par le script principal\n
    Utilise le sdk python fournit par Microsoft, avec quelques ajustements.\n
    Utilise les paramètres :
    - file_conf = emplacement du fichier de configuraton .cfg
    - choix_plan = nom du plan de sauvegarde
    - init_path = chemin absolu depuis lequel le script à été lancé
    """
    try:
        print("Exécution d'une sauvegarde Azure Blob storage :")
        
        # Ouverture du fichier.cfg et stockage dans des variables pour les clés nécessaires
        cfg.read(file_path)
        CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        CONTAINER_NAME = cfg.get(choix_plan, 'container_name')
        path_source = cfg.get(choix_plan, 'path_source') 
        bkp_rotate = cfg.get(choix_plan, 'bkp_rotate')
        date_value = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss')        # Création d'un nom unique basé sur la date pour le dossier racine dans le container
        
        # Créer l'objet BlobServiceClient qui sera utilisé pour créer un client conteneur
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

        # Récupère la liste des containers existant dans une variable
        container_online = blob_service_client.list_containers()  
        
        # Pour chaque item de container_online, on l'ajoute à la liste container_list
        container_list = []
        for item in container_online:      
            container_list.append(item.name)
        
        if CONTAINER_NAME in container_list:    # Si le container existe déjà dans Azure, on continue le script
            pass
        else:   # Si le container n'existe pas on le créé
            blob_service_client.create_container(CONTAINER_NAME)

        # Création d'objet pour utiliser la class et définir le contenaire
        client = DirectoryClient(CONNECTION_STRING, CONTAINER_NAME)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        

        # Construction d'une arborescence pour classer les save + Appel de la fonction d'upload + log dans un fichier txt, à la racine de la sauvegarde, le resultat
        client.upload(path_source, choix_plan+"/"+date_value)
        blob_list = container_client.list_blobs(name_starts_with=(choix_plan+"/"+date_value))
        for blob in blob_list:
            with open(path_log+'/'+choix_plan[0:-4]+'-upload-'+datetime.now().strftime('%Y.%m')+'.txt', 'a') as file: # Log l'upload dans un txt qui change de nom tout les mois
                file.write("\nFichier uploadé : ---- " + blob.name)
    
        # Récupération des blobs en ligne sous l'arborescence commençant par 'choix_plan'
        blob_list = container_client.list_blobs(name_starts_with=(choix_plan+"/"))
        
        for blob in blob_list:                                                          # Pour chaque élément de la liste  
          if blob.name.startswith(choix_plan+"/") :                                     # Si l'élement est dans l'arbo du 'choix_plan'
            recup_date = blob.name.replace(choix_plan+'/', '')[0:22]                    # Récupère la date d'upload
            convert_recup_date = datetime.strptime(recup_date, '%Y-%m-%d-%Hh-%Mm-%Ss')  # Convertit la date d'upload (str) en vrai date
            delta = datetime.now() - convert_recup_date                                 # Calcul le delta entre la date actuelle et la date d'upload
            if delta.days >= int(bkp_rotate) and int(bkp_rotate) != 0:                  # Si l'écart de jours du delta est >= à la date de rotation choisie et diff de 0
              client.rm(blob.name)                                                      # Suppression de l'objet blob
              with open(path_log+'/'+choix_plan[0:-4]+'-delete-'+datetime.now().strftime('%Y.%m')+'.txt', 'a') as file: # Log la suppression dans un txt qui change de nom tout les mois
                file.write("\nFichier supprimé le "+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : ---- " + blob.name)

    
    except Exception as ex:
        print('Exception:')
        print(ex)


def restore_azure(file_path, choix_plan, init_path, path_log):
    """ 
    Fonction appelée lors de l'exécution d'une restauration par le script principal\n
    Utilise le sdk python fournit par Microsoft, avec quelques ajustements.\n
    Utilise les paramètres :
    - file_conf = emplacement du fichier de configuraton .cfg
    - choix_plan = nom du plan de sauvegarde
    - init_path = chemin absolu depuis lequel le script à été lancé
    """
    try:
        print("Exécution d'une restauration Azure Blob storage :")
        
        # Ouverture du fichier.cfg et stockage dans des variables pour les clés nécessaires
        cfg.read(file_path)
        CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING') 
        CONTAINER_NAME = cfg.get(choix_plan, 'container_name')
        
        # Créer l'objet BlobServiceClient qui sera utilisé pour créer un client conteneur
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

        # Récupère la liste des containers existant dans une variable
        container_online = blob_service_client.list_containers()  
        
        # Pour chaque item de container_online, on l'ajoute à la liste container_list
        container_list = []
        for item in container_online:      
            container_list.append(item.name)

        # Création d'objet pour utiliser la class et définir le contenaire
        client = DirectoryClient(CONNECTION_STRING, CONTAINER_NAME)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Récupération des blobs en ligne sous l'arborescence commençant par 'choix_plan'
        blob_list = container_client.list_blobs(name_starts_with=(choix_plan+"/"))

        liste_date = []
        print("\nScan des contenaires et recherche des sauvegardes disponibles", end=" ")
        for i in range(70):
          if i%10==0:
            time.sleep(.300)
            print(".", end=" ", flush=True) 
  
        if CONTAINER_NAME in container_list:    # Si le container existe déjà dans Azure, on continue le script
          pass
        else:   # Si le container n'existe pas on stop
            print("\n ! ATTENTION ! : Le contenaire '"+CONTAINER_NAME+"' n'existe pas en ligne.\n")
            time.sleep(1)

        for blob in blob_list:   
                                                                 # Pour chaque élément de la liste  
          if blob.name.startswith(choix_plan+"/") :                                         # Si l'élement est dans l'arbo du 'choix_plan'
            recup_date = blob.name.replace(choix_plan+'/', '')[0:22]                        # Récupère la date d'upload  
            liste_date.append(recup_date) if recup_date not in liste_date else liste_date   # Si la date n'est pas déjà présente dans la liste on l'y ajoute
    
        while True:                     # Boucle tant que la saisie n'est pas nulle ou un nombre entier positif compris dans la liste
          for i, elt in enumerate(liste_date):
            print("\n-----------------\nChoisir '{}' pour restaurer la sauvegarde du : '{}'.".format(i, elt))  # Enumère la liste avec ses indices pour créer des choix simple à saisir

          choix_restore = input("\nChoix (help) : ")    # Demande le choix du user
                                         
          if choix_restore== "help":     # Si saisie = help, affiche des explications
            print("###########################\n|\t    AIDE\n|")
            print("| ~~ Fonctionnement ~~\n| - Saisir un nombre entier (>=0) compris dans les choix proposés.")
            print("| - Chaque nombre correspond à une date de sauvegarde disponible pour une restauration.\n|")
            print("| ~~ Exemple ~~\n| - Nombre choisi = '0'")
            print("|  --> La sauvegarde en date du '"+liste_date[0]+"' sera restaurée.\n|")
            print("###########################\n")
          elif not choix_restore:            # Si la saisie est vide, on boucle
            pass
          elif choix_restore.isdigit() and int(choix_restore) < len(liste_date) :    # Si la saisie est bien un nombre entier positif compris dans la 'liste_date'
            print("La sauvegarde en date du '"+liste_date[int(choix_restore)]+"' sera restaurée.\n")

            while True:
              dir_restore = input("Saisir le chemin absolu où restaurer la sauvegarde (help) : ")   # Boucle pour définir le repertoire de restauration

              if dir_restore== "help":     # Si saisie = help, affiche des explications
                print("###########################\n|\t    AIDE\n|")
                print("| ~~ Fonctionnement ~~\n| - Saisir le chemin absolu du dossier local qui accueillera la restauration.\n| - La sauvegarde choisie y sera téléchargée.")
                print("| - Les fichiers homonymes déjà présents dans le repertoire cible seront écrasés.\n| - Les repertoires seront conservés.\n|")
                print("| ~~ Exemple ~~\n| - Chemin saisi : '/usr/local/bin/restauration'")
                print("|  --> Tous les sous-dossiers et fichiers contenus dans la sauvegarde Azure y seront téléchargés dans un dossier nommé '"+liste_date[int(choix_restore)]+"'.\n|")
                print("###########################\n")
              elif not dir_restore:            # Si la saisie est vide, on applique la valeur par défaut et on affiche 'result'
                print("Merci de saisir un chemin, la réponse ne peut-être vide.")

              else:
                if os.path.isdir(dir_restore):  # Test si le repertoire cible existe
                  print("La sauvegarde sera restaurée dans : '"+ dir_restore +"/"+ liste_date[int(choix_restore)] +"'.")
                  # Exécute la restauration et log le resultat dans un fichier txt
                  client.download(choix_plan+"/"+str(liste_date[int(choix_restore)]), dir_restore)
                  blob_list = container_client.list_blobs(name_starts_with=(choix_plan+"/"+liste_date[int(choix_restore)]))
                  for blob in blob_list:
                    # Log dans un fichier qui change de nom tout les mois pour éviter un log trop gros
                    with open(path_log+'/'+choix_plan[0:-4]+'-restor-'+datetime.now().strftime('%Y.%m')+'.txt', 'a') as file: 
                      file.write("\nFichier restauré le "+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : " + blob.name)
                  break  

                else: 
                  print("!! Attention, ce repertoire semble ne pas exister, si vous continuez, merci de le créer avant de continuer la restauration.")
                  try: 
                    alerte = input("Continuer ? (o/n) : ")
                    if alerte == "o" or not alerte:
                      if os.path.isdir(dir_restore): # Test à nouveau si le repertoire existe
                        # Exécute la restauration et log le resultat dans un fichier txt 
                        client.download(choix_plan+"/"+str(liste_date[int(choix_restore)]), dir_restore)
                        blob_list = container_client.list_blobs(name_starts_with=(choix_plan+"/"+liste_date[int(choix_restore)]))
                        for blob in blob_list:
                          with open(path_log+'/'+choix_plan+'-restor.txt', 'a') as file:
                            file.write("\nFichier restauré le "+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : " + blob.name)
                        break  

                      else: # Si le repertoire n'existe toujours pas, on ferme le script
                        print("Erreur, le repertoire ciblé n'exite toujours pas, merci de le créer avant de relancer une restauration.")    
                        sys.exit()

                    elif alerte == "n":
                      sys.exit()

                  except Exception as ex:
                    print('Exception:')
                    print(ex)
            break
          else:
            pass
    
    except Exception as ex:
        print('Exception:')
        print(ex)