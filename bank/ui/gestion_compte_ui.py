import tkinter as tk
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from datetime import date
from ..core import gestion_compte


def action_virement(
    base_de_donnees,
    base_de_budgets,
    id_compte,
    cle,
    compte_dep,  
    dest,        
    montant,
    date,
    fenetre,
    refresh
):
    """correspondance etre le virement graphique UI et CORE"""

    compte_dest = dest.get().lower().replace(" ", "_")
    somme = float(montant.get())

    gestion_compte.virement(
        base_de_donnees, id_compte, compte_dep, compte_dest, somme, date
    )
    gestion_compte.sauvegarder_utilisateur(
        id_compte, base_de_donnees, base_de_budgets, cle
    )
    fenetre.destroy()
    refresh()


def action_ajouter_operation(
    base_de_donnees,
    base_de_budgets,
    id_compte,
    cle,
    compte_selectionner,
    date,
    libelle,
    montant,
    choixbud,
    fenetre,
    refresh,
):
    """correspondance etre les operations graphique UI et CORE"""

    # pour selectionner le compte qu'on veut utilisera
    try:
        compte = compte_selectionner.get().lower().replace(" ", "_")
    except AttributeError:
        compte = compte_selectionner

    data = {
        "date": date.get(),
        "libelle": libelle.get(),
        "montant": -float(montant.get()),
        "budget": choixbud.get(),
    }

    # ajout memoire
    gestion_compte.operation(base_de_donnees, base_de_budgets, id_compte, compte, data)

    # sauvegarder
    gestion_compte.sauvegarder_utilisateur(
        id_compte, base_de_donnees, base_de_budgets, cle
    )
    fenetre.destroy()
    refresh()


def action_ajouter_compte(
    base_de_donnees, base_de_budgets, id_compte, nom_cpt, montant, cle, fenetre, refresh
):
    """correspondance etre l'ajout de compte graphique UI et CORE"""

    nom = nom_cpt.get()

    # ajouter a la mamoire
    gestion_compte.ajouter_compte(base_de_donnees, base_de_budgets, id_compte, nom)

    montant_Init = montant.get()
    if montant_Init and montant_Init not in ("-", "+", ""):
        cle_compte = nom.lower().replace(" ", "_")
        data_op = {
            "date": date.today().strftime("%d/%m/%Y"),  # Date auto
            "libelle": "Solde initial",
            "montant": float(montant_Init),
            "verification": "True",
            "budget": "divers",
        }
        gestion_compte.operation(
            base_de_donnees, base_de_budgets, id_compte, cle_compte, data_op
        )

    # sauvegarder
    gestion_compte.sauvegarder_utilisateur(
        id_compte, base_de_donnees, base_de_budgets, cle
    )
    fenetre.destroy()
    refresh()


