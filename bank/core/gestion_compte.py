import os
from datetime import date
from .crypt import encrypt, decrypt


def charger_donnees(dossier_utilisateurs, cle):
    """
    Charge toutes les données depuis des fichiers cryptés.
    """
    cle = int(cle)
    base_de_donnees = {}
    base_de_budgets = {}

    for fichier in os.listdir(dossier_utilisateurs):
        if not fichier.endswith(".txt"):
            continue

        user_id = fichier.replace(".txt", "")
        base_de_donnees[user_id] = {}
        base_de_budgets[user_id] = {}

        chemin = os.path.join(dossier_utilisateurs, fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue

                ligne_decrypte = decrypt(ligne, cle)
                elements = ligne_decrypte.split("*")
                tag = elements[0].strip()

                if tag == "CPT":
                    nom_compte = elements[1].strip()
                    cle_compte = nom_compte.lower().replace(" ", "_")
                    base_de_donnees[user_id].setdefault(cle_compte, [])
                    base_de_budgets[user_id].setdefault(cle_compte, [])

                elif tag == "OPE":
                    date, libelle, compte, type_op, montant, statut, budget = (
                        elements[1].strip(),
                        elements[2].strip(),
                        elements[3].strip(),
                        elements[4].strip(),
                        float(elements[5]),
                        elements[6].strip() == "True",
                        elements[7].strip(),
                    )
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


import os
# (Garde tes autres imports en haut du fichier, notamment encrypt)

def sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle):
    """
    Sauvegarde les changements dans un fichier temporaire d'abord.
    Si tout se passe bien, il remplace le vrai fichier, évitant ainsi toute perte 
    de données en cas de crash pendant l'écriture.
    """
    # 1. Définition des chemins dynamiques et sécurisés
    dossier_users = os.path.join(os.path.dirname(__file__), "users")
    os.makedirs(dossier_users, exist_ok=True) 
    
    fichier_final = os.path.join(dossier_users, f"{id_compte}.txt")
    fichier_temp = os.path.join(dossier_users, f"{id_compte}_temp.txt") # Le fameux fichier temporaire
    
    try:
        # 2. On écrit TOUT dans le fichier temporaire en premier
        with open(fichier_temp, "w", encoding="utf-8") as f:
            
            # Sauvegarde des budgets
            if id_compte in base_de_budgets:
                for compte, budgets in base_de_budgets[id_compte].items():
                    nom_compte = compte.replace("_", " ").title()
                    for budget in budgets:
                        libelle_budget, montant_max = budget
                        ligne = f"BUD*{libelle_budget}*{montant_max}*{nom_compte}"
                        f.write(encrypt(ligne, cle) + "\n")

            # Sauvegarde des comptes et opérations
            if id_compte in base_de_donnees:
                for compte, operations in base_de_donnees[id_compte].items():
                    nom_compte = compte.replace("_", " ").title()
                    ligne_cpt = f"CPT*{nom_compte}"
                    f.write(encrypt(ligne_cpt, cle) + "\n")
                    
                    for op in operations:
                        date_op, libelle, type_op, montant, statut, budget = op
                        ligne_ope = f"OPE*{date_op}*{libelle}*{nom_compte}*{type_op}*{montant}*{statut}*{budget}"
                        f.write(encrypt(ligne_ope, cle) + "\n")
                        
        # 3. LE COUP DE MAGIE : Si on arrive à cette ligne sans crash, 
        # on écrase l'ancien fichier avec le nouveau. C'est instantané et sans risque !
        os.replace(fichier_temp, fichier_final)
        
    except Exception as e:
        print(f"Erreur critique lors de la sauvegarde : {e}")
        # En cas de crash pendant l'écriture, on efface juste le brouillon (le temp)
        # L'ancien fichier reste intact !
        if os.path.exists(fichier_temp):
            os.remove(fichier_temp)


def ajouter_compte(base_de_donnees, base_de_budgets, id_compte, nom_compte):
    cle = nom_compte.lower().replace(" ", "_")
    base_de_donnees[id_compte][cle] = []
    base_de_budgets[id_compte][cle] = []
    return base_de_donnees, base_de_budgets


def operation(base_de_donnees, base_de_budgets, id_compte, compte, data):
    base_de_donnees[id_compte][compte].append(
        [
            data["date"],
            data["libelle"],
            "CB",
            data["montant"],
            "OPT",
            data["budget"],
        ]
    )


    return base_de_donnees, base_de_budgets


def virement(base_de_donnees, id_compte, compte_1, compte_2, somme, date_op):
    verification = date_op <= date.today()
    date_str = date_op.strftime("%Y/%m/%d")

    op1 = [date_str, "Virement", "VIR", -somme, verification, ""]
    op2 = [date_str, "Virement", "VIR", somme, verification, ""]

    base_de_donnees[id_compte][compte_1].append(op1)
    base_de_donnees[id_compte][compte_2].append(op2)

    return base_de_donnees


def validation_montant(montant):
    """input -> bool
    verifie la typo de chaque input pour le mdp et l'id
    """
    valeur = montant.replace(",", ".")

    if valeur in ("", "+", "-"):
        return True
    try:
        float(valeur)
        return True
    except ValueError:
        return False


def main_gestion_compte(id_compte, cle):
    base_de_donnees, base_de_budgets = charger_donnees("bank/core/users", cle)
    sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle)
