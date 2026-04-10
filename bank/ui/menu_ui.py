from tkinter import *
import gestion_compte_ui
import gestion_budget_ui

def ouvrir_menu(fenetre_parente):
    fenetre_menu = gestion_budget_ui.Toplevel(fenetre_parente)
    fenetre_menu.title("Menu Principal")
    fenetre_menu.geometry("500x500")

    gestion_budget_ui.Label(fenetre_menu, text="Que souhaitez-vous faire ?", font=("", 20)).pack(expand=True)

    gestion_budget_ui.Button(fenetre_menu, text="Aller à la Gestion de compte", command=lambda: gestion_compte_ui.ouvrir_gestion_compte(fenetre_menu)).pack(expand=True)
           
    gestion_budget_ui.Button(fenetre_menu, text="Aller à la Gestion de budget", command=lambda: gestion_budget_ui.ouvrir_gestion_budget(fenetre_menu)).pack(expand=True)

    gestion_budget_ui.Button(fenetre_menu, text = "Fermer", command = fenetre_menu.destroy).pack(expand=True)