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
from datetime import datetime, timedelta
try:    # Test d'import des SDK et de la présence du dossier 'package'
    import package.Azure.sdk_azure
except: # Stop le script si manquant avec une explication
    print("Le dossier 'package' contenant les SDK est absent ou il manque des SDK dedans. Veuillez le télécharger depuis GitHub.")
    sys.exit()

##################################################################################
#   Gestion du lancement, de l'aide, et des arguments optionnels et positionnels #

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
path_conf = init_path + "/conf"                         # Ajoute et créé si besoinle sous dossier 'conf' à ce chemin
if not os.path.isdir(path_conf):
    os.makedirs(path_conf)
path_package = init_path + "/package"                   # Ajoute le sous dossier 'package' à ce chemin
path_log = init_path + "/log"                           # Ajoute et créé si besoin le sous dossier 'log' à ce chemin
if not os.path.isdir(path_log) :
    os.makedirs(path_log)
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
    


    while True:
        for i, elt in enumerate(list_cloud):
            print("-----------------\nChoisir '{}' pour utiliser : '{}'.".format(i, elt))  # Enumère la liste avec ses indices pour créer des choix simple à saisir
        choix_user = input("Saisir la plateforme cloud à utiliser (help) : ")                       # Demande faire un choix
                                         
        if choix_user== "help":     # Si saisie = help, affiche des explications
            print("###########################\n|\t    AIDE\n|")
            print("| ~~ Fonctionnement ~~\n|- Saisir un nombre entier (>=0) compris dans les choix proposés.")
            print("|- Chaque nombre correspond à une plateforme de cloud dont le SDK est disponible.\n|")
            print("| ~~ Exemple ~~\n|- Nombre choisi = '0'")
            print("|  --> La plateforme '"+list_cloud[0]+"' sera utilisée.")
            print("###########################")
        elif not choix_user:            # Si la saisie est vide, on boucle
            pass
        elif choix_user.isdigit() and int(choix_user) < len(list_cloud) :    # Si la saisie est bien un nombre entier positif compris dans la 'liste_date'
            print("La plateforme '"+ list_cloud[int(choix_user)] + "' a été choisie comme cible de la sauvegarde.")
            choix_cloud = list_cloud[int(choix_user)]
            break
        else:
            continue


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
        if os.listdir(path_conf):   # Test si il y a des plans existant dans le dossier conf
            
            print("\nListe des plans disponibles :\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")

            while True:             # Boucle pour choisir un plan valide dans la liste
                choix_user = input("Saisir le numéro du plan de sauvegarde à utiliser "+str(list_nb)+" (help) : ")  # Affiche les choix possibles de la liste et propose de l'aide
                if choix_user == "help":                                                                            # Si saisie = help, affiche des explications
                    print("###########################\n|\tAIDE\n|")
                    print("|- Saisir un nombre entier de liste correspondant à un nom de fichier.\n|\t~~ Exemple ~~\n|"+str(dct_conf))
                    print("|- Dans cette liste si le nombre saisi est '1', le fichier selectionné sera '"+str(dct_conf[int(1)])+"'")
                    print("###########################")

                elif not choix_user:                                                                 # Si la saisie est vide, réaffiche les choix possibles
                    print("\n~~~~~~~~~~~~ " + str(dct_conf) + " ~~~~~~~~~~~~\n")
                elif (choix_user.isdigit()):                                                         # Si la saisie est nombre entier positif
                    if int(choix_user) in list_nb:                                                   # Si ce nombre saisi est dans la liste des choix possibles
                        choix_plan = dct_conf[int(choix_user)]                                       # Variable globale 'choix_plan' = valeur de la clé du dico correspondante au choix user
                        print("La fichier "+ choix_plan + " a été choisi.")
                        return choix_plan
                    else:
                        pass
        else: # Si il n'existe pas de plan dans le dossier conf propose d'en créer un nouveau
            print("Aucun plan de sauvegarde trouvé dans le dossier 'conf'.")
            create = input("Souhaitez-vous en créer un nouveau ? (o/n) : ")
            if create == "o" or not create:
                creation()
            else:
                sys.exit()

    

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

        print("Le nom du fichier enregistré dans le dossier './conf' sera : "+ file_conf)

        if file_exists:
            print("Ce nom est déjà utilisé.")
            reuse = input("Voulez-vous le réutiliser, ce plan sera écrasé ? (o/n) : ")
            if reuse == "o" or not reuse:
                pass
            else :
                continue
        
        cfg.add_section(file_conf)                              # Création d'une nouvelle section portant le nom du fichier
        cfg.set(file_conf, 'cloud_cible', str(choix_cloud))     # Création d'une nouvelle clé dans la section qui définie la plateforme cloud choisi
        while True:
            path_source = input("----------------\nSaisir le chemin absolu du repertoire à sauvegarder (help) : ")
            if path_source== "help":     # Si saisie = help, affiche des explications
                print("###########################\n|\t    AIDE\n|")
                print("| ~~ Fonctionnement ~~\n|- Saisir le chemin absolu du dossier racine à sauvegarder.\n|- Le contenu de ce dossier sera sauvegardé de manière récursive.\n|")
                print("| ~~ Exemple ~~\n|- Chemin saisi : '/usr/local/bin'")
                print("|  --> Tous les sous-dossiers et fichiers contenus dans '/usr/local/bin' seront sauvegardés.")
                print("###########################")
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
                        if alerte == "o" or not alerte:
                            break
                        elif alerte == "n":
                            sys.exit()
                    except Exception as ex:
                        print('Exception:')
                        print(ex)
                        with open(path_log+'/0-log-error.txt', 'a') as file:
                            file.write("\n"+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : ERREUR = '"+ex+"'" )
            
        while True:                     # Boucle tant que la saisie n'est pas nulle ou un nombre entier positif
            bkp_rotate = input("----------------\nNombre de jours avant suppression des anciennes sauvegardes (défaut=7 | infini=0) (help): ")
            result = "Les sauvegardes existantes depuis "+ str(bkp_rotate) + " jours et plus seront supprimées à chaque exécution de la sauvegarde."
                             
            if bkp_rotate== "help":     # Si saisie = help, affiche des explications
                print("###########################\n|\t    AIDE\n|")
                print("| ~~ Fonctionnement ~~\n|- Saisir un nombre entier >=0\n|- 0 = ne jamais effacer les sauvegardes\n|- Le calcul se base sur la date au moment de l'éxécution d'une sauvegarde.\n|")
                print("| ~~ Exemple ~~\n|- Nombre choisi = '7'\n|- Une sauvegarde est planifiée tous les jours, à midi :")
                print("|  --> Les sauvegardes en ligne depuis 7 jours et + (à la date d'éxécution) seront supprimées.")
                print("|  --> Ici, il restera donc toujours 7 sauvegardes en ligne dans le contenaire.")
                print("###########################")
            elif not bkp_rotate:            # Si la saisie est vide, on applique la valeur par défaut et on affiche 'result'
                bkp_rotate = 7
                print("----------------\nNombre par défaut appliqué : "+ str(bkp_rotate))
                print("Les sauvegardes existantes depuis 7 jours et plus seront supprimées à chaque exécution de la sauvegarde.")
                break
            elif bkp_rotate.isdigit() and bkp_rotate != "0":    # Si la saisie est bien un nombre entier positif différent de 0, affiche 'result'
                print(result)
                break
            elif bkp_rotate == "0":
                print("Les sauvegardes seront conservées indéfiniment.")
                break
            else:
                continue
        
        while True:                     # Boucle tant que la saisie n'est pas nulle ou un nombre entier positif
            log_rotate = input("----------------\nNombre de mois avant suppression des anciens log (défaut=12 | infini=0) (help): ")
            result = "Les logs existants depuis "+ str(log_rotate) + " mois et plus seront supprimées à chaque exécution de la sauvegarde."
                             
            if log_rotate== "help":     # Si saisie = help, affiche des explications
                print("###########################\n|\t    AIDE\n|")
                print("| ~~ Fonctionnement ~~\n|- Saisir un nombre entier >=0\n|- 0 = ne jamais effacer les logs\n|- 3 fichiers log.txt sont créés par plan de sauvegarde et par mois")
                print("|  --> (1 par opération effectuée sur le cloud (upload/download/del)) \n|")
                print("| ~~ Exemple ~~\n|- Nombre choisi = '12'\n| (On considère que chaque type d'opération est éxécuté au moins 1 fois/mois (up/dl/del))")
                print("|  --> Les logs existants depuis 12 mois et + (à la date d'éxécution d'une save) seront supprimés.")
                print("|  --> Ici, dans 1 an, il restera donc 36 fichiers de logs pour ce plan (12 fichiers pour chacune des 3 opérations (up/dl/del)).")
                print("###########################")
            elif not log_rotate:            # Si la saisie est vide, on applique la valeur par défaut 
                log_rotate = 12
                print("----------------\nNombre par défaut appliqué : "+ str(log_rotate))
                print("Les logs existants depuis 12 mois et plus seront supprimées à chaque exécution de la sauvegarde.")
                break
            elif log_rotate.isdigit() and log_rotate != "0":    # Si la saisie est bien un nombre entier positif différent de 0, affiche 'result'
                print(result)
                break
            elif log_rotate == "0":
                print("Les logs seront conservées indéfiniment.")
                break
            else:
                continue

        cfg.set(file_conf, 'path_source', str(path_source))         # Création d'une clé dans la section qui définie la source locale à sauvegarder
        cfg.set(file_conf, 'bkp_rotate', str(bkp_rotate))           # Création d'une clé dans la section qui définie le nombre de sauvegardes à conserver en ligne
        cfg.set(file_conf, 'log_rotate', str(log_rotate))           # Création d'une clé dans la section qui définie le nombre de logs à conserver
        cfg.write(open(file_path,'w'))                              # Saisie les entrées précédantes dans le fichier.cfg
        cloud_create_conf = 'create_' + choix_cloud.lower()         # Construction d'une variable selon le nom de la plateforme de cloud choisie
        
        # Appel la fonction définie dans les packages selon les choix établis
        eval("package."+ choix_cloud +".sdk_"+ choix_cloud.lower() +"."+ cloud_create_conf + '(file_conf, path_conf, path_log)')
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
    global path_log
    choix_plan = choix_user

    # Utilise la fonction 'listing_plan' pour valider le choix saisi en paramètre ou le corriger
    listing_plan()
    
    # Construction du chemin absolu du fichier de conf à utiliser selon le retour de 'choix_plan' de la fonction 'listing_plan'
    file_path = os.path.join(path_conf, choix_plan)

    # Ouverture du fichier et inscription en variables des données à utiliser
    cfg.read(file_path)
    cloud_cible = cfg.get(choix_plan, 'cloud_cible')
    log_rotate = cfg.get(choix_plan, 'log_rotate')
    list_log = os.listdir(path_log)                  # Créé une liste selon les fichiers contenus dans le dossier 'log'
    fonction_save = "save_"+ cloud_cible.lower()     # Variable pour la construction d'appel de la fonction

    MonthInDay = (int(log_rotate)*(365/12))          # Conversion des mois de 'log_rotate' en jours
    
    for files in list_log:                           # Pour chaque fichiers log de la liste
        if files.startswith(choix_plan[0:-4]):                          # Si le fichier commence par le nom du plan
            recup_date = files[-11:].replace('.txt', '')                # Récupère la date du fichier de log
            convert_recup_date = datetime.strptime(recup_date, '%Y.%m') # Convertit la date d'upload (str) en vrai date
            delta = datetime.now() - convert_recup_date                 # Calcul le delta entre la date actuelle et la date du fichier
            if delta.days >= int(MonthInDay) and int(log_rotate) != 0:  # Si le nombre de jours du delta est supérieur ou = au nombre de jours définis et que =! 0 (pour conservation infini)
                os.remove(path_log+"/"+files)
    
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
                        with open(path_log+'/0-log-error.txt', 'a') as file:
                            file.write("\n"+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : Erreur = 'Argument --plan (-p) invalide, la cible n'existe pas. Fermeture du script.'" )
                        break
                    else: 
                        execution(choix_plan)
                        break
            else:
                if args.quiet is True or args.quiet is False:   # Sinon quelque soit l'état de quiet et que l'argument --plan est absent, on force le print + message dans les log pour les Cron
                    enablePrint()
                    print("ERREUR = 'Argument --plan (-p) invalide.'")
                    with open(path_log+'/0-log-error.txt', 'a') as file:
                        file.write("\n"+datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')+" : ERREUR = ' Mode Quiet activé + Argument --plan (-p) absent/invalide. \n\t\t\t\tLe script passe en mode verbose auto pour continuer une éxécution manuelle. \n\t\t\t\tSi l'éxécution provient d'une tâche planifiée, celle-ci ne s'est pas éxécutée correctement.'" )
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