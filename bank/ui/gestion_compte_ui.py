import tkinter as tk
from tkinter.ttk import Combobox
from tkcalendar import Calendar, DateEntry
from datetime import date
from ..core import gestion_compte


def action_virement(base_de_donnees, base_de_budgets, id_compte, cle, dep, dest, montant, date, fenetre):
    '''correspondance etre le virement graphique UI et CORE
    '''
    
    compte_dep = dep.get().lower().replace(" ", "_")
    compte_dest = dest.get().lower().replace(" ", "_")
    somme = float(montant.get())

    gestion_compte.virement(base_de_donnees, id_compte, compte_dep, compte_dest, somme, date)
    gestion_compte.sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle)
    fenetre.destroy()

def action_ajouter_operation(base_de_donnees, base_de_budgets, id_compte, cle, compte_selectionner, date, libelle, montant, choixtyp, choixbud, fenetre):
    '''correspondance etre les operations graphique UI et CORE
    '''
    
    #pour selectionner le compte qu'on veut utilisera
    compte = compte_selectionner.get().lower().replace(" ", "_")

    data = {
        "date" : date.get(),
        "libelle" : libelle.get(),
        "montant" : float(montant.get()),
        "verification" : choixtyp.get(), #verification n'est pas verification mais le type (VIR OU OPT) ducoup a revoir
        "budget" : choixbud.get()
    }

    #ajout memoire
    gestion_compte.operation(base_de_donnees, base_de_budgets, id_compte, compte, data)

    #sauvegarder
    gestion_compte.sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle)
    fenetre.destroy()
    
def action_ajouter_compte(base_de_donnees, base_de_budgets, id_compte, nom_cpt, cle, fenetre):
    '''correspondance etre l'ajout de compte graphique UI et CORE
    '''
    #ajouter a la mamoire
    gestion_compte.ajouter_compte(
        base_de_donnees, base_de_budgets, id_compte, nom_cpt.get())
    #sauvegarder
    gestion_compte.sauvegarder_utilisateur(
        id_compte, base_de_donnees, base_de_budgets, cle)
    fenetre.destroy()

