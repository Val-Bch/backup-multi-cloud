import os, uuid, configparser, unicodedata, re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime, timedelta

cfg = configparser.ConfigParser()


def create_azure(file_conf, path_conf):
    """
    Fonction appelée par la fonction générale de création, pour la création d'un plan de sauvegarde avec Azure Storage Blob
    Récupère en paramètre la variable file_conf et path_conf qui contiennent le nom du plan sur lequel travailler et son chemin absolu
    Met à jour le fichier.cfg avec les particularités de connexions liées à cette plateforme Cloud (ici la variable 'connect-str' qui contient la chaine de connexion Azure)
    """
    # Construction du chemin absolu du fichier de conf.cfg
    file_path = os.path.join(path_conf, file_conf)

    # Demande les détails pour la sauvegarde Azure (Clé d'accès, nom du conteneur)
    connect_str = input("----------------\nEntrer la chaine de connexion (dans 'Clé d'accès' du menu 'Paramètres' du compte de stockage Azure) : ")
    container_name =  input("----------------\nEntrer le nom du conteneur d'objet Blob Azure à créer/utiliser (help) : ") 
    if container_name == "help":    # Affiche l'aide selon les informations Azure
        print("     ###########################\n                 AIDE\n     ###########################\n")
        print("\n    - Le nom doit avoir entre 3 et 63 caractères.\n      - Ce nom peut contenir seulement des lettres MINUSCULES, des chiffres et des traits d'union.\n")
        print("    - Il doit commencer par une lettre ou un chiffre.\n")
        print("    - Chaque trait d'union doit être précédé et suivi d'un caractère autre qu'un trait d'union.\n")
        print("    - Il doit commencer par une lettre ou un chiffre.\n")
    else:   # Sinon on essaie de nettoyer la saisie en supprimant les accents, les majuscules, les caractères spéciaux et les espaces
        container_name_correct = unicodedata.normalize('NFKD', container_name)
        container_name_correct =  container_name_correct.encode('ascii', 'ignore').decode('ascii').lower()
        container_name_correct = re.sub('[^A-z0-9 -]', '', container_name_correct).replace(" ", "").replace("--", "-").replace("^", "").replace("[", "").replace("]", "").replace("\\", "").replace("_", "-")
        container_name = container_name_correct

    # Ouverture du fichier.cgf cible, inscription des variables saisies dans des clés de la section principale, puis sauvegarde du fichier
    cfg.read(file_path)
    cfg.set(file_conf, 'connect_str', str(connect_str))
    cfg.set(file_conf, 'container_name', str(container_name))
    cfg.write(open(file_path,'w'))


def save_azure(file_path, choix_plan):
    """ 
    Fonction appelée lors de l'exécution d'une sauvegarde par le script principal
    Contient le sdk python fournit par Azure, avec quelques ajustements.
    Récupère en paramètre la variable file_conf qui contient le nom du plan sur lequel travailler
    """
    try:
        print("Exécution d'une sauvegarde Azure Blob storage")
        
        # Ouverture du fichier.cfg et stockage dans des variables pour les clés nécessaires
        cfg.read(file_path)
        connect_str = cfg.get(choix_plan, 'connect_str') 
        container_name = cfg.get(choix_plan, 'container_name')
        path_source = cfg.get(choix_plan, 'path_source') 

        # Créez l'objet BlobServiceClient qui sera utilisé pour créer un client conteneur
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Défini un variable 'date_Value' qui contient la date+heure actuelle + création d'un nom unique au contenaire basé sur save- + la date 
        date_Value = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss') 
        
        # Récupère la liste des containers dans une variable
        container_online = blob_service_client.list_containers()  
        
        # Pour charque item de container_online, on l'ajoute à la liste container_list
        container_list = []
        for item in container_online:      
            container_list.append(item.name)
        
        if container_name in container_list:    # Si le container existe déjà dans Azure, on continue le script
            pass
        else:   # Si le container n'existe pas on le créé
            blob_service_client.create_container(container_name)

        #Scan du repertoire cible 
        os.listdir(path_source)

        for files in os.listdir(path_source):
            
            if os.path.isdir(files):
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=files)
                upload_file_path = os.path.join(path_source, files)
                blob_client.upload_dir(source, dest)

            else:
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=files)
                upload_file_path = os.path.join(path_source, files)
                with open(upload_file_path, "rb") as data:
                    blob_client.upload_blob(data)

        print("Terminé.")


    except Exception as ex:
        print('Exception:')
        print(ex)
