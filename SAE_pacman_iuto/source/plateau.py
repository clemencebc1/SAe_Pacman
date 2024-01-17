"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import const
import case
import random



def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    return max(plateau)


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    return len(plateau[1])

def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos [1] == 0:
        return (pos[0], get_nb_colonnes(plateau)-1)
    else:
        return (pos[0], pos[1]-1)

def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos [1] == get_nb_colonnes(plateau)-1:
        return (pos[0], 0)
    else:
        return (pos[0], pos[1]+1)

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos [0]+1 == 1:
        return (get_nb_lignes(plateau)-1, pos[1])
    else:
        return (pos[0]-1, pos[1])


def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos [0] == get_nb_lignes(plateau)-1:
        return (0, pos[1])
    else:
        return (pos[0]+1, pos[1])

def pos_arrivee(plateau,pos,direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    if direction == 'N':
        pos = pos_nord(plateau,pos)
    elif direction == 'S':
        pos = pos_sud(plateau,pos)
    elif direction == 'E':
        pos = pos_est(plateau,pos)
    elif direction == 'O':
        pos = pos_ouest(plateau,pos)
    else:
        return None
    return pos

def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    
    return plateau[pos[0]+1][pos[1]]


def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """
    return case.get_objet(plateau[pos[0]+1][pos[1]])

def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_pacman(plateau[pos[0]+1][pos[1]],pacman)

def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_fantome(plateau[pos[0]+1][pos[1]],fantome)

def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_objet(plateau[pos[0]+1][pos[1]],objet)

def plateau_from_str(la_chaine, complet=True):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    fic = la_chaine.split('\n')
    pos = fic[0].split(';')
    pos[0] = int(pos[0])
    pos[1] = int(pos[1])
    fic[0] = pos
    plateau = {}
    for i in range(1, pos[0]+1):
        plateau[i] = []
        for j in range(pos[1]):
            case_plateau = case.Case(False, '.')
            if fic[i][j] == '#':
                case_plateau['mur'] = True
                case_plateau['objet'] = ' '
            elif fic[i][j] == '!':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == ' ':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '~':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '$':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '@':
                case_plateau['objet'] = fic[i][j]
            else:
                case_plateau['objet'] = fic[i][j]
            
            
            
            plateau[i].append(case_plateau)
    for i in range(pos[0]+2, pos[0]+2+int(fic[pos[0]+1])):
        pos_pacman = fic[i].split(';')
        if plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'] == None:
            plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'] = {pos_pacman[0]}
        else:
            plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'].add(pos_pacman[0])
    for i in range(pos[0]+int(fic[pos[0]+1])+3, pos[0]+int(fic[pos[0]+1])+int(fic[pos[0]+1])+3):
        pos_fantome = fic[i].split(';')
        if plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'] == None:
           plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'] = {pos_fantome[0]}
        else:
            plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'].add(pos_fantome[0])
    return plateau


def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir non peint)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """
    fic = plan.split('\n')
    pos = fic[0].split(';')
    pos[0] = int(pos[0])
    pos[1] = int(pos[1])
    fic[0] = pos
    plateau = {}
    for i in range(1, pos[0]+1):
        plateau[i] = []
        for j in range(pos[1]):
            case_plateau = case.Case(False, '.')
            if fic[i][j] == '#':
                case_plateau['mur'] = True
                case_plateau['objet'] = ' '
            elif fic[i][j] == '!':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == ' ':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '~':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '$':
                case_plateau['objet'] = fic[i][j]
            elif fic[i][j] == '@':
                case_plateau['objet'] = fic[i][j]
            else:
                case_plateau['objet'] = fic[i][j]
            
            
            
            plateau[i].append(case_plateau)
    for i in range(pos[0]+2, pos[0]+2+int(fic[pos[0]+1])):
        pos_pacman = fic[i].split(';')
        if plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'] == None:
            plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'] = {pos_pacman[0]}
        else:
            plateau[int(pos_pacman[1])+1][int(pos_pacman[2])]['pacmans_presents'].add(pos_pacman[0])
    for i in range(pos[0]+int(fic[pos[0]+1])+3, pos[0]+int(fic[pos[0]+1])+int(fic[pos[0]+1])+3):
        pos_fantome = fic[i].split(';')
        if plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'] == None:
           plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'] = {pos_fantome[0]}
        else:
            plateau[int(pos_fantome[1])+1][int(pos_fantome[2])]['fantomes_presents'].add(pos_fantome[0])
    return plateau


def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    plateau[[pos[0]+1][pos[1]]] = une_case


def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    total = case.get_nb_pacmans(plateau[pos[0]+1][pos[1]])
    case.prendre_pacman(plateau[pos[0]+1][pos[1]],pacman)
    total_bis = case.get_nb_pacmans(plateau[pos[0]+1][pos[1]])
    if total_bis != total:
        return True
    return False


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    total = case.get_nb_fantomes(plateau[pos[0]+1][pos[1]])
    case.prendre_fantome(plateau[pos[0]+1][pos[1]],fantome)
    total_bis = case.get_nb_fantomes(plateau[pos[0]+1][pos[1]])
    if total_bis != total:
        return True
    return False


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    return case.prendre_objet(plateau[pos[0]+1][pos[1]])

        
def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    arrive = pos_arrivee(plateau,pos,direction)
    if case.est_mur(plateau[arrive[0]+1][arrive[1]]) == False and case.get_nb_pacmans(plateau[pos[0]+1][pos[1]]):
        enlever_pacman(plateau,pacman,pos)
        poser_pacman(plateau,pacman,arrive)
        return arrive
    elif case.est_mur(plateau[arrive[0]+1][arrive[1]]) == True and passemuraille == True and case.get_nb_pacmans(plateau[pos[0]+1][pos[1]]):
        enlever_pacman(plateau,pacman,pos)
        poser_pacman(plateau,pacman,arrive)
        return arrive
    else:
        return None
    

def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    arrive = pos_arrivee(plateau,pos,direction)
    if case.est_mur(plateau[arrive[0]+1][arrive[1]]) == False and case.get_nb_fantomes(plateau[pos[0]+1][pos[1]]):
        enlever_fantome(plateau,fantome,pos)
        poser_fantome(plateau,fantome,arrive)
        return arrive
    return None

def case_vide(plateau):
    """choisi aléatoirement sur la plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    a = False
    while a == False :
        alea1 = random.randint(0, get_nb_colonnes(plateau))
        alea2 = random.randint(0, get_nb_lignes(plateau))
        case1 = [alea2,alea1]
        if case.est_mur(plateau[case1]) == False :
            if case.get_nb_pacmans(plateau[case1]) == 0 :
               if case.get_nb_fantomes(plateau[case1]) == 0 : 
                  if case.get_objet(plateau[case1]) == ' ' :
                    a = True
    return case1


def directions_possibles(plateau,pos,passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    posPossibles = {pos_nord(plateau,pos),
                    pos_est(plateau,pos),
                    pos_ouest(plateau,pos),
                    pos_sud(plateau,pos)}

    res = set()
    
    #On vérifie si c'est accessible
    for position in posPossibles:
        if not case.est_mur(plateau[position[0]+1][position[1]]) or passemuraille:
            if position == pos_nord(plateau,pos):
               res.add("N")
            elif position == pos_est(plateau,pos):
                res.add("E")
            elif position == pos_ouest(plateau,pos):
                res.add("O")
            elif position ==  pos_sud(plateau,pos):
                res.add("S")
    return res
#---------------------------------------------------------#


def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    def add_case_in_res(plateau, res, pos, distance):
        """summary

        Args:
            plateau (dict)): Le plateau considéré
            res (dict): un dictionnaire de listes
            pos (tuple): une paire (lig,col) d'int
            distance (int): une distance
        """

        case_actuelle = get_case(plateau, pos)
        objet = case.get_objet(case_actuelle)

        if objet in const.LES_OBJETS:
            res["objets"].append((distance, objet))

        res["pacmans"] += [(distance, pacman) for pacman in case.get_pacmans(case_actuelle)]
        res["fantomes"] += [(distance, fantome) for fantome in case.get_fantomes(case_actuelle)]


    next_pos = pos_arrivee(plateau, pos, direction)
    if case.est_mur(get_case(plateau, next_pos)):
        return 

    res = {'objets': [], 
           'pacmans': [], 
           'fantomes': []}

    parcourues, next_cases = set(), [(next_pos, 1)]

    while next_cases:
        case_actuelle = min(next_cases, key = lambda cas: cas[1])

        if case_actuelle[1] > distance_max:
            return res

        add_case_in_res(plateau, res, case_actuelle[0], case_actuelle[1])
        parcourues.add(case_actuelle[0])

        for direction in directions_possibles(plateau, case_actuelle[0]):
            next_pos = pos_arrivee(plateau, case_actuelle[0], direction)
            if next_pos not in parcourues:
                next_cases.append((next_pos, case_actuelle[1] + 1))

        next_cases.remove(case_actuelle)

    return res

    



def prochaine_intersection(plateau,pos,direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    
    intersection = lambda pos: len(directions_possibles(plateau, pos)) > 2
    distance = 0
    prochaine_position = pos_arrivee(plateau, pos, direction)

    while not intersection(prochaine_position):
        distance += 1
        prochaine_position = pos_arrivee(plateau, prochaine_position, direction)

        if prochaine_position == pos:
            return -1

    return distance

# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res