def virement(fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle):
    '''interface graphique pour les virements inter-compte'''
    fenetre_virement = tk.Toplevel(fenetre_gestion_compte)
    #fenetre_gestion_compte.withdraw() permet de faire disparaitre la fenetre mere mais jcp comment la faire reapparaitre apres ...
    fenetre_virement.title("Virement")
    fenetre_virement.geometry("1000x1000")

    frm_virement = tk.Frame(fenetre_virement)
    frm_virement.pack(expand=True, anchor=tk.CENTER)

    tk.Label(frm_virement, text="Virement", font=("", 25)).pack(
        expand=True, pady=(30, 200)
    )
    
    #recuperation des compte existants
    liste_compte = []
    if id_compte in base_de_donnees:
        liste_compte = [compte.replace("_",  " ").title() for compte in base_de_donnees[id_compte].keys()]

    # Compte départ
    frm_depart = tk.Frame(frm_virement)
    frm_depart.pack(expand=True, anchor=tk.CENTER, padx=(40, 0), pady=(0, 20))

    lbl_compte_dep = tk.Label(frm_depart, text="Compte de départ :", font=("", 16))
    lbl_compte_dep.pack(side=tk.LEFT, padx=(16, 0), expand=True)

    dep = Combobox(frm_depart, values=liste_compte, state="readonly")
    dep.pack(expand=True)

    # Compte destinataire
    frm_dest = tk.Frame(frm_virement)
    frm_dest.pack(expand=True, anchor=tk.CENTER, padx=(24, 0))

    lbl_compte_dest = tk.Label(frm_dest, text="Compte destinataire :", font=("", 16))
    lbl_compte_dest.pack(side=tk.LEFT, padx=(20, 0), pady=(45, 50), expand=True)

    dest = Combobox(frm_dest, values=liste_compte, state="readonly")
    dest.pack(expand=True)

    frm_montant = tk.Frame(frm_virement)
    frm_montant.pack(anchor=tk.CENTER, expand=True)
    tk.Label(frm_montant, text="Montant :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT, padx=(50, 0))
    verif_int = (fenetre_virement.register(gestion_compte.validation_montant), '%P')
    montant = tk.Entry(frm_montant, font=("", 14), width=10, validate = "key", validatecommand = verif_int)
    montant.pack(side=tk.LEFT)
    

    tk.Button(
        frm_virement,
        text="Valider",
        command=lambda: action_virement(
            base_de_donnees, base_de_budgets, id_compte, cle, dep, dest, montant, date.today(), fenetre_virement
        ),
    ).pack(expand=True, pady=(75, 0))

    tk.Button(fenetre_virement, text="Annuler", command=fenetre_virement.destroy).pack(
        expand=True, pady=(0, 2)
    )

def addop(fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, compte, cle):
    '''interface graphique pour les diverses operations'''

    fen_op = tk.Toplevel(fenetre_gestion_compte)
    fen_op.title("Ajouter une opération")
    fen_op.geometry("1000x1000")

    tk.Label(fen_op, text="Ajouter une opération", font=("", 18)).pack(pady=20)

    frm_op = tk.Frame(fen_op)
    frm_op.pack(pady=20)

    #choix parmis les compte existants
    liste_compte = []
    if id_compte in base_de_donnees:
        liste_compte = [compte.replace("_",  " ").title() for compte in base_de_donnees[id_compte].keys()]
    
    frm_compte = tk.Frame(frm_op)
    frm_compte.pack(anchor=tk.W, pady=5)
    tk.Label(frm_compte, text="Compte :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)
    cbb_choixCOMPTE = Combobox(frm_compte, values=liste_compte, state="readonly")
    cbb_choixCOMPTE.pack(side=tk.LEFT)

    #DATE
    
    frm_date = tk.Frame(frm_op)
    frm_date.pack(anchor=tk.W, pady=5)
    tk.Label(frm_date, text="Date :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)

    date = DateEntry(
        frm_date, 
        font = ("", 14), 
        width = 18, 
        date_pattern = "dd/mm/yyyy", 
        state = "readonly"
    )
    date.pack(side=tk.LEFT)

    #LIBELLE
    frm_libelle = tk.Frame(frm_op)
    frm_libelle.pack(anchor=tk.W, pady=5)
    tk.Label(frm_libelle, text="Libellé :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)
    libelle = tk.Entry(frm_libelle, font=("", 14), width=20)
    libelle.pack(side=tk.LEFT)

    #MONTANT
    frm_montant = tk.Frame(frm_op)
    frm_montant.pack(anchor=tk.W, pady=5)
    tk.Label(frm_montant, text="Montant :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)
    verif_int = (fen_op.register(gestion_compte.validation_montant), '%P') #Proposed donc le texte total dans le frame budget (verifie tout en gros)
    montant = tk.Entry(
        frm_montant, 
        font = ("", 14), 
        width = 20, 
        validate = "key", #quand je tape au clavier
        validatecommand = verif_int
    )
    montant.pack(side=tk.LEFT)

    #TYPE (VIR OPT)
    frm_typ = tk.Frame(frm_op)
    frm_typ.pack(anchor=tk.W, pady=5)
    tk.Label(frm_typ, text="Type :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)
    choixVIR = ["VIR", 'OPT']
    cbb_choixVIR = Combobox(frm_typ, values=choixVIR, state="readonly")
    cbb_choixVIR.pack(expand=True)

    #BUDGET
    frm_bud = tk.Frame(frm_op)
    frm_bud.pack(anchor=tk.W, pady=5)
    tk.Label(frm_bud, text="Budget :", font=("", 16), width=10, anchor=tk.W).pack(side=tk.LEFT)
    choixbud = ["sorties", "divers", "alimentation"]
    cbb_choixbud = Combobox(frm_bud, values=choixbud, state="readonly")
    cbb_choixbud.pack(expand=True)

    frm_button = tk.Frame(fen_op)
    frm_button.pack(pady=20)

    tk.Button(
        frm_button,
        text="Valider",
        command=lambda: action_ajouter_operation(
            base_de_donnees, base_de_budgets, id_compte, cle, cbb_choixCOMPTE, date, libelle, montant, cbb_choixVIR, cbb_choixbud, fen_op
        ),
    ).pack(expand=True, pady=(75, 0))

    tk.Button(frm_button, text="Annuler", command=fen_op.destroy).pack(
        side=tk.LEFT, padx=10
    )

def addcompte(fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle):
    '''interface graphique pour ajouter un compte dans sa BDD'''

    fen_compte = tk.Toplevel(fenetre_gestion_compte)
    fen_compte.title("Ajouter un compte")
    fen_compte.geometry("1000x1000")

    tk.Label(fen_compte, text="Ajouter un compte", font=("", 18)).pack(pady=20)

    frm_compte = tk.Frame(fen_compte)
    frm_compte.pack(pady=20)

    frm_nom = tk.Frame(frm_compte)
    frm_nom.pack(anchor=tk.W, pady=10)

    tk.Label(frm_nom, text="Nom du compte :", font=("", 16), width=15, anchor=tk.W).pack(side=tk.LEFT)

    nom = tk.Entry(frm_nom, font=("", 14), width=20)
    nom.pack(side=tk.LEFT)

    frm_solde = tk.Frame(frm_compte)
    frm_solde.pack(anchor=tk.W, pady=10)
    tk.Label(frm_solde, text="Solde initial : ", font=("", 16), width=15, anchor=tk.W).pack(side=tk.LEFT)
    verif_int = (fen_compte.register(gestion_compte.validation_montant), '%P') #Proposed donc le texte total dans le frame (verifie tout en gros)
    montant = tk.Entry(frm_solde, font=("", 14), width=20, validate = "key", validatecommand = verif_int)
    montant.pack(side=tk.LEFT)

    frm_button = tk.Frame(fen_compte)
    frm_button.pack(pady=20)
    
    tk.Button(frm_button, text="Annuler", command=fen_compte.destroy).pack(
        side=tk.LEFT, padx=10
    )

    tk.Button(
        frm_button,
        text="Ajouter",
        command=lambda: action_ajouter_compte(
            base_de_donnees, base_de_budgets, id_compte, nom, cle, fen_compte
        ),
    ).pack(side=tk.LEFT, padx=10)

def main_gestion_compte(fenetre_principale, id_compte, cle, compte, blase, dir_user = 'bank/core/users'):
    '''interface graphique qui regroupe tout'''

    base_de_donnees, base_de_budgets = gestion_compte.charger_donnees(dir_user, cle)
    fenetre_gestion_compte = tk.Toplevel(fenetre_principale)
    fenetre_gestion_compte.title("Gestion de compte")
    fenetre_gestion_compte.geometry("1000x1000")


    tk.Label(
        fenetre_gestion_compte, 
        text=f"Gestion des comptes de l'utilisateur : {blase}", 
        font=("", 18)
    ).pack(expand=True)
    
    
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

    if soldes_par_compte: #laisser sinon ca bug si ya pas de compte existant
        frm_details = tk.LabelFrame(fenetre_gestion_compte, padx=20, pady=10)
        frm_details.pack(pady=20)
        
        for nom, solde in soldes_par_compte.items():
            #couleur_texte = "green" if solde >= 0 else "red"
            
            frm_ligne = tk.Frame(frm_details)
            frm_ligne.pack(fill=tk.X, pady=2)
            
            tk.Label(frm_ligne, text=nom, font=("", 12), width=20, anchor="w").pack(side=tk.LEFT)
            tk.Label(frm_ligne, text=solde, font=("", 12, "bold"), width=15, anchor="e").pack(side=tk.RIGHT) #fg=couleur_texte
            

    frm_montant = tk.Frame(fenetre_gestion_compte)
    frm_montant.pack(expand=True)
    
    couleur_fond = "green" if solde_total >= 0 else "red"
    
    lbl_montant = tk.Label(
        frm_montant, 
        text=f"Solde total : {solde_total:.2f} €", 
        bg=couleur_fond,
        fg="white",
        font=("", 16)
    )
    lbl_montant.pack(anchor=tk.CENTER)

    tk.Button(
        fenetre_gestion_compte,
        text="+ ajouter opération",
        command=lambda: addop(
            fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, compte, cle
        ),
    ).pack(expand=True)

    tk.Button(
        fenetre_gestion_compte,
        text="+ faire virement",
        command=lambda: virement(fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle),
    ).pack(expand=True)

    tk.Button(
        fenetre_gestion_compte,
        text="+ ajouter compte",
        command=lambda: addcompte(
            fenetre_gestion_compte, base_de_donnees, base_de_budgets, id_compte, cle
        ),
    ).pack(expand=True)

    tk.Button(
        fenetre_gestion_compte, text="Fermer", command=fenetre_gestion_compte.destroy
    ).pack(expand=True, pady=50)
