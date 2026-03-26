from gestion_compte import charger_donnees, sauvegarder_utilisateur


def filtre(donnes, iD):
    """
    Permet de filtrer les transactions en fonction de la date ou du libelle.

    dictxstr-->list

    """
    while True:
        compte = input("Choisir le compte : ").lower().replace(" ", "_")
        if compte not in donnes[iD]:
            print(f"Compte '{compte}' inexistant.")
        else:
            break

    date = input("Date (aaaa/mm/jj) : ").strip()
    libelle = input("Libelle : ").strip().lower()

    resultat = []
    for transaction in donnes[iD][compte]:
        date_match = date == "" or transaction[0] == date
        libelle_match = libelle == "" or transaction[1].lower() == libelle
        if date_match and libelle_match:
            resultat.append(transaction)

    return resultat


def afficher_budget(base_de_budgets, id):
    """
    Affiche le budget.

    dictxstr-->None

    """
    comptes = base_de_budgets[id]
    for compte, budgets in comptes.items():
        print(f"{compte.replace('_', ' ').title()}")
        if budgets:
            for libelle, montant in budgets:
                print(f"    - {libelle} : {montant}")
        else:
            print("    Aucun budget défini")


def definir_budget(donnees, budgets, id):
    """
    Permet de definir un budget pour un compte particulier.

    dictxstr-->None

    """
    while True:
        print(
            "Comptes disponibles :",
            ", ".join(k.capitalize() for k in donnees[id].keys()),
        )
        compte = input("Choisir le compte : ").lower().replace(" ", "_")
        if compte not in donnees[id]:
            print(f"Compte '{compte}' inexistant.")
        else:
            break

    libelle_budget = input("Nom du budget : ").strip()

    while True:
        try:
            montant_max = float(input("Montant maximal du budget : "))
            break
        except ValueError:
            print("Veuillez entrer un nombre valide pour le montant.")

    budgets[id][compte].append([libelle_budget, montant_max])
    print(
        f"Budget '{libelle_budget}' de {montant_max} ajouté au {compte.capitalize()}."
    )


def main_gestion_budget(id_compte, cle):
    base_de_donnees, base_de_budgets = charger_donnees("users", cle)
    while True:
        print(
            "______________________________________________________________________________"
        )
        print()
        choix = input(
            "| 1 : Afficher le budget \n| 2 : Definir un nouveau budget \n|'r' : revenir en arriere \n"
        )
        print()
        if choix == "1":
            afficher_budget(base_de_budgets, id_compte)
            continue
        elif choix == "2":
            definir_budget(base_de_donnees, base_de_budgets, id_compte)
            continue
        elif choix == "r":
            break
        else:
            print("Input invalide...")
            continue
    sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle)
