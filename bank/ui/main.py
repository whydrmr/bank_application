from .identification_ui_v2 import identification_mainloop


def se_connecter():
    """
    verification de ID et MDP
    """
    id, cle_user = identification_mainloop()
    print("juste pour etre sur : ", id, cle_user)
    
se_connecter()
