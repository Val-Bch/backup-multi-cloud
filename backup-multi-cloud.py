#!/usr/bin/python3
# -*- coding: utf-8 -*-

###########################################
#   Programme Python                      #
#   Auteur : Valentin Boucher             #
#   Licence : Gnu GPL3                    #
###########################################

###########################################
#   Importation des fonctions externes :  #
import sys, argparse, os, configparser
import package.Azure.sdk_azure
import package.AWS.sdk_aws

##################################################################################
#   Gestion du lancement, de l'aide, et des arguments optionnels et positionnels #

#syslog.syslog('Processing started')
parser = argparse.ArgumentParser(description="Sauvegarde/restauration multi Cloud")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-a", "--action", nargs='+', help="Choisir une action : create | restore | save")
parser.add_argument("-p", "--plan", nargs='+', help="Indiquer le nom du fichier.cfg a lire.")
args = parser.parse_args()

#################################################################
#   Fonction d'activation/desactivation du mode verbeux         #
def enablePrint():
    """Fontion a appeler pour activer l'affichage (verbose)."""
    sys.stdout = sys.__stdout__

def blockPrint():
    """Fontion a appeler pour désactiver l'affichage (quiet)."""
    sys.stdout = open(os.devnull, 'w')


########################################
#   Déclaration des variables gobales  #
init_path = os.path.abspath(os.path.dirname( __file__)) # Récupère le chemin absolu du script
path_conf = init_path + "/conf"                         # Ajoute le sous dossier conf à ce chemin
path_package = init_path + "/package"                   # Ajoute le sous dossier package à ce chemin
path_log = init_path + "/log"                   # Ajoute le sous dossier package à ce chemin
list_conf = os.listdir(path_conf)                       # Liste les fichiers .cfg du dossier "conf"
cfg = configparser.ConfigParser()
choix_cloud = ""
file_path = ""
plan = ""
choix_plan = ""


###############################################
#   Fonctions générales du script principal   #
def listing_cloud():
    """
    Fonction de listing des dossiers présent dans './package' et qui représentent la liste des plateformes Cloud disponibles.
    """
    global choix_cloud

    enablePrint()                           # Active de force le mode verbeux
    list_cloud = os.listdir(path_package)   # Liste les sous-dossiers du dossier "package" qui sont nommés selon les plateformes cloud
    
    print("----------------\nListe des services cloud disponibles : " + str(list_cloud))  # Affiche la liste des cloud dispo
    choix_cloud = input("Saisir la plateforme cloud à utiliser : ")                       # Demande faire un choix

    while True:                         # Boucle pour choisir une plateforme valide dans la liste
        if choix_cloud in list_cloud:   # Si la saisie correspond à une entrée de la liste des packages cloud dispo
            print("La plateforme "+ choix_cloud + " a été choisie comme cible de la sauvegarde.")
            break
        else:                           # Sinon réaffiche la liste et précise la sensibilité à la casse
            choix_cloud = input("Saisir la plateforme cloud à utiliser (sensible à la casse)" + str(list_cloud) +" : ")



