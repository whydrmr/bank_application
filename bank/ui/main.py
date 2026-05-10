from .identification_ui import identification_mainloop
from .menu_ui import ouvrir_menu


def se_connecter():
    """

    None --> None

    La fonction se_connecter() lance tout l'application.

    """
    fenetre, id, cle_user, blase = identification_mainloop()
    print(blase)  # renvoie None

    if id is not None:
        ouvrir_menu(fenetre, id, cle_user, blase)


if __name__ == "__main__":
    se_connecter()