def virement(
    fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle, refresh, compte_selectionne
):
    """interface graphique pour les virements inter-compte"""
    
    compte_selectionne_after = compte_selectionne.get().lower().replace(" ", "_")
    fen_virement = tk.Toplevel(fenetre_gestion_compte)
    fenetre_gestion_compte.withdraw()  # permet de faire disparaitre la fenetre mere mais jcp comment la faire reapparaitre apres ...
    fen_virement.title("Virement")
    fen_virement.geometry("1000x1000")

    frm_virement = tk.Frame(fen_virement)
    frm_virement.pack(expand=True, anchor=tk.CENTER)

    tk.Label(frm_virement, text="Virement", font=("", 25)).pack(
        expand=True, pady=(30, 200)
    )

    # recuperation des compte existants
    liste_compte = []
    if id_compte in base_de_donnees:
        liste_compte = [
            compte.replace("_", " ").title()
            for compte in base_de_donnees[id_compte].keys()
        ]

    # Compte départ
    frm_depart = tk.Frame(frm_virement)
    frm_depart.pack(expand=True, anchor=tk.CENTER, padx=(40, 0), pady=(0, 20))

    lbl_compte_dep = tk.Label(frm_depart, text=f"Compte de départ : {compte_selectionne.get().lower().replace("_", " ")}", font=("", 16))
    lbl_compte_dep.pack(side=tk.LEFT, padx=(16, 0), expand=True)


    # Compte destinataire
    frm_dest = tk.Frame(frm_virement)
    frm_dest.pack(expand=True, anchor=tk.CENTER, padx=(24, 0))

    lbl_compte_dest = tk.Label(frm_dest, text="Compte destinataire :", font=("", 16))
    lbl_compte_dest.pack(side=tk.LEFT, padx=(20, 0), pady=(45, 50), expand=True)

    cbb_dest = Combobox(frm_dest, values=liste_compte, state="readonly")
    cbb_dest.pack(expand=True)

    frm_montant = tk.Frame(frm_virement)
    frm_montant.pack(anchor=tk.CENTER, expand=True)
    tk.Label(frm_montant, text="Montant :", font=("", 16), width=10, anchor=tk.W).pack(
        side=tk.LEFT, padx=(50, 0)
    )
    verif_int = (fen_virement.register(gestion_compte.validation_montant), "%P")
    montant = tk.Entry(
        frm_montant, font=("", 14), width=10, validate="key", validatecommand=verif_int
    )
    montant.pack(side=tk.LEFT)

    tk.Button(
        frm_virement,
        text="Valider",
        command=lambda: action_virement(
            base_de_donnees,
            base_de_budgets,
            id_compte,
            cle,
            compte_selectionne_after,
            cbb_dest,
            montant,
            date.today(),
            fen_virement,
            refresh, 
        ),
    ).pack(expand=True, pady=(75, 0))

    def annuler_virement():
        fen_virement.destroy()
        fenetre_gestion_compte.deiconify() 
        refresh()

    tk.Button(
        frm_virement, 
        text="Annuler",
        bg="white",
        fg="black",
        command=annuler_virement
    ).pack(expand = True, pady=(10, 20))

    fen_virement.protocol("WM_DELETE_WINDOW", annuler_virement)

def addop(
    fenetre_gestion_compte,
    base_de_donnees,
    base_de_budgets,
    id_compte,
    cle,
    compte_selectionne,
    refresh,
):
    compte_selectionne_after = compte_selectionne.get().lower().replace(" ", "_")
    fen_addop = tk.Toplevel(fenetre_gestion_compte)
    fenetre_gestion_compte.withdraw()
    fen_addop.title("Ajouter une opération")
    fen_addop.geometry("1000x1000")

    tk.Label(fen_addop, text="Ajouter une opération", font=("Arial", 30, "bold")).pack(
        pady=60
    )

    frm_op = tk.Frame(fen_addop)
    frm_op.pack(pady=50)
    
    frm_compteselect = tk.Frame(frm_op)
    frm_compteselect.pack(anchor=tk.W, pady=20)
    tk.Label(
        frm_compteselect, text=f"Compte selectionner : {compte_selectionne.get().lower().replace('_', ' ')}", font=("Arial", 20, "bold")
    ).pack(side=tk.LEFT)

    frm_date = tk.Frame(frm_op)
    frm_date.pack(anchor=tk.W, pady=20)
    tk.Label(
        frm_date, text="Date :", font=("Arial", 20, "bold"), width=10, anchor=tk.W
    ).pack(side=tk.LEFT)

    date = DateEntry(
        frm_date,
        font=("Arial", 20, "bold"),
        width=30,
        date_pattern="dd/mm/yyyy",
        state="readonly",
    )
    date.pack(side=tk.LEFT)

    frm_libelle = tk.Frame(frm_op)
    frm_libelle.pack(anchor=tk.W, pady=20)
    tk.Label(
        frm_libelle, text="Libellé :", font=("Arial", 20, "bold"), width=10, anchor=tk.W
    ).pack(side=tk.LEFT)
    libelle = tk.Entry(frm_libelle, font=("Arial", 20, "bold"), width=10)
    libelle.pack(side=tk.LEFT)

    frm_montant = tk.Frame(frm_op)
    frm_montant.pack(anchor=tk.W, pady=20)
    tk.Label(
        frm_montant, text="Montant :", font=("Arial", 20, "bold"), width=10, anchor=tk.W
    ).pack(side=tk.LEFT)
    verif_int = (
        fen_addop.register(gestion_compte.validation_montant),
        "%P",
    )
    montant = tk.Entry(
        frm_montant,
        font=("Arial", 20, "bold"),
        width=10,
        validate="key",
        validatecommand=verif_int,
    )
    montant.pack(side=tk.LEFT)

    frm_bud = tk.Frame(frm_op)
    frm_bud.pack(anchor=tk.W, pady=20)
    tk.Label(
        frm_bud, text="Budget :", font=("Arial", 20, "bold"), width=10, anchor=tk.W
    ).pack(side=tk.LEFT)

    choixbud_set = {"sorties", "divers", "alimentation"}
    if id_compte in base_de_budgets and compte_selectionne_after in base_de_budgets[id_compte]:
        for b_item in base_de_budgets[id_compte][compte_selectionne_after]:
            choixbud_set.add(b_item[0].strip().lower())
    
    choixbud = sorted(list(choixbud_set))

    cbb_choixbud = Combobox(
        frm_bud, values=choixbud, state="readonly", font=("Arial", 15, "bold"), width=30
    )
    if choixbud:
        cbb_choixbud.set(choixbud[0])
    cbb_choixbud.pack(expand=True)

    frm_button = tk.Frame(fen_addop)
    frm_button.pack(pady=20)

    tk.Button(
        fen_addop,
        text="Valider",
        font=("Arial", 18, "bold"),
        command=lambda: action_ajouter_operation(
            base_de_donnees,
            base_de_budgets,
            id_compte,
            cle,
            compte_selectionne_after,
            date,
            libelle,
            montant,
            cbb_choixbud,
            fen_addop,
            refresh,
        ),
    ).pack(pady=(1, 1))

    def annuler():
        fen_addop.destroy()
        fenetre_gestion_compte.deiconify()
        refresh()

    tk.Button(
        fen_addop, text="Annuler", font=("Arial", 12, "bold"), command=annuler
    ).pack(padx=10, pady=(20, 20))

    fen_addop.protocol("WM_DELETE_WINDOW", annuler)


