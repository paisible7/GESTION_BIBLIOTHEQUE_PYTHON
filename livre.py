livres = []

def chargerLivres():
    pass

def sauvegarderLivres():
    pass

def afficherLivres():
    pass

def validerTitre(titre):
    if titre.isdigit():
        print("Écrivez correctement le titre du livre")
        return False
    else:
        return True

def validerAuteur(auteur):
    if auteur.isdigit():
        print("Écrivez correctement le nom de l'auteur")
        return False
    else :
        return True

def validerGenre(genre):
    if genre.isdigit():
        print("Écrivez correctement le genre du livre")
        return False
    else :
        return True
    
def livreExiste():
    pass

def ajouterLivre():
    while True:
        titreLivre = input("entrer le titre du livre : ")
        if validerTitre(titreLivre):
            break

    while True:
        auteurLivre = input("entrer l'auteur du livre : ")
        if validerAuteur(auteurLivre):
            break

    while True:
        genreLivre = input("entrer le genre du livre : ")
        if validerTitre(genreLivre):
            break
    
    livre = {"titre": titreLivre, "auteur": auteurLivre, "genre": genreLivre}
    livres.append(livre)
    print(livres)
    print("Livre ajouté avec succès")

        