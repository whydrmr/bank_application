from identification import main_identification
from gestion_compte import main_gestion_compte


def main():
    id, cle = main_identification()
    while True:
        response = input(
            "| 1 : Gestion compte \n| 2 : Gestion_budget \n| 3 : Changer identifiant \n| 'q' : quitter \n"
        )
        if response == "1":
            main_gestion_compte(id, cle)
        elif response == "2":
            from gestion_budget import main_gestion_budget

            main_gestion_budget(id, cle)
        elif response == "3":
            main()
        elif response == "q":
            print("Au revoir :)")
            break
        else:
            print("Input invalide...")
            continue


main()
