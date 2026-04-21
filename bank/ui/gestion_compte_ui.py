import tkinter as tk
from tkinter.ttk import Combobox
from datetime import date
from ..core import gestion_compte


def init_f(base_d, base_b, id):
    global base_de_donnees, base_de_budgets, id_compte
    base_de_donnees = base_d
    base_de_budgets = base_b
    id_compte = id


def action_virement(dep, dest, montant, date):
    compte_1 = dep.get().lower().replace(" ", "_")
    compte_2 = dest.get().lower().replace(" ", "_")
    somme = float(montant.get())
    date = date.get()

    gestion_compte.virement(base_de_donnees, id_compte, compte_1, compte_2, somme, date)


# def action_ajouter_operation():
# #add logic
# addop(fenetre_gestion_compte)


def action_ajouter_compte(nom_cpt):
    gestion_compte.ajouter_compte(
        base_de_donnees, base_de_budgets, id_compte, nom_cpt.get()
    )


def virement():
    fenetre_virement = tk.Tk()
    fenetre_virement.title("Virement")
    fenetre_virement.geometry("1000x1000")

    frm_virement = tk.Frame(fenetre_virement)
    frm_virement.pack(expand=True, anchor=tk.CENTER)

    tk.Label(frm_virement, text="Virement", font=("", 25)).pack(
        expand=True, pady=(30, 200)
    )

    # Compte départ
    frm_depart = tk.Frame(frm_virement)
    frm_depart.pack(expand=True, anchor=tk.CENTER, padx=(40, 0))

    lbl_compte_dep = tk.Label(frm_depart, text="Compte de départ :", font=("", 16))
    lbl_compte_dep.pack(side=tk.LEFT, padx=(16, 0), expand=True)

    dep = Combobox(frm_depart, values=list(base_de_donnees[id_compte].keys()))
    dep.pack(expand=True)

    # Compte destinataire
    frm_dest = tk.Frame(frm_virement)
    frm_dest.pack(expand=True, anchor=tk.CENTER, padx=(24, 0))

    lbl_compte_dest = tk.Label(frm_dest, text="Compte destinataire :", font=("", 16))
    lbl_compte_dest.pack(side=tk.LEFT, padx=(20, 0), pady=(45, 50), expand=True)

    dest = Combobox(frm_dest, values=list(base_de_donnees[id_compte].keys()))
    dest.pack(expand=True)

    frm_montant = tk.Frame(frm_virement)
    frm_montant.pack(expand=True, anchor=tk.CENTER)
    tk.Label(frm_montant, text="Montant :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )
    montant = tk.Entry(frm_montant, font=("", 14), width=20).pack(side=tk.LEFT)

    tk.Button(
        fenetre_virement,
        text="Valider",
        command=lambda: action_virement(dep, dest, montant, date.today()),
    ).pack(expand=True, pady=2)

    tk.Button(fenetre_virement, text="Fermer", command=fenetre_virement.destroy).pack(
        expand=True, pady=(0, 2)
    )


def addop():
    fen_op = tk.Tk()
    fen_op.title("Ajouter une opération")
    fen_op.geometry("1000x1000")

    tk.Label(fen_op, text="Ajouter une opération", font=("", 18)).pack(pady=20)

    frm_op = tk.Frame(fen_op)
    frm_op.pack(pady=20)

    frm_date = tk.Frame(frm_op)
    frm_date.pack(anchor=tk.W, pady=5)
    tk.Label(frm_date, text="Date :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )
    tk.Entry(frm_date, font=("", 14), width=20).pack(side=tk.LEFT)

    frm_libelle = tk.Frame(frm_op)
    frm_libelle.pack(anchor=tk.W, pady=5)
    tk.Label(frm_libelle, text="Libellé :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )
    tk.Entry(frm_libelle, font=("", 14), width=20).pack(side=tk.LEFT)

    frm_montant = tk.Frame(frm_op)
    frm_montant.pack(anchor=tk.W, pady=5)
    tk.Label(frm_montant, text="Montant :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )
    tk.Entry(frm_montant, font=("", 14), width=20).pack(side=tk.LEFT)

    frm_typ = tk.Frame(frm_op)
    frm_typ.pack(anchor=tk.W, pady=5)
    tk.Label(frm_typ, text="Type :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )

    choixtyp = ["CB", "VIR"]
    cbb_choixtyp = Combobox(frm_typ, values=choixtyp)
    cbb_choixtyp.pack(expand=True)

    frm_bud = tk.Frame(frm_op)
    frm_bud.pack(anchor=tk.W, pady=5)
    tk.Label(frm_bud, text="Budget :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT
    )

    choixbud = ["sorties", "divers", "alimentation"]
    cbb_choixbud = Combobox(frm_bud, values=choixbud)
    cbb_choixbud.pack(expand=True)

    frm_button = tk.Frame(fen_op)
    frm_button.pack(pady=20)

    tk.Button(frm_button, text="Annuler", command=fen_op.destroy).pack(
        side=tk.LEFT, padx=10
    )


def addcompte():
    fen_compte = tk.Tk()
    fen_compte.title("Ajouter un compte")
    fen_compte.geometry("1000x1000")

    tk.Label(fen_compte, text="Ajouter un compte", font=("", 18)).pack(pady=20)

    frm_compte = tk.Frame(fen_compte)
    frm_compte.pack(pady=20)

    frm_nom = tk.Frame(frm_compte)
    frm_nom.pack(anchor=tk.W, pady=10)
    tk.Label(
        frm_nom, text="Nom du compte :", font=("", 16), width=15, anchor=tk.W
    ).pack(side=tk.LEFT)
    nom = tk.Entry(frm_nom, font=("", 14), width=20).pack(side=tk.LEFT)

    frm_solde = tk.Frame(frm_compte)
    frm_solde.pack(anchor=tk.W, pady=10)
    # tk.Label(
    #    frm_solde, text="Solde initial :", font=("", 16), width=15, anchor=tk.W
    # ).pack(side=tk.LEFT)
    # tk.Entry(frm_solde, font=("", 14), width=20).pack(side=tk.LEFT)

    frm_button = tk.Frame(fen_compte)
    frm_button.pack(pady=20)

    tk.Button(frm_button, text="Annuler", command=fen_compte.destroy).pack(
        side=tk.LEFT, padx=10
    )

    tk.Button(
        frm_button, text="Ajouter", command=lambda: action_ajouter_compte(nom)
    ).pack(side=tk.LEFT, padx=10)


def ouvrir_gestion_compte(fenetre_principale):
    fenetre_gestion_compte = tk.Toplevel(fenetre_principale)
    fenetre_gestion_compte.title("Gestion de compte")
    fenetre_gestion_compte.geometry("1000x1000")

    tk.Label(fenetre_gestion_compte, text="Gestion de Compte", font=("", 18)).pack(
        expand=True
    )

    frm_montant = tk.Frame(fenetre_gestion_compte)
    frm_montant.pack(expand=True)
    lbl_montant = tk.Label(frm_montant, text="Montant : 1500 €", bg="green")
    lbl_montant.pack(anchor=tk.CENTER)

    tk.Button(
        fenetre_gestion_compte,
        text="+ ajouter opération",
        command=addop,
    ).pack(expand=True)

    tk.Button(fenetre_gestion_compte, text="+ faire virement", command=virement).pack(
        expand=True
    )

    tk.Button(fenetre_gestion_compte, text="+ ajouter compte", command=addcompte).pack(
        expand=True
    )

    tk.Button(
        fenetre_gestion_compte, text="Fermer", command=fenetre_gestion_compte.destroy
    ).pack(expand=True, pady=50)
