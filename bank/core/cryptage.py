SHIFT_CHIFFRE = 3
SHIFT_LETTRE = 11


def crypter_chiffres(texte):
    result = ""

    for caractere in texte:
        result += chr((ord(caractere) - ord("0") + SHIFT_CHIFFRE) % 10 + ord("0"))

    return result


def crypter_texte(texte):
    result = ""

    for caractere in texte.lower():
        if "a" <= caractere <= "z":
            result += chr((ord(caractere) - ord("a") + SHIFT_LETTRE) % 26 + ord("a"))

    return result


def crypter_fichier(fichier_entree, fichier_sortie):
    with open(fichier_entree, "r") as f:
        lignes = f.readlines()

    with open(fichier_sortie, "w") as f:
        for ligne in lignes:
            ligne = ligne.strip()

            identifiant, mdp, nom, cle = ligne.split("*")

            id_crypte = crypter_chiffres(identifiant)
            mdp_crypte = crypter_chiffres(mdp)
            nom_crypte = crypter_texte(nom)
            cle_cryptee = crypter_chiffres(cle)

            f.write(f"{id_crypte}*{mdp_crypte}*{nom_crypte}*{cle_cryptee}\n")


if __name__ == "__main__":
    crypter_fichier("bank/core/compte.txt", "bank/core/compte_crypte.txt")

