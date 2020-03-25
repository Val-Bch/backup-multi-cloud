#!/usr/bin/python3
import sys, argparse, os

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


#Fonction de listing des sdk cloud
def listing_cloud():
    print("Liste des services cloud disponibles :" )


#Fonction des plans de sauvegardes existants
def listing_plan():
    print("Liste des services cloud disponibles :" )


#Fonction de création d'un nouveau plan de sauvegarde
def creation():
    input("Veuillez choisir un cloud cible [Lecture liste sdk dispo] :")


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
            print("Création d'un plan de sauvegarde")
            creation()
            break
        elif args.action != None and args.action == "save": 
            print("Exécution d'un plan de sauvegarde")
            execution()
            break
        elif args.action != None and args.action == "restore":
            print("Restauration d'un plan de sauvegarde")
            restauration()
            break
        elif args.action != None and args.action == "quit":
            print("Fermeture du script.")
            break
        else: #Force le mode verbeux et demande de faire un choix si aucun argument valide n'a été passé
            enablePrint()
            args.action = input("Quelle action souhaitez-vous faire ? [create | save | restore | quit] : ")


#Appel de la fonction "lancement" en mode verbeux par défaut ou en mode quiet si précisé
if args.quiet:
    lancement(blockPrint())
elif args.verbose or (args.quiet is False and args.verbose is False):
    lancement(enablePrint())