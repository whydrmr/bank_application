from identification import main_identification
from gestion_compte import main_gestion_compte
from gestion_budget import main_gestion_budget

def main():
    id = main_identification()
    while True:
        response = input("1 : gestion compte | 2 : gestion_budget | 3 : changer identifiant | 'q' : quitter : ")
        if response == '1':
            main_gestion_compte(id)
        elif response == '2':
            main_gestion_budget(id)
        elif response == '3':
            main()
        elif response == 'q':
            print("au revoir :)")
            break
        else:
            print("input invalide..")
            continue

main()