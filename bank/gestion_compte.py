import os
from datetime import date, datetime


def charger_donnees(info_comptes):
    """
    ________________________________________

    Charge les donnes de tout les comptes.

    str-->dictxdict
    ________________________________________

    """

    base_de_donnees = {}
    base_de_budgets = {}

    for fichier in os.listdir(info_comptes):
        if not fichier.endswith(".txt"):
            continue

        user_id = fichier.replace(".txt", "")

        base_de_donnees[user_id] = {}
        base_de_budgets[user_id] = {}
        correspondance_comptes = {}

        chemin = os.path.join(info_comptes, fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue

                elements = ligne.split("*")
                tag = elements[0].strip()

                if tag == "CPT":
                    nom_compte = elements[1].strip()
                    cle_compte = nom_compte.lower().replace(" ", "_")

                    correspondance_comptes[nom_compte] = cle_compte

                    base_de_donnees[user_id].setdefault(cle_compte, [])
                    base_de_budgets[user_id].setdefault(cle_compte, [])

                elif tag == "OPE":
                    date = elements[1].strip()
                    libelle = elements[2].strip()
                    compte = elements[3].strip()
                    type_op = elements[4].strip()
                    montant = float(elements[5])
                    statut = elements[6].strip() == "True"
                    budget = elements[7].strip()

                    cle_compte = compte.lower().replace(" ", "_")
                    base_de_donnees[user_id].setdefault(cle_compte, [])
                    base_de_donnees[user_id][cle_compte].append(
                        [date, libelle, type_op, montant, statut, budget]
                    )

                elif tag == "BUD":
                    libelle_budget = elements[1].strip()
                    montant_max = float(elements[2])
                    compte = elements[3].strip()

                    cle_compte = compte.lower().replace(" ", "_")
                    base_de_budgets[user_id].setdefault(cle_compte, [])
                    base_de_budgets[user_id][cle_compte].append(
                        [libelle_budget, montant_max]
                    )

    return base_de_donnees, base_de_budgets


base_de_donnees, base_de_budgets = charger_donnees("users")


def sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets):
    """
    _____________________________________________________________________

    Sauvegarde les changements dans le fichier texte avec l'id du compte.

    strxdict-->None
    _____________________________________________________________________

    """
    fichier = f"users/{id_compte}.txt"

    with open(fichier, "w", encoding="utf-8") as f:
        for compte, budgets in base_de_budgets[id_compte].items():
            nom_compte = compte.replace("_", " ").title()
            for budget in budgets:
                libelle_budget, montant_max = budget
                f.write(f"BUD*{libelle_budget}*{montant_max}*{nom_compte}\n")

        for compte, operations in base_de_donnees[id_compte].items():
            nom_compte = compte.replace("_", " ").title()
            f.write(f"CPT*{nom_compte}\n")

            for op in operations:
                date, libelle, type_op, montant, statut, budget = op
                f.write(
                    f"OPE*{date}*{libelle}*{nom_compte}*{type_op}*{montant}*{statut}*{budget}\n"
                )


def choisirecompte(base_de_donnees, id):
    """Demande sur quelle compte l'utilisateur veut ajouter la transaction"""
    while True:
        print(
            "Comptes disponibles :",
            ", ".join(k.capitalize() for k in base_de_donnees[id].keys()),
        )
        compt = input("Compte(ex. Compte A) : ").lower().replace(" ", "_")
        if compt not in base_de_donnees[id]:
            reponse = input(
                f"Le compte '{compt}' n'existe pas. Voulez-vous le créer ? (o/n) : "
            ).lower()
            if reponse == "o":
                base_de_donnees[id][compt] = []
                print(f"Compte '{compt}' créé.")
                break
            elif reponse == "n":
                print("Veuillez choisir un compte existant.")
                continue
            else:
                print("Réponse invalide. Merci de répondre par 'o' ou 'n'.")
                continue
        else:
            break

    return compt


def op_vir(base_de_donnees, id_compte):
    """Demande soit operation soit virement"""
    x = int(input("Choisir entre : 1 - operation ; 2 - virement : "))

    if x == 1:  # renvoie la fonction operation
        compt, liste = operation(base_de_donnees, id_compte)
        ajoute_transaction(base_de_donnees, id_compte, compt, liste)
        return base_de_donnees

    elif x == 2:  # renvoie la fonction virement
        compte_1 = choisirecompte(base_de_donnees, id_compte)
        compte_2 = choisirecompte(base_de_donnees, id_compte)
        somme = float(input("Montant : "))

        c1, l1, c2, l2 = virement(base_de_donnees, id_compte, compte_1, compte_2, somme)

        ajoute_transaction(base_de_donnees, id_compte, c1, l1)
        ajoute_transaction(base_de_donnees, id_compte, c2, l2)

    else:
        print("Veuillez choisir entre 1 et 2")


def ajoute_transaction(base_de_donnees, id_compte, compt, liste):
    """
    __________________________________________________________
    Rajoute une transaction.

    dictxstrxstrxlist --> dict
    __________________________________________________________
    """
    base_de_donnees[id_compte][compt].append(liste)
    print("Votre operation a bien etait ajoute.")
    return base_de_donnees


def operation(base_de_donnees, id_compte):
    """Demande a l'utilisateur quelles sont les details
    qu'il veut ajouter a l'operation.Sous la forme:
    [date(str),libelle(str),montant(float),type(str),verification(str ou bool),budget(str)]
    """
    compt = choisirecompte(base_de_donnees, id_compte)
    while True:
        date = input("Date(sous la forme aaaa/mm/jj): ")
        try:
            datetime.strptime(date, "%Y/%m/%d")
            break
        except ValueError:
            print("Date invalide. Format attendu : aaaa/mm/jj (ex: 2026/02/22)")
    libelle = str(input("Libelle: "))

    montant = float(input("Montant: "))

    typ = "CB"  # deja choisie dans la fonction op_tr

    while True:
        verification = input("1 : Verifie ou 2 : Pas encore verifie : ")
        if verification == "1":
            verification = True
            break
        elif verification == "2":
            verification = False
            break
        else:
            print(
                "Verification doit etre : soit - 1 (Verifie), soit - 2 (Pas encore verifie) "
            )

    budget = str(input("Budget: "))
    liste = [date, libelle, typ, montant, verification, budget]
    return compt, liste


def virement(base_de_donnees, id, compte_1, compte_2, somme):
    """
    ___________________________________________________________________________________

    La fonction virement() fait un virement d'une somme d'argent entre les deux comptes.

    dictxstrxstrxstrxfloat --> bool
    ___________________________________________________________________________________

    """
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
    date_str = dat.strftime("%Y/%m/%d")

    liste_1 = [date_str, "virement", "VIR", -somme, verification, " "]
    liste_2 = [date_str, "virement", "VIR", somme, verification, " "]

    return compte_1, liste_1, compte_2, liste_2


if __name__ == "__main__":
    id_compte = input("Quel utilisateur ? (ex: 23456789) : ")
    op_vir(base_de_donnees, id_compte)
    sauvegarder_utilisateur(id_compte, base_de_donnees)

    # Afficher ce qu'on a dans le compte après ajout
    print("\n--- Données mises à jour ---")
    print(base_de_donnees[id_compte])
