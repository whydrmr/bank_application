GLOBAL_KEY = 21

def extraction(dcmt_text):
    """str -> dict
    extraction donnée sous forme {id;[mdp, nom, clé]}
    """
    dico = {}
    with open(dcmt_text, "r") as fichier:
        for lignes in fichier:
            lignes = lignes.strip()
            temp = lignes.split("*")
            identifiant = temp[0]
            infos = temp[1:]
            dico[identifiant] = infos
    return dico

def validation_typo(element, taille):
    '''str x int -> bool
    verifie la typo de chaque input pour le mdp et l'id
    '''
    if not element.isdigit():
        print("Que des chiffres svp")
        return False  # continue va retourne au debout de la boucle While en skippant tout le reste du code

    if len(element) != taille:
        print("Taille chaine de caractere incorrecte")
        return False

    return True


def decrypter(a_decrypter, cle):
    """str x int -> str
    decrypter l'id et le mdp de l'identifiant avec la clé (clé cesar)
    """
    result = ""
    cle = int(cle)    # Si c un nombre (id)
    if a_decrypter.isdigit():  # on va traiter que des str ducoup c'est une methode pour verifier que c bien des chiffres
        for elem in a_decrypter:
            result += chr((ord(elem) - ord('0') + cle) % 10 + ord('0'))
        return result

    # sinon c du texte (mdp)
    else:
        for elem in a_decrypter.lower():
            if 'a' <= elem <= 'z':
                result += chr((ord(elem) - ord('a') + cle) % 26 + ord('a'))
        return result.capitalize()



def verif_id(id_decrypt, dico):
    """str x dict -> Bool
    rentrée l'identifiant décrypter de l'utilsiateur avec verif de la tipo (ppas de lettre, limitre de lettre etc)
    """
    for id_crypte, info in dico.items():
        cle_user = decrypter(info[2], GLOBAL_KEY)
        cle = int(cle_user) + GLOBAL_KEY
        if id_decrypt == decrypter(id_crypte, cle):
            return True
    return False


def verif_mdp(id_saisi, mdp_saisi, dico):
    """str x str x dict -> Bool
    Vérifie si le mdp saisi correspond au mdp stocké après décryptage
    pour l'identifiant.
    """
    for id_crypte, info in dico.items():
        cle_user = decrypter(info[2], GLOBAL_KEY)
        cle = int(cle_user) + GLOBAL_KEY
        if id_saisi == decrypter(id_crypte, cle):
            mdp_decrypt_stocke = decrypter(info[0], cle)
            if mdp_saisi == mdp_decrypt_stocke:
                nom_decrypt = decrypter(info[1], cle)
                print(f" ---------- MDP valide, bienvenue {nom_decrypt}! ----------")
                return True
    return False


if __name__ == "__main__":
    dico = extraction("compte_crypte.txt")
    i = 0
    continuation_1 = True
    print("+++++++++++++ Bienvenue dans la BANQUE +++++++++++++")
    while continuation_1:
        continuation_2 = True
        identifiant = input("Veuillez entrer votre ID : ")
        if not validation_typo(identifiant, 8):
            continue
        if verif_id(identifiant, dico):  # si l'utilisateur est trv, on verif son mdp MAIS ON A PAS RECUP LES INFOS DIRECT.. il faut retourner les chercher
            print("---------- ID valide ----------")
            i = 0
            while continuation_2:
                mdp = input("Veuillez entrer votre MDP : ")
                if not validation_typo(mdp, 6):
                    continue
                if verif_mdp(identifiant, mdp, dico): 
                    continuation_1 = False
                    continuation_2 = False
                else:
                    print("MDP incorrect")
                    i += 1
                    if i > 3:
                        print("Trop d'essaies pour le mdp")
                        continuation_2 = False
        else:
            print("ID incorrect")
            i += 1
            if i > 3:
                print("Trop d'essaies...")
                continuation_1 = False
    print("---------- Fermeture de la page de connexion.. ----------")
