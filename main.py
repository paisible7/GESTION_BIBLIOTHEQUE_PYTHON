#importation de livre et utilisateur
import livre
import utilisateur

#fonction menu() qui affiche le mennu et recupere le choix du user
def menu():
    print("1. Ajouter un livre\n")
    print("2. Chercher un livre\n")
    print("3. Supprimer un livre\n")
    print("4. Afficher les livres\n")
    print("5. Emprunter un livre\n")
    print("6. Retourner un livre\n")
    print("7. Afficher l'historique\n")
    print("8. Vérifier les retards\n")
    print("9. Modifier un livre\n")
    print("10. Afficher livre par categorie\n")
    print("11. Quitter le programme\n")
    choix = int(input("Sélectionner une option : "))
    return choix #retour du choix de l'utilisateur

def main():#fonction principale
    #le dictionnaire pour les fonctions selon le choix 
    menu_actions = {
        1: livre.ajouterLivre,
        2: livre.rechercherLivre,
        3: livre.supprimerLivre,
        4: livre.afficherLivres,
        5: livre.emprunterLivre,
        6: livre.retournerLivre,
        7: livre.afficherHistorique,
        8: livre.verifierRetards,
        9: livre.modifierLivre,
        10: livre.affLivCategorie
    }

    while True:
        choix = menu() #appel du menu
        if choix == 11:
            print("Vous avez quitté le programme\nMerci d'avoir utilisé")
            break
        elif choix in menu_actions:#condition qui appel la fonction à la clé selon le choix 
            menu_actions[choix]()
        else:
            print("Veuillez choisir une option valide\n")


if __name__ == "__main__": #appel de la fonction main si tout es ok
    main()
