from tkinter import *

def ouvrir_gestion_compte(fenetre_principale):
    fenetre_gestion_compte = Toplevel(fenetre_principale)
    fenetre_gestion_compte.title("Gestion de compte")
    fenetre_gestion_compte.geometry("500x500")

    Label(fenetre_gestion_compte, text= "Gestion de Compte", font=("", 18)).pack(expand=True)

    frm_montant = Frame(fenetre_gestion_compte)
    frm_montant.pack(expand = True)
    lbl_montant = Label(frm_montant, text = "Montant : 1500 €", bg = "green")
    lbl_montant.pack(anchor = CENTER)




    def action_virement():
        virement(fenetre_gestion_compte)

    Button(fenetre_gestion_compte, text = "Virement", command = action_virement).pack(expand= True)

    Button(fenetre_gestion_compte, text = "Fermer", command = fenetre_gestion_compte.destroy).pack(expand = True)


from tkinter import *

def virement(fenetre_principale) :
    fenetre_virement = Toplevel(fenetre_principale)
    fenetre_virement.title("Virement")
    fenetre_virement.geometry("500x500")
    
    Label(fenetre_virement, text="Virement", font=("", 18)).pack(pady=20)

    frm_virement = Frame(fenetre_virement)
    frm_virement.pack(fill=X, padx=30, pady=20) 

    #Compte depart

    frm_depart = Frame(frm_virement)
    frm_depart.pack(anchor=W)
    
    lbl_compte_dep = Label(frm_depart, text="Compte de départ :", font=("", 16))
    lbl_compte_dep.pack(side=LEFT, padx = (40,0) , pady =5)
    

    liste_compte_depart = Listbox(frm_depart, height=2, font=("", 14)) 
    liste_compte_depart.insert(1, "A")
    liste_compte_depart.insert(2, "B")
    liste_compte_depart.pack(side=LEFT)

    #Compte destinataire

    frm_dest = Frame(frm_virement)
    frm_dest.pack(anchor=W)

    lbl_compte_dest = Label(frm_dest, text = "Compte destinataire :", font = ("", 16))
    lbl_compte_dest.pack(side = LEFT, padx = (20,0), pady = (10, 50))


    liste_compte_dest = Listbox(frm_dest, height = 2, font = ("", 14))
    liste_compte_dest.insert(1, "C")
    liste_compte_dest.insert(2, "D")
    liste_compte_dest.pack(side = LEFT)







    Button(fenetre_virement, text = "Fermer", command = fenetre_virement.destroy).pack(expand= True)

    