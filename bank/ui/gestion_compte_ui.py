from tkinter import *
# Ici on importe les fonctions depuis tes autres fichiers
from virement import virement
from operation import addop
from compte import addcompte

def ouvrir_gestion_compte(fenetre_principale):
    fenetre_gestion_compte = Toplevel(fenetre_principale)
    fenetre_gestion_compte.title("Gestion de compte")
    fenetre_gestion_compte.geometry("500x500")

    Label(fenetre_gestion_compte, text="Gestion de Compte", font=("", 18)).pack(expand=True)

    fmmontant = Frame(fenetre_gestion_compte)
    fmmontant.pack(expand=True)
    lbl_montant = Label(fmmontant, text="Montant : 1500 €", bg="green")
    lbl_montant.pack(anchor=CENTER)

    def action_virement():
        virement(fenetre_gestion_compte)

    def action_ajouter_operation():
        addop(fenetre_gestion_compte)

    def action_ajouter_compte():
        addcompte(fenetre_gestion_compte)

    Button(
        fenetre_gestion_compte,
        text="+ ajouter opération",
        command=action_ajouter_operation
    ).pack(expand=True)

    Button(
        fenetre_gestion_compte,
        text="+ faire virement",
        command=action_virement
    ).pack(expand=True)

    Button(
        fenetre_gestion_compte,
        text="+ ajouter compte",
        command=action_ajouter_compte
    ).pack(expand=True)

    Button(
        fenetre_gestion_compte,
        text="Fermer",
        command=fenetre_gestion_compte.destroy
    ).pack(expand=True)