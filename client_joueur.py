# coding: utf-8
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module client_joueur.py
        Ce module contient le programme principal d'un joueur
        il s'occupe des communications avec le serveur
            - envois des ordres
            - recupération de l'état du jeu
        la fonction mon_IA est celle qui contient la stratégie de
        jeu du joueur.

"""
import argparse
import random
import client
import const
import plateau
import case
import joueur

prec='X'
""" pour : #####
           ..##c
           #.##d
           #A...
         teleportation supp  
         ajouter variable globale avec pos-2, pos-1, pos pour ne pas alterner les cases ?
         pb entre fantome et pacman collision 

"""


def verifie_passemuraile(joueurs, ma_couleur):
    """verifie la valeur du passemuraille d'un pacman

    Args:
        joueurs (dict): dictionnaire de joueurs avec pour cle la couleur et valeurs les infos joueur
        ma_couleur (str): cahine de caracteres representant une couleur d'un pacman

    Returns:
        bool: True si possede passemuraille sinon False
    """
    if joueur.get_duree(joueurs[ma_couleur], '~') > 0: 
        return True
    else: 
        return False


def calcul_points(dico_analyse):
    """calcule le nb de points de l'ensemble des objets d'une direction

    Args:
        dico_analyse (dict): dictionnaire analyse plateau

    Returns:
        int: nb entier representant des points
    """    
    pts = 0
    try: 
        for obj in dico_analyse['objets']:
           pts += const.PROP_OBJET[obj[1]][0]
        return pts
    except:
        return pts

def construit_dico_analyse(directions_possibles, le_plateau, position_pacman, danger):
    """construit un dictionnaire sous la forme {'N':{'objets': [(2, '@')], 'pacmans': [(3, 'D')], 'fantomes': [(3, 'b')], 'S':{'objets': [(2, '@')], 'pacmans': [(3, 'D')], 'fantomes': [(3, 'b')] ...}

    Args:
        directions_possibles (set): ensemble des directions possibles à partir d'une case
        le_plateau (dict): le plateau de jeu
        position_pacman (tuple): position ligne, colonne
        danger (int): distance à parcourir

    Returns:
        dict: dictionnaire avec pour clé les directions NSEO et pour valeurs des dictionnaires avec obj, fantomes, pacmans
    """    
    dico_analyse = {}
    for position in directions_possibles:
        dico_analyse[position] = plateau.analyse_plateau(le_plateau, position_pacman, position, danger)
    return dico_analyse


def set_to_str(un_ensemble):
    chaine = ""
    for lettre in un_ensemble:
        chaine += lettre
    return chaine



def mon_IA(ma_couleur,carac_jeu, plan, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                   de la partie séparées par des ;
             duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet           
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;nb_cases_peintes;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """
    # decodage des informations provenant du serveur
    joueurs={}
    for ligne in les_joueurs.split('\n'):
        lejoueur=joueur.joueur_from_str(ligne)
        joueurs[joueur.get_couleur(lejoueur)]=lejoueur

    le_plateau=plateau.Plateau(plan)

    # IA complètement aléatoire
    # on met en place l'ensemble des variables
    objets_pacman = const.PROP_OBJET
    position_pacman = joueur.get_pos_pacman(joueurs[ma_couleur])
    position_fantome = joueur.get_pos_fantome(joueurs[ma_couleur])
    fantome_distance = plateau.get_nb_colonnes(le_plateau)-1
    danger = 5
    objets_distance = 20
    max_objet = (5, ".")

    passemuraille = verifie_passemuraile(joueurs, ma_couleur)

    pos_possibles_pacman = plateau.directions_possibles(le_plateau, position_pacman, passemuraille) # directions possibles pour la position actuelle de pacman

    dico_pos_pacman = construit_dico_analyse(pos_possibles_pacman, le_plateau, position_pacman, danger) # on définit le dico pacman pour le danger et fantome
    dico_pos_pacman_obj = construit_dico_analyse(pos_possibles_pacman, le_plateau, position_pacman, objets_distance) # dico pour les objets avec une plus grande distance
    dir_pacman_e = plateau.directions_possibles(le_plateau, position_pacman, passemuraille)
    dir_pacman_s = set_to_str(dir_pacman_e)
    future_direction_pacman = random.choice("NESO")

    pos_possibles_fantome = plateau.directions_possibles(le_plateau, position_fantome)
    dico_pos_fantome = construit_dico_analyse(pos_possibles_fantome, le_plateau, position_fantome, fantome_distance) # dico fantome 

    try:
        for direction in dico_pos_pacman: # pour chaque direction dans l'ensemble des directions possibles
            if dico_pos_pacman[direction]['fantomes'][0][1].upper() != ma_couleur and len(dico_pos_pacman[direction]['fantomes']) > 0 and direction in dir_pacman_e:
                dir_pacman_e.remove(direction) # si il y a un fantome dans cette direction autre que le notre et que l'on peut y aller alors on la supprime des directions possibles
    except: # pour éviter le TypeError si analyse plateau a renvoyé None
        None

    if dir_pacman_e == set():
        max_pts = 0 # si que des fantomes 
        for lettre in pos_possibles_pacman:
            if dico_pos_pacman[lettre]['objets'] != [] and objets_pacman[dico_pos_pacman[lettre]['objets'][0][1]][0] > max_pts:
                future_direction_pacman = lettre
                max_pts = objets_pacman[dico_pos_pacman[lettre]['objets'][0][1]][0] # si aucun mur alors on avance vers objet 

    else:
        for direction in dir_pacman_e:
          dir_pacman_s += direction
          future_direction_pacman = random.choice(dir_pacman_s)
    for direction in dico_pos_pacman: # cherche objet
        calcul_pts = calcul_points(dico_pos_pacman_obj[direction]) 
        max_pts = 0
        pts_passemuraille = 0
        
        try: 
            if dico_pos_pacman[direction]['fantomes'][0][1] == ma_couleur and len(dico_pos_pacman[direction]['fantomes']) < 2 and dico_pos_pacman_obj[direction]['objets'] != [] and min(dico_pos_pacman_obj[direction]['objets'])[0] < max_objet[0]: #si pas de fantomes + objets pas loin + objet plus proche que le precedent
                  max_objet = (min(dico_pos_pacman_obj[direction]['objets'])[0], min(dico_pos_pacman_obj[direction]['objets'])[1])
                  future_direction_pacman = direction
            elif dico_pos_pacman[direction]['fantomes'][0][1] == ma_couleur and len(dico_pos_pacman[direction]['fantomes']) < 2 and dico_pos_pacman_obj[direction]['objets'] != [] and min(dico_pos_pacman_obj[direction]['objets'])[0] ==  max_objet[0]: # si distance egale
                if objets_pacman[min(dico_pos_pacman_obj[direction]['objets'])[1]][0] > objets_pacman[max_objet[1]][0]:
                  max_objet = (min(dico_pos_pacman_obj[direction]['objets'])[0], min(dico_pos_pacman_obj[direction]['objets'])[1])
                  future_direction_pacman = direction
            if dico_pos_pacman[direction]['fantomes'][0][1] == ma_couleur and len(dico_pos_pacman[direction]['fantomes']) < 2 and dico_pos_pacman_obj[direction]['objets'] != [] and calcul_pts > max_pts:
                max_pts = calcul_pts
                future_direction_pacman = direction
            if passemuraille: # si il a passemuraille il va vers obj avec le plus de pts
                if dico_pos_pacman_obj[direction]['objets'] != [] and calcul_pts > pts_passemuraille:
                    future_direction_pacman = direction
        except: 
             None
    
    dir_p= future_direction_pacman

    dir_fantome_e = plateau.directions_possibles(le_plateau, position_fantome)
    dir_fantome_s = set_to_str(dir_fantome_e)

    future_position_fantome = random.choice(dir_fantome_s) 
    position_fantome_parcours = future_position_fantome
    distance_avec_fantome = 20
    for direction in dico_pos_fantome: # cherche le pacman le plus proche
        if dico_pos_fantome[direction]['pacmans'] != []: # si liste pas vide
            if dico_pos_fantome[direction]['pacmans'][0][1] != ma_couleur: # on vérifie qu'il n'y a pas que notre pacman
                for pacman in dico_pos_fantome[direction]['pacmans']:
                    if pacman[0] < distance_avec_fantome and "$" not in joueur.get_objets(joueurs[pacman[1]]) and pacman[1] != ma_couleur: # si pacman est le plus proche et n'a pas le glouton
                        distance_avec_fantome = pacman[0]
                        future_position_fantome = direction
                    elif pacman[0] < distance_avec_fantome and "$" in joueur.get_objets(joueurs[pacman[1]]): # si il a le glouton on doit l'éviter
                        dir_fantome_e.remove(direction)
                        continue
                    
    if dir_fantome_e != plateau.directions_possibles(le_plateau, position_fantome) and position_fantome_parcours == future_position_fantome: # si l'ensemble des directions a été modif + la position avant parcours est la même
        if dir_fantome_e != set(): # on verifie que l'ensemble n'est pas vide puis on choisit une position au hasard puisqu'aucun pacman à l'horizon sauf glouton 
            dir_fantome_s = set_to_str(dir_fantome_e)
            future_position_fantome = random.choice(dir_fantome_s)

    dir_f=  future_position_fantome

    return dir_p+dir_f          

if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            carac_jeu,le_plateau,les_joueurs=le_jeu.split("--------------------\n")
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")
