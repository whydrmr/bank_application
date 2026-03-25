def crypter(texte: str, cle: int) -> str:
    """Crypte une chaîne avec un décalage César.
    Les lettres (majuscules et minuscules) sont cryptées.
    Les chiffres et symboles sont laissés tels quels.
    """
    resultat = ""
    for c in texte:
        if "a" <= c <= "z":
            resultat += chr((ord(c) - ord("a") - cle) % 26 + ord("a"))
        elif "A" <= c <= "Z":
            resultat += chr((ord(c) - ord("A") - cle) % 26 + ord("A"))
        elif "0" <= c <= "9":
            resultat += chr((ord(c) - ord("0") - cle) % 10 + ord("0"))
        else:
            resultat += c  # laisser les symboles intacts
    return resultat


def decrypter(texte: str, cle: int) -> str:
    """Décrypte une chaîne cryptée avec le décalage César."""
    resultat = ""
    for c in texte:
        if "a" <= c <= "z":
            resultat += chr((ord(c) - ord("a") + cle) % 26 + ord("a"))
        elif "A" <= c <= "Z":
            resultat += chr((ord(c) - ord("A") + cle) % 26 + ord("A"))
        elif "0" <= c <= "9":
            resultat += chr((ord(c) - ord("0") + cle) % 10 + ord("0"))
        else:
            resultat += c
    return resultat
