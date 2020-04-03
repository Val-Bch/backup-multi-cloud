import os, uuid, glob, configparser, unicodedata, re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime, timedelta

date_Value = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss')
local_path = "c:/Users/Valentin/Desktop/Temp"
local_file_name = "essai-" + date_Value + ".txt"
upload_file_path = os.path.join(local_path, local_file_name)
cfg = configparser.ConfigParser()


def listing_plan():

    list_conf = os.listdir('./conf')                #Liste les fichiers .cfg du dossier "conf"
    list_nb = list(range(1, len(list_conf)+1))      #Liste qui incrémente chaque item de +1 jusqu'au nombre d'éléments présents dans "list_conf" (+1 pour inclure le dernier dans le range) 
    cles, vals = list_nb, list_conf                 #identifie les clés et valeurs du dictionnaire selon les 2 précédantes listes
    dct_conf = {a:b for a, b in zip(cles, vals)}    #Dictionnaire qui assemble les 2 listes pour donner des numéros au noms de fichier.cfg et faciliter la saisie
    print("\nListe des plans disponibles :\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")
    global plan
    while True:       #Boucle pour choisir un plan valide dans la liste
        choix_plan = input("Saisir le numéro du plan de sauvegarde à utiliser "+str(list_nb)+" (help) : ")  #Affiche les choix possibles de la liste et propose de l'aide

        if choix_plan == "help":    #si saisie = help, affiche des explications
            print("     ###########################\n                 AIDE\n     ###########################\n")
            print(" - Saisir un nombre entier de liste correspondant à un nom de fichier :\n    Exemple : "+str(dct_conf))
            print("    Dans cette liste si le nombre saisi est '1', le fichier selectionné sera '"+str(dct_conf[int(1)])+"'\n")
        elif not choix_plan:        #Si la saisie est vide, réaffiche les choix possibles
            print("\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")
        elif (choix_plan.isdigit()):    #Si la saisie est nombre entier
            if int(choix_plan) in list_nb:  #si ce nombre saisi est compris dans liste des choix possibles
                plan = dct_conf[int(choix_plan)]    #Variable plan = valeur de la clé du dico correspondante au choix user
                print("La fichier "+ plan + " a été choisi.")
                return plan
            else:
                 pass         

for files in os.listdir(local_path):
    if os.path.isdir(files):
        print(files)
    else:
        print(files +" : est un fichier ")