def listing_plan():
    """
    Fonction pour lister les plans de sauvegardes existants dans le dossier './conf).
    """
    global plan
    global choix_plan

    list_nb = list(range(1, len(list_conf)+1))      # Liste qui incrémente chaque item de +1 jusqu'au nombre d'éléments présents dans "list_conf" (+1 pour inclure le dernier dans le range) 
    cles, vals = list_nb, list_conf                 # Identifie les clés et valeurs du dictionnaire selon les 2 listes précédantes
    dct_conf = {a:b for a, b in zip(cles, vals)}    # Dictionnaire qui assemble les 2 listes pour donner des numéros au noms de fichier.cfg et faciliter la saisie

    if choix_plan in vals:      # Si la valeur de choix_plan est dans la liste 'vals'
        return choix_plan       # Le plan choisi est valide et on retourne la variable globale 'choix_plan'
    else:                       # Sinon on propose la liste des plans dispos et on demande de faire un choix
        print("\nListe des plans disponibles :\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")

        while True:             # Boucle pour choisir un plan valide dans la liste
            choix_user = input("Saisir le numéro du plan de sauvegarde à utiliser "+str(list_nb)+" (help) : ")  # Affiche les choix possibles de la liste et propose de l'aide
            if choix_user == "help":                                                                            # Si saisie = help, affiche des explications
                print("     ###########################\n                 AIDE\n     ###########################\n")
                print(" - Saisir un nombre entier de liste correspondant à un nom de fichier :\n    Exemple : "+str(dct_conf))
                print("    Dans cette liste si le nombre saisi est '1', le fichier selectionné sera '"+str(dct_conf[int(1)])+"'\n")

            elif not choix_user:                                                                 # Si la saisie est vide, réaffiche les choix possibles
                print("\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")
            elif (choix_user.isdigit()):                                                         # Si la saisie est nombre entier positif
                if int(choix_user) in list_nb:                                                   # Si ce nombre saisi est dans la liste des choix possibles
                    choix_plan = dct_conf[int(choix_user)]                                       # Variable globale 'choix_plan' = valeur de la clé du dico correspondante au choix user
                    print("La fichier "+ choix_plan + " a été choisi.")
                    return choix_plan
                else:
                    pass
    

