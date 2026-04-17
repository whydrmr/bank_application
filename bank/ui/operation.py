from tkinter import *

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