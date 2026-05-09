import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from ..core import identification as IDTXT

# On charge la base de données au lancement de l'UI
BASE_DONNEE = IDTXT.extraction(
    os.path.join(os.path.dirname(__file__), "..", "core", "compte_crypte.txt")
)
NB_ESSAIS = 0


def identification_mainloop():
    # variable local mais pas local
    identifiant_valide = None
    cle_user_valide = None
    nom_decrypt_valide = None

    def se_connecter():
        global NB_ESSAIS
        nonlocal identifiant_valide, cle_user_valide, nom_decrypt_valide
        identifiant = entry_id.get()  # c'est  le compte de Nima '23456789'
        mdp = entry_mdp_var.get()  #'000000'

        if not IDTXT.validation_typo(identifiant, 8):
            messagebox.showwarning("Erreur ID", "L'ID doit contenir 8 chiffres.")
            return

        if not IDTXT.validation_typo(mdp, 6):
            messagebox.showwarning("Erreur MDP", "Le MDP doit contenir 6 chiffres.")
            return

        if IDTXT.verification_id_utilisateur(identifiant, BASE_DONNEE):
            valide, cle_user, nom_decrypt = IDTXT.verification_mdp_utilisateur(
                identifiant, mdp, BASE_DONNEE
            )

            if valide:
                messagebox.showinfo(
                    "Succès", f"Connexion réussie ! Bienvenue {nom_decrypt} !"
                )
                identifiant_valide = identifiant
                cle_user_valide = cle_user
                nom_decrypt_valide = nom_decrypt
                identification_fenetre.withdraw()
                identification_fenetre.quit()
                return
            else:
                NB_ESSAIS += 1
                messagebox.showerror("Erreur", f"MDP incorrect ({NB_ESSAIS}/3)")
        else:
            NB_ESSAIS += 1
            messagebox.showerror("Erreur", f"ID inconnu ({NB_ESSAIS}/3)")

        if NB_ESSAIS >= 3:
            messagebox.showerror("Bloqué", "Trop de tentatives. Fermeture.")
            identification_fenetre.destroy()
            identification_fenetre.quit()

    def ajouter_chiffre(chiffre):
        nouveau_mdp = entry_mdp_var.get() + str(chiffre)
        entry_mdp_var.set(nouveau_mdp)

    def enlever_chiffre():
        nouveau_mdp = entry_mdp_var.get()[:-1]
        entry_mdp_var.set(nouveau_mdp)

    def montrer_mdp():
        if entry_mdp.cget("show") == "*":
            entry_mdp.config(show="")
        else:
            entry_mdp.config(show="*")

    identification_fenetre = tk.Tk()
    identification_fenetre.title("Banque - Connexion")
    identification_fenetre.geometry("1000x800")

    identification_fenetre.tk.call("tk", "scaling", 2.0)

    style = ttk.Style()

    style.configure("Title.TLabel", font=("Arial", 18))

    style.configure("Normal.TLabel", font=("Arial", 13))

    style.configure("Big.TButton", font=("Arial", 12), padding=2, background="white")

    style.configure("Connect.TButton", font=("Arial", 13), padding=4)

    style.configure("Green.TButton", font=("Arial", 12), padding=2, background="green")

    style.configure("Red.TButton", font=("Arial", 12), padding=2, background="red")

    style.configure(
        "Number.TButton",
        background="#d9d9d9",
        foreground="black",
        font=("Arial", 12),
        padding=4,
    )

    ttk.Label(
        identification_fenetre,
        text="Bienvenue sur la page de connexion",
        style="Title.TLabel",
    ).pack(pady=75)

    frm_inputs = ttk.Frame(identification_fenetre)
    frm_inputs.pack(pady=50)

    ttk.Label(frm_inputs, text="ID", style="Normal.TLabel").grid(
        row=0, column=0, padx=10
    )

    entry_id = ttk.Entry(frm_inputs, font=("Arial", 18), width=25)

    entry_id.grid(row=0, column=1, pady=10)

    ttk.Label(frm_inputs, text="MDP", style="Normal.TLabel").grid(
        row=1, column=0, padx=10
    )

    entry_mdp_var = tk.StringVar()

    entry_mdp = ttk.Entry(
        frm_inputs, textvariable=entry_mdp_var, font=("Arial", 18), width=25, show="*"
    )

    entry_mdp.grid(row=1, column=1, pady=10)

    # bloque clavier physique
    entry_mdp.bind("<Key>", lambda e: "break")

    chk_montrer = ttk.Checkbutton(
        identification_fenetre, text="MONTRER MDP", command=montrer_mdp
    )

    chk_montrer.place(in_=entry_mdp, relx=1.0, x=30, rely=0.5, anchor="w")

    # bouton clavier numerique
    frm_num = ttk.Frame(identification_fenetre)
    frm_num.pack(pady=50)

    chiffres = list(range(10))
    random.shuffle(chiffres)

    for row in range(3):
        for col in range(3):
            test = chiffres.pop()

            ttk.Button(
                frm_num,
                text=str(test),
                style="Number.TButton",
                command=lambda c=test: ajouter_chiffre(c),
            ).grid(row=row, column=col, padx=5, pady=5)

    ttk.Button(
        frm_num, text="Entrer", style="Green.TButton", command=se_connecter
    ).grid(row=4, column=0, padx=5, pady=5)

    dernier_chiffre = chiffres.pop()

    ttk.Button(
        frm_num,
        text=str(dernier_chiffre),
        style="Number.TButton",
        command=lambda c=dernier_chiffre: ajouter_chiffre(c),
    ).grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(
        frm_num, text="Effacer", style="Red.TButton", command=enlever_chiffre
    ).grid(row=4, column=2, padx=5, pady=5)

    btn_connect = ttk.Button(
        identification_fenetre,
        text="Connexion",
        style="Connect.TButton",
        command=se_connecter,
    )

    btn_connect.pack(pady=100)

    identification_fenetre.mainloop()

    return (
        identification_fenetre,
        identifiant_valide,
        cle_user_valide,
        nom_decrypt_valide,
    )
