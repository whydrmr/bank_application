def extraction(dcmt_text):
    '''str -> dict
        extraction donnée sous forme {id;[mdp, nom, clé]}
    '''
    dico = {}
    with open(dcmt_text, 'r') as fichier:
        for lignes in fichier:
            lignes = lignes.strip()
            temp = lignes.split("*")
            identifiant = temp[0]
            infos = temp[1:]
            dico[identifiant] = infos
    return dico

def decrypter(a_decrypter, cle):
    '''str x int -> str
    decrypter l'id et le mdp de l'identifiant avec la clé (clé cesar)
    '''
    lettre = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    # Si c un nombre (id)
    if str(a_decrypter).isdigit(): #on va traiter que des str ducoup c'est une methode pour verifier que c bien des chiffres
        for elem in str(a_decrypter):
            temp = (int(elem) + int(cle)) % 10
            result += str(temp)
        return result
    
    # sinon c du texte (mdp)
    else:
        for elem in a_decrypter.lower():
            if elem in lettre:
                temp = (lettre.index(elem) + int(cle)) % 26
                result += lettre[temp]    
        return result.capitalize()


def verif_id(id_decrypt, dico):
    '''str x dict -> Bool
    rentrée l'identifiant décrypter de l'utilsiateur avec verif de la tipo (ppas de lettre, limitre de lettre etc)
    '''
    for id_crypte, info in dico.items():
        cle = info[2]
        if id_decrypt == decrypter(id_crypte, cle):
            return True
    return False


#def verif_mdp(id, mdp):
 #   '''a determiner
  #  comme verif_id mais avec le mdp (on a juste besoin de info (dico.value))
   # '''

def verif_mdp(id_saisi, mdp_saisi, dico):
    '''str x str x dict -> Bool
    Vérifie si le mdp saisi correspond au mdp stocké après décryptage
    pour l'identifiant.
    '''
    for id_crypte, info in dico.items():
        cle = info[2]

        if id_saisi == decrypter(id_crypte, cle):
            mdp_crypte_stocke = info[0]
            mdp_decrypt_stocke = decrypter(mdp_crypte_stocke, cle)
            
            if mdp_saisi == mdp_decrypt_stocke:
                return True
                
    return False


if __name__ == "__main__":
    dico = extraction('compte.txt')
    i = 0
    continuation = True
    while continuation:
        identifiant = input("Veuillez entrer votre ID : ")
        if not identifiant.isdigit():
            print("Que des chiffres svp")
            continue #continue va retourne au debout de la boucle While en skippant tout le reste du code
            
        if len(identifiant) != 8:
            print("Taille chaine de caractere incorrecte")
            continue
        if verif_id(identifiant, dico): #si l'utilisateur est trv, on verif son mdp MAIS ON A PAS RECUP LES INFOS DIRECT.. il faut retourner les chercher
            print("ID valide")
            mdp = input("Veuillez entrer votre mot de passe : ")
            #fonction verif_mdp a faire avec verif caraceter/taille/tentative etc
        else:
            print("ID incorrect")
            i += 1
            if i > 3:
                print("Trop d'essaies... Adieu...")
                continuation = False
    print("Fermeture de la page de connexion.. Au revoir.")


