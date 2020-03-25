import os, uuid, glob, configparser
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime, timedelta

date_Value = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss')
local_path = "c:/Users/Valentin/Desktop/Temp/Git/backup-multi-cloud/SDK_cloud/Azure/data"
local_file_name = "essai-" + date_Value + ".txt"
upload_file_path = os.path.join(local_path, local_file_name)
cfg = configparser.ConfigParser()

def create_azure(file_conf):
    dir_conf = "/../../conf"
    file_path = os.path.join(dir_conf, file_conf)
    connect_str = input("Saisir la chaine de connexion (dans 'Clé d'accès' du menu 'Paramètres' du compte de stockage Azure) : ")
    cfg.set(file_conf, 'connect_str', str(connect_str))
    cfg.write(open(file_path,'w'))

create_azure("Sauvegarde-Azure-1.cfg")