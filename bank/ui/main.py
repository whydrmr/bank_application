from .identification_ui import identification_mainloop
from .menu_ui import ouvrir_menu

def se_connecter():
    """
    verification de ID et MDP
    """
    fenetre, id, cle_user, blase = identification_mainloop()
    print(blase) #renvoie None
    
    if id is not None:
        ouvrir_menu(fenetre, id, cle_user, blase)

se_connecter()