import tkinter as tk
import os
from . import gestion_compte_ui
from . import gestion_budget_ui


def ouvrir_menu(fenetre_parente, id_compte, cle, blase, dir_user="bank/core/users"):
    """
    Permet de lier gestion de compte ou  gestion de budget avec la phase d'identification
    fenetrexstrxstrxstrxdirectory -> None

    """
    dir_user = os.path.join(os.path.dirname(__file__), '..', 'core', 'users')

    fenetre_menu = tk.Toplevel(fenetre_parente)
    fenetre_menu.title("Menu Principal")
    fenetre_menu.geometry("1000x1000")

    tk.Label(
        fenetre_menu, text="Que souhaitez-vous faire ?", font=("Arial", 35, "bold")
    ).pack(pady=(150, 150))

    frame_boutons = tk.Frame(fenetre_menu)
    frame_boutons.pack(expand=True)
    frame_boutons.columnconfigure(0, weight=2)
    frame_boutons.columnconfigure(1, weight=2)

    tk.Button(
        frame_boutons,
        text="Gestion de compte",
        font=("Arial", 16, "bold"),
        width=25,
        height=2,
        command=lambda: gestion_compte_ui.main_gestion_compte(
            fenetre_principale = fenetre_menu, id_compte = id_compte, cle = cle, compte = None, blase = blase, dir_user = os.path.join(os.path.dirname(__file__), '..', 'core', 'users')
        ),
    ).grid(row=0, column=0, padx=40, sticky="w")

    tk.Button(
        frame_boutons,
        text="Gestion de budget",
        font=("Arial", 16, "bold"),
        width=25,
        height=2,
        command=lambda: gestion_budget_ui.ouvrir_gestion_budget(fenetre_parente = fenetre_menu, id_compte = id_compte, cle = cle, dir_user = dir_user),
    ).grid(row=0, column=1, padx=40, sticky="e")

    tk.Button(
        fenetre_menu,
        text="Fermer",
        font=("Arial", 14, "bold"),
        width=20,
        command=fenetre_parente.destroy,
    ).pack(pady=150)

    fenetre_menu.mainloop()
