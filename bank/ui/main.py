from tkinter import *


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


def virement(fenetre_principale):
    fenetre_virement = Toplevel(fenetre_principale)
    fenetre_virement.title("Virement")
    fenetre_virement.geometry("500x500")

    Label(fenetre_virement, text="Virement", font=("", 18)).pack(pady=20)

    frm_virement = Frame(fenetre_virement)
    frm_virement.pack(fill=X, padx=30, pady=20)

    # Compte départ
    frm_depart = Frame(frm_virement)
    frm_depart.pack(anchor=W)

    lbl_compte_dep = Label(frm_depart, text="Compte de départ :", font=("", 16))
    lbl_compte_dep.pack(side=LEFT, padx=(40, 0), pady=5)

    liste_compte_depart = Listbox(frm_depart, height=4, font=("", 14), exportselection=False)
    liste_compte_depart.insert(1, "A")
    liste_compte_depart.insert(2, "B")
    liste_compte_depart.insert(3, "C")
    liste_compte_depart.insert(4, "D")
    liste_compte_depart.pack(side=LEFT)

    # Compte destinataire
    frm_dest = Frame(frm_virement)
    frm_dest.pack(anchor=W)

    lbl_compte_dest = Label(frm_dest, text="Compte destinataire :", font=("", 16))
    lbl_compte_dest.pack(side=LEFT, padx=(20, 0), pady=(10, 50))

    liste_compte_dest = Listbox(frm_dest, height=4, font=("", 14), exportselection=False)
    liste_compte_dest.insert(1, "A")
    liste_compte_dest.insert(2, "B")
    liste_compte_dest.insert(3, "C")
    liste_compte_dest.insert(4, "D")
    liste_compte_dest.pack(side=LEFT)

    Button(
        fenetre_virement,
        text="Fermer",
        command=fenetre_virement.destroy
    ).pack(expand=True)


def addop(fenetre_principale):
    fenop = Toplevel(fenetre_principale)
    fenop.title("Ajouter une opération")
    fenop.geometry("500x500")

    Label(fenop, text="Ajouter une opération", font=("", 18)).pack(pady=20)

    fmop = Frame(fenop)
    fmop.pack(pady=20)

    # Date
    fmdate = Frame(fmop)
    fmdate.pack(anchor=W, pady=5)
    Label(fmdate, text="Date :", font=("", 16), width=10, anchor=W).pack(side=LEFT)
    Entry(fmdate, font=("", 14), width=20).pack(side=LEFT)

    # Libelle
    fmlbl = Frame(fmop)
    fmlbl.pack(anchor=W, pady=5)
    Label(fmlbl, text="Libellé :", font=("", 16), width=10, anchor=W).pack(side=LEFT)
    Entry(fmlbl, font=("", 14), width=20).pack(side=LEFT)

    # Montant
    fmmontant = Frame(fmop)
    fmmontant.pack(anchor=W, pady=5)
    Label(fmmontant, text="Montant :", font=("", 16), width=10, anchor=W).pack(side=LEFT)
    Entry(fmmontant, font=("", 14), width=20).pack(side=LEFT)

    # Type
    fmtyp = Frame(fmop)
    fmtyp.pack(anchor=W, pady=5)
    Label(fmtyp, text="Type :", font=("", 16), width=10, anchor=W).pack(side=LEFT)

    choixtyp = Listbox(fmtyp, height=2, font=("", 14), exportselection=False)
    choixtyp.insert(1, "CB")
    choixtyp.insert(2, "VIR")
    choixtyp.pack(side=LEFT)

    # Budget
    fmbud = Frame(fmop)
    fmbud.pack(anchor=W, pady=5)
    Label(fmbud, text="Budget :", font=("", 16), width=10, anchor=W).pack(side=LEFT)

    choixbud = Listbox(fmbud, height=3, font=("", 14), exportselection=False)
    choixbud.insert(1, "sorties")
    choixbud.insert(2, "alimentation")
    choixbud.insert(3, "divers")
    choixbud.pack(side=LEFT)

    # Verif
    fmverif = Frame(fmop)
    fmverif.pack(anchor=W, pady=10)
    Label(fmverif, text="Vérifiée :", font=("", 16), width=10, anchor=W).pack(side=LEFT)

    caseverif = IntVar(master=fenop)
    Checkbutton(fmverif, variable=caseverif).pack(side=LEFT)

    # Boutons
    fmbouton = Frame(fenop)
    fmbouton.pack(pady=20)

    Button(
        fmbouton,
        text="Annuler",
        command=fenop.destroy
    ).pack(side=LEFT, padx=10)

    Button(
        fmbouton,
        text="Ajouter"
    ).pack(side=LEFT, padx=10)


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


#pert=met de teste
fenetre = Tk()
fenetre.title("Menu Principal")
fenetre.geometry("500x500")

Label(fenetre, text="Que souhaitez-vous faire ?", font=("", 18)).pack(expand=True)

Button(
    fenetre,
    text="Aller à la Gestion de compte",
    command=lambda: ouvrir_gestion_compte(fenetre)
).pack(expand=True)

Button(
    fenetre,
    text="Fermer",
    command=fenetre.destroy
).pack(expand=True)

fenetre.mainloop()