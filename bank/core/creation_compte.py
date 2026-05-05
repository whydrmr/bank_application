import os
from datetime import date
from .crypt import encrypt

def creation_compte(id_user, cle_user, montant):
    """
    Crée le fichier crypté d'un nouvel utilisateur avec un compte par défaut 
    et un dépôt initial correspondant au montant.
    """
    nom_compte = "Compte Principal"
    date_jour = date.today().strftime("%Y/%m/%d")
    
    # Structure des données attendues par gestion_compte.py
    # 1. Création du compte (CPT)
    # 2. Ajout de l'opération initiale (OPE)
    lignes_en_clair = [
        f"CPT*{nom_compte}",
        f"OPE*{date_jour}*Depot initial*{nom_compte}*DEP*{float(montant)}*True*"
    ]
    
    # Chemin vers le dossier users (bank/core/users)
    dossier_users = os.path.join(os.path.dirname(__file__), "users")
    
    # S'assure que le dossier users existe
    os.makedirs(dossier_users, exist_ok=True) 
    
    chemin_fichier = os.path.join(dossier_users, f"{id_user}.txt")
    
    # Écriture du fichier avec cryptage
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        for ligne in lignes_en_clair:
            # On crypte chaque ligne avec la clé de l'utilisateur
            ligne_cryptee = encrypt(ligne, cle_user)
            f.write(ligne_cryptee + "\n")
            
    print(f"Fichier crypté créé avec succès : {chemin_fichier}")
    return chemin_fichier

# --- Exemple d'utilisation (à retirer ou commenter si importé ailleurs) ---
if __name__ == "__main__":
    # Test : Création du compte 99999999 avec la clé 17 et 500€ de solde
    creation_compte("11111111", 24, 1500.0)
