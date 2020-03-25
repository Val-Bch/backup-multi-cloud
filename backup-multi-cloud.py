#!/usr/bin/python3
import sys, argparse, os, configparser
from package import *

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

#Fonction de listing des sdk cloud
def listing_cloud():
    enablePrint()
    list_pack = os.listdir('./package')     #Liste les sous-dossiers du dossier "package" qui sont nommés selon les plateformes cloud
    print("Liste des services cloud disponibles : " + str(list_pack))
    global cloud
    cloud = input("Saisir la plateforme cloud à utiliser : ")
    while True:       #Boucle pour choisir une plateforme valide dans la liste
        if cloud in list_pack:
            print("La plateforme "+ cloud + " a été choisie comme cible de la sauvegarde.")
            break
        else:
            cloud = input("Saisir la plateforme cloud à utiliser (sensible à la casse): ")


#Fonction des plans de sauvegardes existants
def listing_plan():
    print("Liste des services cloud disponibles :" )


#Fonction de création d'un nouveau plan de sauvegarde
def creation():
    listing_cloud() #Appel de la fontion pour lister les plateformes cloud disponible
    dir_conf = "./conf"
    
    while True:
        plan_name = input("Donner un nom/numéro unique à votre plan : ")
        file_conf = "Sauvegarde-" + str(cloud) +"-"+ str(plan_name)+".cfg"
        global file_path
        file_path = os.path.join(dir_conf, file_conf)
        file_exists = os.path.isfile(file_path) 
        if file_exists:
            print("Ce nom est déjà utilisé.")
        else:
            cfg.add_section(file_conf)
            cfg.set(file_conf, 'cloud cible', str(cloud))
            cfg.write(open(file_path,'w'))
            cloud_create_conf = 'create_' + cloud.lower()
            eval(cloud_create_conf + '(file_conf)')
            break


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