def addcompte(
    fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle, refresh
):
    """interface graphique pour ajouter un compte dans sa BDD"""

    fen_addcompte = tk.Toplevel(fenetre_gestion_compte)
    fenetre_gestion_compte.withdraw()  # permet de faire disparaitre la fenetre mere mais jcp comment la faire reapparaitre apres ...
    fen_addcompte.title("Ajouter un compte")
    fen_addcompte.geometry("1000x1000")

    tk.Label(fen_addcompte, text="Ajouter un compte", font=("", 18)).pack(pady=20)

    frm_compte = tk.Frame(fen_addcompte)
    frm_compte.pack(pady=20)

    frm_nom = tk.Frame(frm_compte)
    frm_nom.pack(anchor=tk.W, pady=10)

    tk.Label(
        frm_nom, text="Nom du compte :", font=("", 16), width=15, anchor=tk.W
    ).pack(side=tk.LEFT)

    nom = tk.Entry(frm_nom, font=("", 14), width=20)
    nom.pack(side=tk.LEFT)

    frm_solde = tk.Frame(frm_compte)
    frm_solde.pack(anchor=tk.W, pady=10)
    tk.Label(
        frm_solde, text="Solde initial : ", font=("", 16), width=15, anchor=tk.W
    ).pack(side=tk.LEFT)
    verif_int = (
        fen_addcompte.register(gestion_compte.validation_montant),
        "%P",
    )  # Proposed donc le texte total dans le frame (verifie tout en gros)
    montant = tk.Entry(
        frm_solde, font=("", 14), width=20, validate="key", validatecommand=verif_int
    )
    montant.pack(side=tk.LEFT)

    frm_button = tk.Frame(fen_addcompte)
    frm_button.pack(pady=20)

    tk.Button(frm_button, text="Annuler", command=refresh).pack(
        side=tk.LEFT, padx=10
    )

    tk.Button(
        frm_button,
        text="Ajouter",
        command=lambda: (
            action_ajouter_compte(
                base_de_donnees,
                base_de_budgets,
                id_compte,
                nom,
                montant,
                cle,
                fen_addcompte,
                refresh,
            ),
        ),
    ).pack(side=tk.LEFT, padx=10)


