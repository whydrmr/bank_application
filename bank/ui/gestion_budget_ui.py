import tkinter as tk

# CORRECTION : ajout du paramètre fenetre_parente
def ouvrir_gestion_budget(fenetre_parente): 
    # CORRECTION : utilisation de Toplevel pour créer une fenêtre secondaire
    fenetre_gestion_budget = tk.Toplevel(fenetre_parente)
    fenetre_gestion_budget.title("Gestion de Budget")
    fenetre_gestion_budget.geometry("500x500")

    tk.Label(
        fenetre_gestion_budget, text="Interface de Gestion de Budget", font=("", 18)
    ).pack(expand=True)
    tk.Button(
        fenetre_gestion_budget, text="Fermer", command=fenetre_gestion_budget.destroy
    ).pack(expand=True)
    
    # SUPPRESSION de fenetre_gestion_budget.mainloop()