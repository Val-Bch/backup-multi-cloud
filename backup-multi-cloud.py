#!/usr/bin/python3
import sys, argparse, os, configparser
import package.Azure.sdk_azure

#Gestion du lancement, de l'aide, et des arguments optionnels et positionnels
parser = argparse.ArgumentParser(description="Sauvegarde/restaration multi Cloud")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-a", "--action", nargs='+', help="Choisir une action : create | restore | save")
args = parser.parse_args()

#Fontion a appeler pour activer l'affichage (verbose)
def enablePrint():
    sys.stdout = sys.__stdout__
#Fontion a appeler pour désactiver l'affichage (quiet)
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

#Variables Gobales
cloud = " "
cfg = configparser.ConfigParser()
file_path = " "
plan = " "

#Fonction de listing des sdk cloud
def listing_cloud():
    enablePrint()
    list_pack = os.listdir('./package')     #Liste les sous-dossiers du dossier "package" qui sont nommés selon les plateformes cloud
    print("----------------\nListe des services cloud disponibles : " + str(list_pack))
    global cloud
    cloud = input("Saisir la plateforme cloud à utiliser : ")
    while True:       #Boucle pour choisir une plateforme valide dans la liste
        if cloud in list_pack:
            print("La plateforme "+ cloud + " a été choisie comme cible de la sauvegarde.")
            break
        else:
            cloud = input("Saisir la plateforme cloud à utiliser (sensible à la casse)" + str(list_pack) +" : ")



def listing_plan():
    """Fonction pour lister les plans de sauvegardes existants dans le dossier './conf)"""
    global plan

    list_conf = os.listdir('./conf')                #Liste les fichiers .cfg du dossier "conf"
    list_nb = list(range(1, len(list_conf)+1))      #Liste qui incrémente chaque item de +1 jusqu'au nombre d'éléments présents dans "list_conf" (+1 pour inclure le dernier dans le range) 
    cles, vals = list_nb, list_conf                 #identifie les clés et valeurs du dictionnaire selon les 2 précédantes listes
    dct_conf = {a:b for a, b in zip(cles, vals)}    #Dictionnaire qui assemble les 2 listes pour donner des numéros au noms de fichier.cfg et faciliter la saisie
    
    print("\nListe des plans disponibles :\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")
    
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