def main_gestion_compte(
    fenetre_principale, id_compte, cle, compte, blase, dir_user
):
    """interface graphique qui regroupe tout"""

    base_de_donnees, base_de_budgets = gestion_compte.charger_donnees(dir_user, cle)
    fenetre_gestion_compte = tk.Toplevel(fenetre_principale)
    fenetre_gestion_compte.title("Gestion de compte")
    fenetre_gestion_compte.geometry("1000x800")

    def refresh():
        fenetre_gestion_compte.destroy()
        main_gestion_compte(fenetre_principale, id_compte, cle, compte, blase, dir_user)

    tk.Label(
        fenetre_gestion_compte,
        text=f"Gestion des comptes de l'utilisateur : {blase}",
        font=("Arial", 30, "bold"),
    ).pack(pady=(20, 20))

    frm_select_compte = tk.Frame(fenetre_gestion_compte)
    frm_select_compte.pack(anchor="e", padx=150, pady=10)

    tk.Label(
        frm_select_compte,
        text="Compte actuel :",
        font=("Arial", 20, "bold"),
    ).pack(side=tk.LEFT, padx=10)

    liste_compte = [
        compte.replace("_", " ").title()
        for compte in base_de_donnees[id_compte].keys()
        if compte and compte.strip()
    ]

    cbb_compte_principal = Combobox(
        frm_select_compte,
        values=liste_compte,
        state="readonly",
        font=("Arial", 14, "bold"),
        width=25,
    )

    cbb_compte_principal.pack(side=tk.LEFT)

    # autoselection du premier compte
    if liste_compte:
        cbb_compte_principal.current(0)

    # calcul argent individuel et total
    solde_total = 0.0
    soldes_par_compte = {}

    if id_compte in base_de_donnees:
        for nom_cpt, operations in base_de_donnees[id_compte].items():
            solde_compte = 0.0
            for op in operations:
                solde_compte += op[3]
                solde_total += op[3]

            nom_propre = nom_cpt.replace("_", " ").title()
            soldes_par_compte[nom_propre] = solde_compte

    frm_montant = tk.Frame(fenetre_gestion_compte)
    frm_montant.pack(pady=(50, 50))

    couleur_fond = "green" if solde_total >= 0 else "red"

    lbl_montant = tk.Label(
        frm_montant,
        text=f"Solde total : {solde_total:.2f} €",
        bg=couleur_fond,
        fg="white",
        font=("Arial", 20, "bold"),
    )
    lbl_montant.pack(anchor=tk.CENTER)

    if soldes_par_compte:  # laisser sinon ca bug si ya pas de compte existant
        frm_details = tk.LabelFrame(fenetre_gestion_compte, padx=20, pady=10)
        frm_details.pack(pady=50)

        for nom, solde in soldes_par_compte.items():
            couleur_texte = "green" if solde >= 0 else "red"

            frm_ligne = tk.Frame(frm_details)
            frm_ligne.pack(fill=tk.X, pady=2)

            tk.Label(
                frm_ligne, text=nom, font=("Arial", 15, "bold"), width=20, anchor="w"
            ).pack(side=tk.LEFT)
            tk.Label(
                frm_ligne,
                text=solde,
                font=("Arial", 18, "bold"),
                width=15,
                anchor="e",
                fg=couleur_texte,
            ).pack(side=tk.RIGHT)  # fg=couleur_texte

    frame_actions = tk.Frame(fenetre_gestion_compte)
    frame_actions.pack(pady=70)

    tk.Button(
        frame_actions,
        text="+ Ajouter opération",
        font=("Arial", 14, "bold"),
        width=25,
        height=2,
        command=lambda: addop(
            fenetre_gestion_compte,
            base_de_donnees,
            base_de_budgets,
            id_compte,
            cle,
            cbb_compte_principal,
            refresh,
        ),
    ).grid(row=0, column=0, padx=20)

    tk.Button(
        frame_actions,
        text="+ Faire virement",
        font=("Arial", 14, "bold"),
        width=25,
        height=2,
        command=lambda: virement(
            fenetre_gestion_compte,
            base_de_donnees,
            base_de_budgets,
            id_compte,
            cle,
            refresh,
            cbb_compte_principal,
        ),
    ).grid(row=0, column=1, padx=20)

    tk.Button(
        frame_actions,
        text="+ Ajouter compte",
        font=("Arial", 14, "bold"),
        width=25,
        height=2,
        command=lambda: addcompte(
            fenetre_gestion_compte,
            base_de_donnees,
            base_de_budgets,
            id_compte,
            cle,
            refresh,
        ),
    ).grid(row=0, column=2, padx=20)

    tk.Button(
        fenetre_gestion_compte,
        text="Fermer",
        font=("Arial", 12, "bold"),
        width=20,
        command=fenetre_gestion_compte.destroy,
    ).pack(pady=40)
