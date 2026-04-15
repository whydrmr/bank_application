from tkinter import *
from menu_ui import ouvrir_menu

def se_connecter():
    """
    verification de ID et MDP
    """
    
    ouvrir_menu(identification_fenetre)

#Fenetre identification

identification_fenetre = Tk()
identification_fenetre.title("Espace Bancaire - Connexion")
identification_fenetre.geometry("500x500")

frm_id_mdp = Frame(identification_fenetre)
frm_id_mdp.pack(expand = True, padx = (0,10))

Label(frm_id_mdp, text = "     Bienvenue sur la fenêtre principale !", font = ("", 25)).pack(expand = True, pady = 20)

# id
frm_id = Frame(frm_id_mdp)
frm_id.pack( anchor = CENTER, padx = (40,0) , pady =5 )
Label(frm_id, text = "ID :").pack(side = LEFT, padx = 5)
Entry(frm_id).pack(side=LEFT, padx = 3)

# mdp
frm_mdp = Frame(frm_id_mdp)
frm_mdp.pack(anchor = CENTER, padx = (24,0), pady = (10, 50))
Label(frm_mdp, text="MDP :").pack(side=LEFT, padx=5)
Entry(frm_mdp, show="*").pack(side=LEFT, padx = 1)

# connection
Button(frm_id_mdp, text="Se connecter", command = se_connecter).pack(expand=True, padx = (50,0), pady = 50)

identification_fenetre.mainloop()