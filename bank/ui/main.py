from .identification_ui import identification_mainloop
from .menu_ui import ouvrir_menu

def se_connecter():
    """
    verification de ID et MDP
    """
    fenetre, id, cle_user = identification_mainloop()
    
    if id is not None:
        ouvrir_menu(fenetre, id, cle_user)

se_connecter()