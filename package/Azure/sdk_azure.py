import os, uuid, configparser
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
    container_name =  input("----------------\nEntrer le nom du conteneur d'objet Blob Azure à créer/utiliser : ") 

    # Ouverture du fichier.cgf cible, inscription des variables saisies dans des clés de la section principale, puis sauvegarde du fichier
    cfg.read(file_path)
    cfg.set(file_conf, 'connect_str', str(connect_str))
    cfg.set(file_conf, 'container_name', str(container_name))
    cfg.write(open(file_path,'w'))


def save_azure(file_conf, path_conf, path_package):
    """ 
    Fonction appelée lors de l'exécution d'une sauvegarde par le script principal
    Contient le sdk python fournit par Azure, avec quelques ajustements.
    Récupère en paramètre la variable file_conf qui contient le nom du plan sur lequel travailler
    """
    try:
        print("Azure Blob storage v12")
        
        # Ouverture du fichier.cfg et stockage dans des variables pour les clés nécessaires
        cfg.read(file_conf)
        connect_str = cfg.get(file_conf, 'connect_str') 
        container_name =cfg.get(file_conf, 'container_name') 

        # Créez l'objet BlobServiceClient qui sera utilisé pour créer un client conteneur
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Défini un variable 'date_Value' qui contient la date+heure actuelle + création d'un nom unique au contenaire basé sur save- + la date 
        date_Value = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss') 
        container_name = "save-" + date_Value

        # Création du contenaire
        container_client = blob_service_client.create_container(container_name)

        # Create a file in local Documents directory to upload and download
        local_path = "c:/Users/Valentin/Desktop/Temp/Git/backup-multi-cloud/SDK_cloud/Azure/data"
        local_file_name = "essai-" + date_Value + ".txt"
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file
        file = open(upload_file_path, 'w')
        file.write("Hello, moi!")
        file.close()

        # Créez un client blob en utilisant le nom de fichier local comme nom pour le blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nTéléchargement vers Azure Storage en tant qu'objet blob :\n\t" + local_file_name)

        # Upload le fichier créé
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
    
    
        print("\nListe des blobs...")

        # Liste les blobs dans le container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)

        # Téléchargez le blob dans un fichier local
        # Ajoutez 'DL' avant l'extension .txt pour voir les deux fichiers dans Documents
        download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DL.txt'))
        print("\nTéléchargement de blob sur \n\t" + download_file_path)

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        # Clean up
        print("\nAppuyez sur la touche Entrée pour commencer le nettoyage")
        input()

        print("Suppression du conteneur d'objets blob ...")
        container_client.delete_container()

        print("Suppression de la source locale et des fichiers téléchargés ...")
        os.remove(upload_file_path)
        os.remove(download_file_path)

        print("Terminé.")


    except Exception as ex:
        print('Exception:')
        print(ex)