def creation():
    """Fonction pour assister à la création d'un nouveau plan de sauvegarde."""
    global file_path
    listing_cloud()     #Appel de la fontion pour lister les plateformes cloud disponible

    dir_conf = "./conf" #Emplacement du dossier pour les fichiers .cfg
    
    while True:
        plan_name = input("----------------\nDonner un nom/numéro unique à votre plan : ")

        file_conf = "Plan-" + str(cloud) +"-"+ str(plan_name)+".cfg"    #Construction du nom du fichier.cfg
        file_path = os.path.join(dir_conf, file_conf)                   #Contruction du chemin relatif pour mener au fichier .cfg
        file_exists = os.path.isfile(file_path)                         #Variable qui stocke le resultat de l'éxistense d'un fichier homonyme dans le dossier ./conf

        print("Le nom du fichier .cfg enregistré dans le dossier './conf' sera : "+ file_conf)

        if file_exists:
            print("Ce nom est déjà utilisé.")
        else:
            cfg.add_section(file_conf)      #Création d'une nouvelle section portant le nom du fichier
            cfg.set(file_conf, 'cloud_cible', str(cloud))   #Création d'une nouvelle clé dans la section qui définie la plateforme cloud choisie
            path_source = input("----------------\nSaisir le chemin absolu du repertoire à sauvegarder (ex : /usr/local/bin/mondossier) : ")

                #    path_tmp = input("Saisir le chemin absolu du repertoire temporaire pour les archives de sauvegardes qui seront uploadées (ex : /tmp/) : ")
                #    data_tmp_cut = input("Saisir la taille maximum en Mo de chaque archive (défaut = 50 Mo) : ")
                #    data_tmp_del = input("Souhaitez-vous que les archives de backup soient supprimées après l'upload (O/N): ")

        while True:     #boucle tant que la saisie n'est pas nulle ou un nombre entier positif
            bkp_rotate = input("----------------\nNombre d'anciennes sauvegardes à conserver en ligne (défaut=2) (aide:help): ")
            if bkp_rotate== "help":    #si saisie = help, affiche des explications
                print("\n    - Saisir un nombre entier >=0 \n    - La dernière sauvegarde uploadée est comptée en + de ce nombre")
                print("    - Exemple : nombre saisi ='2' \n                --> Il restera toujours 2 sauvegardes en + de la dernière uploadée, soit 3 au total.\n")
            elif not bkp_rotate:       #si la saisie est vide, on applique la valeur par défaut annoncée
                bkp_rotate = 2
                print("----------------\nNombre par défaut appliqué : "+ str(bkp_rotate))
                total = (int(bkp_rotate)+1)         #incrémente le nombre de sauvegardes à conserver de +1 pour obtenir le total de sauvegardes en ligne avec la dernière uploadée
                print("Nombre total de sauvegardes stockées en ligne : "+ str(total))
                break
            elif (bkp_rotate.isdigit()):    #si la saisie est bien un nombre entier positif
                total = (int(bkp_rotate)+1)
                print("Nombre total maximum de sauvegardes stockées en ligne : "+ str(total))
                break

        cfg.set(file_conf, 'path_source', str(path_source)) #Création d'une nouvelle clé dans la section qui définie la source locale à sauvegarder
        cfg.set(file_conf, 'bkp_rotate', str(bkp_rotate))   #Création d'une nouvelle clé dans la section qui définie le nombre de sauvegardes à conserver en ligne
        cfg.write(open(file_path,'w'))                      #Saisie les entrées précédantes dans le fichier.cfg
        cloud_create_conf = 'create_' + cloud.lower()       #Construction d'une variable selon le nom de la plateforme de cloud choisie
        eval("package."+ cloud +".sdk_"+ cloud.lower() +"."+ cloud_create_conf + '(file_conf)') ##Appel la fonction définie dans les packages selon la variable établie
        break                                                                                   ##en lui passant l'argument file_conf qui correspond au fichier.cfg en cours
        


#Fonction d'éxécution d'un plan de sauvegarde existant
def execution ():
    enablePrint()
    input("Veuillez choisir un plan de sauvegarde à executer [Lecture liste plans de sauvegarde] : ")


#Fonction de restauration d'un plan de sauvegarde existant
def restauration ():
    input("Veuillez choisir un plan de sauvegarde à restaurer [Lecture liste plans de sauvegarde] : ")


#Fonction "lancement" qui s'appuie sur les arguments saisis ou les demande si absent et appel les fonctions associées
def lancement(mode):
    
    while args.action == None or args.action != "create" or args.action != "save" or args.action != "restore":
        if args.action != None:
            args.action = ''.join(args.action)
        if args.action != None and args.action == "create":
            print("----------------\nCréation d'un plan de sauvegarde")
            creation()
            break
        elif args.action != None and args.action == "save": 
            print("----------------\nExécution d'un plan de sauvegarde")
            execution()
            break
        elif args.action != None and args.action == "restore":
            print("----------------\nRestauration d'un plan de sauvegarde")
            restauration()
            break
        elif args.action != None and args.action == "quit":
            print("----------------\nFermeture du script.")
            break
        else: #Force le mode verbeux et demande de faire un choix si aucun argument valide n'a été passé
            enablePrint()
            args.action = input("----------------\nQuelle action souhaitez-vous faire ? [create | save | restore | quit] : ")


#Appel de la fonction "lancement" en mode verbeux par défaut ou en mode quiet si précisé
if args.quiet:
    lancement(blockPrint())
elif args.verbose or (args.quiet is False and args.verbose is False):
    lancement(enablePrint())