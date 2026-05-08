import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Scrollbar
from datetime import datetime
from ..core import gestion_compte

def ouvrir_gestion_budget(fenetre_parente, id_compte, cle, dir_user): 
    base_de_donnees, base_de_budgets = gestion_compte.charger_donnees(dir_user, cle)
    
    fenetre_gestion_budget = tk.Toplevel(fenetre_parente)
    fenetre_gestion_budget.title("Gestion de Budget")
    fenetre_gestion_budget.geometry("1000x850")

    categories_base = {"sorties", "divers", "alimentation"}
    if id_compte in base_de_budgets:
        for compte_cle in base_de_budgets[id_compte]:
            for b_item in base_de_budgets[id_compte][compte_cle]:
                categories_base.add(b_item[0].strip().lower())
    categories = sorted(list(categories_base))

    frm_entete = tk.Frame(fenetre_gestion_budget)
    frm_entete.pack(fill=tk.X, pady=15)
    tk.Label(frm_entete, text="Gestion de Budget", font=("Arial", 25, "bold")).pack(side=tk.LEFT, padx=50)
    tk.Button(frm_entete, text="Fermer", font=("Arial", 12, "bold"), bg="white", fg="black", command=fenetre_gestion_budget.destroy).pack(side=tk.RIGHT, padx=50)

    frm_select = tk.Frame(fenetre_gestion_budget)
    frm_select.pack(pady=10)
    tk.Label(frm_select, text="Compte :", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10)
    
    liste_compte_noms = [c.replace("_", " ").title() for c in base_de_donnees.get(str(id_compte), {}).keys()]
    cbb_compte = Combobox(frm_select, values=liste_compte_noms, state="readonly", font=("Arial", 14), width=20)
    cbb_compte.pack(side=tk.LEFT)

    tk.Button(frm_select, text="Rafraîchir les données", font=("Arial", 12, "bold"), bg="white", fg="black", 
              command=lambda: actualiser_affichage()).pack(side=tk.LEFT, padx=20)

    tk.Label(frm_select, text="Trier par :", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=(10, 5))
    cbb_tri = Combobox(frm_select, values=["Date", "Libellé", "Catégorie", "Montant"], state="readonly", font=("Arial", 12), width=12)
    cbb_tri.set("Date")
    cbb_tri.pack(side=tk.LEFT, padx=5)

    frm_budgets = tk.LabelFrame(fenetre_gestion_budget, text="Définir / Suivre les Budgets", font=("Arial", 14, "bold"), padx=20, pady=10)
    frm_budgets.pack(fill=tk.X, padx=50, pady=15)

    frm_ligne_budget = tk.Frame(frm_budgets)
    frm_ligne_budget.pack(fill=tk.X, pady=5)
    
    tk.Label(frm_ligne_budget, text="Catégorie :", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    cbb_cat = Combobox(frm_ligne_budget, values=categories, state="readonly", font=("Arial", 12), width=15)
    cbb_cat.pack(side=tk.LEFT, padx=5)

    tk.Label(frm_ligne_budget, text="modifier budget (€) :", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    ent_budget_modif = tk.Entry(frm_ligne_budget, font=("Arial", 12), width=10)
    ent_budget_modif.pack(side=tk.LEFT, padx=5)
    
    lbl_init = tk.Label(frm_ligne_budget, text="Budget Initial : -- €", font=("Arial", 12, "bold"))
    lbl_init.pack(side=tk.LEFT, padx=20)
    
    lbl_dispo = tk.Label(frm_ligne_budget, text="Dispo: -- €", font=("Arial", 12, "bold"))
    lbl_dispo.pack(side=tk.LEFT, padx=20)

    def actualiser_stats_categorie(*args): #*args
        cat = cbb_cat.get().strip().lower()
        compte_sel = cbb_compte.get().lower().replace(" ", "_")
        if not cat or not compte_sel: return
        
        depenses_totales = 0.0
        if id_compte in base_de_donnees and compte_sel in base_de_donnees[id_compte]:
            for op in base_de_donnees[id_compte][compte_sel]:
                try:
                    if str(op[5]).strip().lower() == cat:
                        depenses_totales += float(op[3])
                except: pass
                    
        budget_limite = 0.0
        if id_compte in base_de_budgets and compte_sel in base_de_budgets[id_compte]:
            for b in base_de_budgets[id_compte][compte_sel]:
                if b[0].strip().lower() == cat:
                    budget_limite = float(b[1])
                    break
        
        dispo = budget_limite + depenses_totales
        
        ent_budget_modif.delete(0, tk.END)
        ent_budget_modif.insert(0, f"{budget_limite:.2f}")
        
        lbl_dispo.config(text=f"Dispo: {dispo:.2f} €", fg="green" if dispo > 0 else "red")
        lbl_init.config(text=f"Initial: {budget_limite:.2f} €", fg="green" if dispo >= 0 else "red")

    def valider_budget():
        cat = cbb_cat.get().strip().lower()
        compte_sel = cbb_compte.get().lower().replace(" ", "_")
        if not cat or not compte_sel: return
        try:
            nouveau_budget_limite = float(ent_budget_modif.get())
            if id_compte not in base_de_budgets: base_de_budgets[id_compte] = {}
            if compte_sel not in base_de_budgets[id_compte]: base_de_budgets[id_compte][compte_sel] = []
            
            trouve = False
            for b in base_de_budgets[id_compte][compte_sel]:
                if b[0].strip().lower() == cat:
                    b[1] = nouveau_budget_limite
                    trouve = True
                    break
            if not trouve:
                base_de_budgets[id_compte][compte_sel].append([cat, nouveau_budget_limite])
            
            gestion_compte.sauvegarder_utilisateur(id_compte, base_de_donnees, base_de_budgets, cle)
            messagebox.showinfo("Succès", "Budget mis à jour")
            actualiser_stats_categorie()
        except ValueError:
            messagebox.showerror("Erreur", "Entrez un nombre valide.")

    tk.Button(frm_ligne_budget, text="Enregistrer", bg="white", fg="black", command=valider_budget).pack(side=tk.LEFT, padx=10)

    frm_ajout = tk.Frame(frm_budgets)
    frm_ajout.pack(fill=tk.X, pady=10)
    tk.Label(frm_ajout, text="Nouvelle catégorie :", font=("Arial", 10)).pack(side=tk.LEFT)
    ent_new_cat = tk.Entry(frm_ajout, width=15)
    ent_new_cat.pack(side=tk.LEFT, padx=5)

    def ajouter_cat():
        new_cat = ent_new_cat.get().strip().lower()
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            categories.sort()
            cbb_cat['values'] = categories
            cbb_cat.set(new_cat)
            ent_new_cat.delete(0, tk.END)
            actualiser_stats_categorie()

    tk.Button(frm_ajout, text="+ Ajouter", command=ajouter_cat).pack(side=tk.LEFT)

    frm_tableau = tk.Frame(fenetre_gestion_budget)
    frm_tableau.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)

    cols = ("Date", "Libellé", "Catégorie", "Montant")
    tree = Treeview(frm_tableau, columns=cols, show="headings", height=10)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=150, anchor="center")
    
    scrollbar = Scrollbar(frm_tableau, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def actualiser_affichage(*args):
        nonlocal base_de_donnees, base_de_budgets
        base_de_donnees, base_de_budgets = gestion_compte.charger_donnees(dir_user, cle)
        compte_sel = cbb_compte.get().lower().replace(" ", "_")
        if not compte_sel: return
            
        for i in tree.get_children(): tree.delete(i)
        
        trans = []
        if id_compte in base_de_donnees and compte_sel in base_de_donnees[id_compte]:
            for op in base_de_donnees[id_compte][compte_sel]:
                try:
                    trans.append((op[0], op[1], str(op[5]).strip().title(), float(op[3])))
                except: pass

        critere = cbb_tri.get()
        if critere == "Date":
            def safe_date_sort(x):
                try: return datetime.strptime(x[0], "%Y/%m/%d")
                except: 
                    try: return datetime.strptime(x[0], "%d/%m/%Y")
                    except: return datetime.min
            trans.sort(key=safe_date_sort, reverse=True)
        elif critere == "Libellé":
            trans.sort(key=lambda x: x[1].lower())
        elif critere == "Catégorie":
            trans.sort(key=lambda x: x[2].lower())
        elif critere == "Montant":
            trans.sort(key=lambda x: x[3], reverse=True)

        # Affiche proprement date tableau
        def formater_date(date_str):
            try: return datetime.strptime(date_str, "%Y/%m/%d").strftime("%d/%m/%Y")
            except: return date_str

        for t in trans:
            tree.insert("", tk.END, values=(formater_date(t[0]), t[1], t[2], f"{t[3]:.2f} €"))

        actualiser_stats_categorie()

    cbb_compte.bind("<<ComboboxSelected>>", actualiser_affichage)
    cbb_cat.bind("<<ComboboxSelected>>", actualiser_stats_categorie)
    cbb_tri.bind("<<ComboboxSelected>>", actualiser_affichage) 
    
    if liste_compte_noms:
        cbb_compte.current(0)
        actualiser_affichage()
    if categories:
        cbb_cat.set("alimentation")
        actualiser_stats_categorie()