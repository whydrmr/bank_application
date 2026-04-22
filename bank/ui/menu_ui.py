import tkinter as tk
from . import gestion_compte_ui
from . import gestion_budget_ui


def ouvrir_menu(fenetre_parente, id_compte, cle):
    fenetre_menu = tk.Toplevel(fenetre_parente)
    fenetre_menu.title("Menu Principal")
    fenetre_menu.geometry("1000x1000")

    tk.Label(fenetre_menu, text="Que souhaitez-vous faire ?", font=("", 20)).pack(
        expand=True
    )

    tk.Button(
        fenetre_menu,
        text="Aller à la Gestion de compte",
        command=lambda: gestion_compte_ui.main_gestion_compte(
            fenetre_menu, id_compte, cle
        ),
    ).pack(expand=True)

    tk.Button(
        fenetre_menu,
        text="Aller à la Gestion de budget",
        command=lambda: gestion_budget_ui.ouvrir_gestion_budget(fenetre_menu),
    ).pack(expand=True)

    tk.Button(fenetre_menu, text="Fermer", command=fenetre_menu.destroy).pack(
        expand=True
    )
