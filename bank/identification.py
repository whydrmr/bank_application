def extraction(dcmt_text):
    '''
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

def verif_id(id_decrypt, dico):
    '''
    rentrée l'identifiant décrypter de l'utilsiateur avec verif de la tipo (ppas de lettre, limitre de lettre etc)
    '''
    for id_crypte, info in dico.items():
        cle = info[2]
        if id_decrypt == decrypter(id_crypte, cle):
            return True
    return False


def verif_mdp(id, mdp):
    '''comme utilsiateur mais avec le mdp
    '''
    pass

def decrypter(a_decrypter, cle):
    '''
    decrypter l'id et le mdp de l'identifiant avec la clé (clé cesar)
    '''
    lettre = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    if type(a_decrypter) is int:
        for elem in str(a_decrypter):
            temp = (int(elem) + int(cle)) % 10
            result += str(temp)
        return result
    else:
        for elem in a_decrypter.lower():
            temp = (lettre.index(elem) + int(cle)) % 26
            result += lettre[temp]
        return result.capitalize()


print(extraction('compte.txt'))