def creation():
    """
    Fonction pour assister à la création d'un nouveau plan de sauvegarde.
    """
    global file_path

    listing_cloud()     # Appel de la fontion pour lister les plateformes cloud disponible
    
    while True:         # Boucle pour la construction du fichier de conf .cfg
        plan_name = input("----------------\nDonner un nom/numéro unique à votre plan : ")

        file_conf = "Plan-" + str(choix_cloud) +"-"+ str(plan_name)+".cfg"    # Construction du nom du fichier.cfg
        file_path = os.path.join(path_conf, file_conf)                        # Contruction du chemin absolu pour mener au fichier .cfg
        file_exists = os.path.isfile(file_path)                               # Variable de test sur l'existence d'un fichier homonyme dans le dossier ./conf

        print("Le nom du fichier .cfg enregistré dans le dossier './conf' sera : "+ file_conf)

        if file_exists:
            print("Ce nom est déjà utilisé.")
            continue
        else:
            cfg.add_section(file_conf)                              # Création d'une nouvelle section portant le nom du fichier
            cfg.set(file_conf, 'cloud_cible', str(choix_cloud))     # Création d'une nouvelle clé dans la section qui définie la plateforme cloud choisi
            while True:
                path_source = input("----------------\nSaisir le chemin absolu du repertoire à sauvegarder (help) : ")
                if path_source== "help":     # Si saisie = help, affiche des explications
                    print("###########################\n\t    AIDE\n###########################\n")
                    print("~~ Fonctionnement ~~\n- Saisir le chemin absolu du dossier racine à sauvegarder.\n- Le contenu de ce dossier sera sauvegardé de manière récursive. \n")
                    print("~~ Exemple ~~\n  - Chemin saisi : '/usr/local/bin'")
                    print("\t--> Tous les sous-dossiers et fichiers contenus dans '/usr/local/bin' seront sauvegardés.")
                elif not path_source:            # Si la saisie est vide, on applique la valeur par défaut et on affiche 'result'
                    print("Merci de saisir un chemin, la réponse ne peut-être vide.")
                else:
                    if os.path.isdir(path_source):
                        print("Tout le contenu de '"+path_source+"' sera sauvegardé.")
                        break
                    else: 
                        print("!! Attention, ce repertoire semble ne pas exister, si vous continuez, merci de le créer avant de lancer une sauvegarde.")
                        try: 
                            alerte = input("Continuer ? (o/n) : ")
                            if alerte == "o":
                                break
                            elif alerte == "n":
                                sys.exit()
                        except Exception as ex:
                            print('Exception:')
                            print(ex)
            
            while True:                     # Boucle tant que la saisie n'est pas nulle ou un nombre entier positif
                bkp_rotate = input("----------------\nNombre de jours avant suppression des anciennes sauvegardes (défaut=7 | infini=0) (help): ")
                result = "Les sauvegardes existantes depuis "+ str(bkp_rotate) + " jours et plus seront supprimées à chaque exécution de la sauvegarde."
                               
                if bkp_rotate== "help":     # Si saisie = help, affiche des explications
                    print("###########################\n\t    AIDE\n###########################\n")
                    print("~~ Fonctionnement ~~\n- Saisir un nombre entier >=0\n- 0 = ne jamais effacer les sauvegardes\n- Le calcul se base sur la date au moment de l'éxécution d'une sauvegarde.\n")
                    print("~~ Exemple ~~\n  - Nombre choisi = '7'\n  - Une sauvegarde est planifiée tous les jours, à midi (Crontab) :")
                    print("\t--> Les sauvegardes existantes depuis 7 jours et + (à la date d'éxécution) seront supprimées.")
                    print("\t--> Ici, il restera donc toujours 7 sauvegardes en ligne dans le contenaire.")
                elif not bkp_rotate:            # Si la saisie est vide, on applique la valeur par défaut et on affiche 'result'
                    bkp_rotate = 7
                    print("----------------\nNombre par défaut appliqué : "+ str(bkp_rotate))
                    print("Les sauvegardes existantes depuis 7 jours et plus seront supprimées à chaque exécution de la sauvegarde.")
                    break
                elif bkp_rotate.isdigit() and bkp_rotate != "0":    # Si la saisie est bien un nombre entier positif différent de 0, affiche 'result'
                    print(result)
                    break
                else:
                    print("Les sauvegardes seront conservées indéfiniment.")
                    break

        cfg.set(file_conf, 'path_source', str(path_source))         # Création d'une clé dans la section qui définie la source locale à sauvegarder
        cfg.set(file_conf, 'bkp_rotate', str(bkp_rotate))           # Création d'une clé dans la section qui définie le nombre de sauvegardes à conserver en ligne
        cfg.write(open(file_path,'w'))                              # Saisie les entrées précédantes dans le fichier.cfg
        cloud_create_conf = 'create_' + choix_cloud.lower()         # Construction d'une variable selon le nom de la plateforme de cloud choisie
        
        # Appel la fonction définie dans les packages selon les choix établis
        eval("package."+ choix_cloud +".sdk_"+ choix_cloud.lower() +"."+ cloud_create_conf + '(file_conf, path_conf)')
        break
        



def execution (choix_user):
    """
    Fonction d'éxécution d'un plan de sauvegarde existant.\n
    Répond à l'argument de lancement '-a save'.
    Utilise le paramètre :
    - choix_user = nom du fichier .cfg défini par l'argument de lancement '-p Plan-x-x.cfg'
    """
    global choix_plan
    global file_path
    global init_path
    choix_plan = choix_user

    # Utilise la fonction 'listing_plan' pour valider le choix saisi en paramètre ou le corriger
    listing_plan()
    
    # Construction du chemin absolu du fichier de conf à utiliser selon le retour de 'choix_plan' de la fonction 'listing_plan'
    file_path = os.path.join(path_conf, choix_plan)

    # Ouverture du fichier et inscription en variables des données à utiliser
    cfg.read(file_path)
    cloud_cible = cfg.get(choix_plan, 'cloud_cible')
    fonction_save = "save_"+ cloud_cible.lower()

    # Construction de l'appel de la fonction 'save_xxx' dans le sdk du cloud utilisé
    eval("package."+ cloud_cible +".sdk_"+ cloud_cible.lower() +"."+ fonction_save + '(file_path, choix_plan, init_path, path_log)')


