import tkinter as tk
from tkinter import messagebox
import random
import sys
import os

# Ajout du chemin pour trouver le dossier 'core' si besoin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.identification import extraction, validation_typo, verification_id_utilisateur, verification_mdp_utilisateur

# On charge la base de données au lancement de l'UI
BASE_DONNEE = extraction(os.path.join(os.path.dirname(__file__), '..', 'core', 'compte_crypte.txt'))
NB_ESSAIS = 0

def se_connecter():
    
    global NB_ESSAIS
    identifiant = entry_id.get()
    mdp = entry_mdp_var.get()

    if not validation_typo(identifiant, 8):
        messagebox.showwarning("Erreur ID", "L'ID doit contenir 8 chiffres.")
        return
    
    if not validation_typo(mdp, 6):
        messagebox.showwarning("Erreur MDP", "Le MDP doit contenir 6 chiffres.")
        return

    if verification_id_utilisateur(identifiant, BASE_DONNEE):
        valide, cle_user, nom_decrypt = verification_mdp_utilisateur(identifiant, mdp, BASE_DONNEE)
        
        if valide:
            messagebox.showinfo("Succès", f"Connexion réussie ! Bienvenue {nom_decrypt} !")
            identification_fenetre.destroy() 
        else:
            NB_ESSAIS += 1
            messagebox.showerror("Erreur", f"MDP incorrect ({NB_ESSAIS}/3)")
    else:
        NB_ESSAIS += 1
        messagebox.showerror("Erreur", f"ID inconnu ({NB_ESSAIS}/3)")

    if NB_ESSAIS >= 3:
        messagebox.showerror("Bloqué", "Trop de tentatives. Fermeture.")
        identification_fenetre.destroy()

def ajouter_chiffre(chiffre):
    nouveau_mdp = entry_mdp_var.get() + str(chiffre)
    entry_mdp_var.set(nouveau_mdp)
    
def enlever_chiffre():
    nouveau_mdp = entry_mdp_var.get()[:-1]
    entry_mdp_var.set(nouveau_mdp)
    
def montrer_mdp():
    if entry_mdp.cget('show') == '*':
        entry_mdp.config(show='')
    else:
        entry_mdp.config(show='*')



identification_fenetre = tk.Tk()
identification_fenetre.title("Banque - Connexion")
identification_fenetre.geometry("1000x800")
identification_fenetre.configure(bg="white")


tk.Label(identification_fenetre, text="Bienvenue sur la page de connexion", font=("Arial", 30), bg="white").pack(pady=20)

frm_inputs = tk.Frame(identification_fenetre, bg="white")
frm_inputs.pack(pady=14)

tk.Label(frm_inputs, text="ID", font=("Arial", 18), bg="white").grid(row=0, column=0, padx=10)
entry_id = tk.Entry(frm_inputs, font=("Arial", 18), bd=2, relief="solid")
entry_id.grid(row=0, column=1, pady=10)

tk.Label(frm_inputs, text="MDP", font=("Arial", 18), bg="white").grid(row=1, column=0, padx=10)
entry_mdp_var = tk.StringVar()
entry_mdp = tk.Entry(frm_inputs, textvariable=entry_mdp_var, font=("Arial", 18), show="*", bd=2, relief="solid")
entry_mdp.grid(row=1, column=1, pady=10)
entry_mdp.bind("<Key>", lambda e: "break")

chk_montrer = tk.Checkbutton(identification_fenetre, text="MONTRER MDP", font=("Arial", 13), bg="white", command=montrer_mdp)
chk_montrer.place(in_=entry_mdp, relx=1.0, x=15, rely=0.5, anchor="w")

#bouton clavier numerique

frm_num = tk.Frame(identification_fenetre, bg="white")
frm_num.pack(pady=14)

chiffres = list(range(10))
random.shuffle(chiffres)

for row in range(3):
    for col in range(3):
        test = chiffres.pop()
        tk.Button(
            frm_num,
            text=str(test),
            width=10,
            height=5,
            command=lambda c=test: ajouter_chiffre(c)
        ).grid(row=row, column=col)
        
tk.Button(frm_num,
            text="Enter",
            width=10,
            height=5,
            bg="green",
            command=se_connecter
        ).grid(row=4, column=0)

dernier_chiffre = chiffres.pop()
tk.Button(frm_num,
            text=str(dernier_chiffre),
            width=10,
            height=5,
            command=lambda c=dernier_chiffre: ajouter_chiffre(c)
        ).grid(row=4, column=1)

tk.Button(frm_num,
            text="cancel",
            width=10,
            height=5,
            bg="red",
            command=enlever_chiffre 
        ).grid(row=4, column=2)


btn_connect = tk.Button(identification_fenetre, text="connection", font=("Arial", 18), 
                        command=se_connecter, relief="solid", bd=2, padx=20)
btn_connect.pack(pady=20)

identification_fenetre.mainloop()