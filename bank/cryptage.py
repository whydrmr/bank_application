GLOBAL_KEY = 67


def crypter(texte, cle):
    """str x int -> str
    crypte une chaine avec un césar inverse
    compatible avec le programme de décryptage
    """
    result = ""

    # chiffres
    if texte.isdigit():
        for caractere in texte:
            result += chr((ord(caractere) - ord('0') - cle) % 10 + ord('0'))
        return result

    # texte
    else:
        for caractere in texte.lower():
            if 'a' <= caractere <= 'z':
                result += chr((ord(caractere) - ord('a') - cle) % 26 + ord('a'))
        return result


def crypter_fichier(fichier_entree, fichier_sortie):
    with open(fichier_entree, "r") as f:
        lignes = f.readlines()

    with open(fichier_sortie, "w") as f:
        for ligne in lignes:

            ligne = ligne.strip()
            identifiant, mdp, nom, cle = ligne.split("*")

            cle_totale = int(cle) + GLOBAL_KEY

            id_crypte = crypter(identifiant, cle_totale)
            mdp_crypte = crypter(mdp, cle_totale)
            nom_crypte = crypter(nom, cle_totale)
            cle_cryptee = crypter(cle, GLOBAL_KEY)

            f.write(f"{id_crypte}*{mdp_crypte}*{nom_crypte}*{cle_cryptee}\n")


if __name__ == "__main__":
    crypter_fichier("compte.txt", "compte_crypte.txt")