def restauration (choix_user):
    """
    Fonction de restauration d'un plan de sauvegarde existant.\n
    Répond à l'argument de lancement '-a restore'.
    Utilise le paramètre :
    - choix_user = nom du fichier .cfg défini par l'argument de lancement '-p Plan-x-x.cfg'
    """
    global choix_plan
    global file_path
    global init_path
    choix_plan = choix_user
    #Force l'activation du print
    enablePrint()

    # Utilise la fonction 'listing_plan' pour valider le choix saisi en paramètre ou le corriger
    listing_plan()
    
    # Construction du chemin absolu du fichier de conf à utiliser selon le retour de 'choix_plan' de la fonction 'listing_plan'
    file_path = os.path.join(path_conf, choix_plan)

    # Ouverture du fichier et inscription en variables des données à utiliser
    cfg.read(file_path)
    cloud_cible = cfg.get(choix_plan, 'cloud_cible')
    fonction_restore = "restore_"+ cloud_cible.lower()

    # Construction de l'appel de la fonction 'save_xxx' dans le sdk du cloud utilisé
    eval("package."+ cloud_cible +".sdk_"+ cloud_cible.lower() +"."+ fonction_restore + '(file_path, choix_plan, init_path, path_log)')


def lancement(mode):
    """
    Fonction d'initialisation qui utilise les arguments saisis ou les demande si absent puis appel les fonctions associées.\n
    Utilise les paramètres :\n
    - mode = -v (--verbose) / -q (--quiet)
    """
    global choix_plan
    global list_conf

    # Boucle pour scanner les arguments de lancement et si absent proposer des choix
    while args.action == None or args.action != "create" or args.action != "save" or args.action != "restore":
        if args.action != None:
            args.action = ''.join(args.action)
        if args.action != None and args.action == "create":
            print("----------------\nCréation d'un nouveau plan de sauvegarde.")
            creation()
            break
        elif args.action != None and args.action == "save":     
            if args.plan != None:
                if args.plan[0] in list_conf:                   
                    choix_plan = args.plan[0]
                    print("----------------\nExécution du plan de sauvegarde "+ choix_plan)
                    execution(choix_plan)
                    break
                else:
                    if args.quiet is True:          # Si l'argument quiet a été saisie et que l'argument --plan est invalide, on stop avec un log erreur (adapté au Cron par exemple)
                        enablePrint()
                        print("syslog.syslog(syslog.LOG_ERR, 'Argument --plan (-p) invalide, fermeture du script.')")
                        break
                    else: 
                        execution(choix_plan)
                        break
            else:
                if args.quiet is True or args.quiet is False:          # Sinon quelque soit l'état de quiet et que l'argument --plan est absent, on force le print + message dans les log pour les Cron
                    enablePrint()
                    print("syslog.syslog(syslog.LOG_ERR, 'Argument --plan (-p) invalide.')")
                    execution(choix_plan)
                    break

        elif args.action != None and args.action == "restore":
            if args.plan != None:
                if args.plan[0] in list_conf:                   
                    choix_plan = args.plan[0]
                    print("----------------\nRestauration du plan de sauvegarde '"+ choix_plan+"'\n")
                    restauration(choix_plan)
                    break
                else: 
                        restauration(choix_plan)
                        break

        elif args.action != None and args.action == "quit":
            print("----------------\nFermeture du script.")
            break
        else:               # Force le mode verbeux et demande de faire un choix si aucun argument valide n'a été saisi
            enablePrint()
            args.action = input("----------------\nQuelle action souhaitez-vous faire ? [create | save | restore | quit] : ")


# Appel de la fonction "lancement" en mode verbeux par défaut ou en mode quiet si précisé
if args.quiet:
    lancement(blockPrint())
elif args.verbose or (args.quiet is False and args.verbose is False):
    lancement(enablePrint())