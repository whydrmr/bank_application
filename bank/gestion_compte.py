from datetime import date, datetime
# from ident import donnes


def choisirecompte():
    """Demande sur quelle compte l'utilisateur veut ajouter la transaction"""
    x = str(input("compte : "))
    return "compte_" + x


def op_vir(donnes, id_compte):
    """Demande soit operation soit virement"""
    x = int(input("Choisir entre : 1 - operation ; 2 - virement : "))

    if x == 1:  # renvoie la fonction operation
        compt, liste = operation(donnes, id_compte)
        ajoute_transaction(donnes, id_compte, compt, liste)
        return donnes

    elif x == 2:  # renvoie la fonction virement
        compte_1 = choisirecompte()
        compte_2 = choisirecompte()
        somme = float(input("Montant : "))

        c1, l1, c2, l2 = virement(donnes, id_compte, compte_1, compte_2, somme)

        ajoute_transaction(donnes, id_compte, c1, l1)
        ajoute_transaction(donnes, id_compte, c2, l2)

    else:
        print("Veuillez choisir entre 1 et 2")


def ajoute_transaction(donnes, id_compte, compt, liste):
    """
    __________________________________________________________
    Rajoute une transaction.

    dictxstrxstrxlist --> dict
    __________________________________________________________
    """
    donnes[id_compte][compt].append(liste)
    print("Votre operation a bien etait ajoute.")
    return donnes


def operation(donnes, id_compte):
    """Demande a l'utilisateur quelles sont les details
    qu'il veut ajouter a l'operation.Sous la forme:
    [date(str),libelle(str),montant(float),type(str),verification(str ou bool),budget(str)]
    """
    compt = choisirecompte()
    while True:
        date = input("date sous la forme aaaa/mm/jj: ")
        try:
            datetime.strptime(date, "%Y/%m/%d")
            break
        except ValueError:
            print("Date invalide. Format attendu : aaaa/mm/jj (ex: 2026/02/22)")
    libelle = str(input("Libelle: "))

    montant = float(input("Montant: "))

    typ = "CB"  # deja choisie dans la fonction op_tr

    while True:
        verification = input("1 : Verifie ou 2 : Pas encore verifie ")
        if verification == "1":
            verification = True
            break
        elif verification == "2":
            verification = False
            break
        else:
            print("Verification doit etre soit 1 : Verifie ou 2 : Pas encore verifie")

    budget = str(input("Budget: "))
    liste = [date, libelle, montant, typ, verification, budget]
    return compt, liste


def virement(donnes, id, compte_1, compte_2, somme):
    """
    ___________________________________________________________________________________

    La fonction virement() fait un virement d'une somme d'argent entre les deux comptes.

    dictxstrxstrxstrxfloat --> bool
    ___________________________________________________________________________________

    """
    assert id in donnes, "ID inexistant."

    assert compte_1 in donnes[id] and compte_2 in donnes[id], (
        "L'un des comptes n'existe pas."
    )

    assert compte_1 != compte_2, "Les comptes doivent être différentes."

    assert somme > 0, "La somme doit être positive."

    choice = int(
        input("Choisissez le type de virement (1 = instantané / 2 = date future) : ")
    )

    if choice == 1:
        dat = date.today()

    elif choice == 2:
        while True:
            date_str = input("Date sous la forme aaaa/mm/jj : ")
            try:
                dat = datetime.strptime(date_str, "%Y/%m/%d").date()
                break
            except ValueError:
                print("Date invalide. Format attendu : aaaa/mm/jj (ex: 2000/02/20)")

    else:
        print("Choix invalide.")
        return False

    verification = dat <= date.today()
    date_str = dat.strftime("%d/%m/%Y")

    liste_1 = [date_str, "virement", -somme, "VIR", verification, " "]
    liste_2 = [date_str, "virement", somme, "VIR", verification, " "]

    return compte_1, liste_1, compte_2, liste_2


if __name__ == "__main__":
    id_compte = input("Quel utilisateur ? (ex: u001) : ")
    op_vir(donnes, id_compte)

    # Afficher ce qu'on a dans le compte après ajout
    print("\n--- Données mises à jour ---")
    print(donnes[id_compte])
