def extraction(dcmt_text):
    '''
        extraction donnée sous forme {id;[mdp, nom, clé]}
    '''
    ID = []
    with open(dcmt_text, 'r') as fichier:
        for lignes in fichier:
            lignes = lignes.strip()
            temp = lignes.split("*")
            ID.append(temp)
        return ID

    pass

def verif_id():
    '''rentrée l'identifiant décrypter de l'utilsiateur avec verif de la tipo (ppas de lettre, limitre de lettre etc)
        '''
    pass

def verif_mdp():
    '''comme utilsiateur mais avec le mdp
        '''
    pass

def decrypter():
    '''decrypter l'id et le mdp de l'identifiant avec la clé (clé cesar)
        '''
    pass

print(extraction("compte.txt"))
