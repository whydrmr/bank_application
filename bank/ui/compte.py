from tkinter import *

def addcompte(fenetre_principale):
    fencompte = Toplevel(fenetre_principale)
    fencompte.title("Ajouter un compte")
    fencompte.geometry("500x300")

    Label(fencompte, text="Ajouter un compte", font=("", 18)).pack(pady=20)

    fmcompte = Frame(fencompte)
    fmcompte.pack(pady=20)

    # Nom compte
    fmnom = Frame(fmcompte)
    fmnom.pack(anchor=W, pady=10)
    Label(fmnom, text="Nom du compte :", font=("", 16), width=15, anchor=W).pack(side=LEFT)
    Entry(fmnom, font=("", 14), width=20).pack(side=LEFT)

    # Solde initial
    fmsolde = Frame(fmcompte)
    fmsolde.pack(anchor=W, pady=10)
    Label(fmsolde, text="Solde initial :", font=("", 16), width=15, anchor=W).pack(side=LEFT)
    Entry(fmsolde, font=("", 14), width=20).pack(side=LEFT)

    # Boutons
    fmbouton = Frame(fencompte)
    fmbouton.pack(pady=20)

    Button(
        fmbouton,
        text="Annuler",
        command=fencompte.destroy
    ).pack(side=LEFT, padx=10)

    Button(
        fmbouton,
        text="Ajouter"
    ).pack(side=LEFT, padx=10)