import json

FICHIER_JSON = 'livres.json'

def chargerLivres():
    try :
        with open(FICHIER_JSON, 'r', encoding='utf-8') as fichier:
            livres = json.load(fichier)
        if livres :
            dernier_id = max(livre['id'] for livre in livres)
        else :
            dernier_id = 0
        return livres, dernier_id
    except FileNotFoundError :
        return [], 0
    except json.JSONDecodeError :
        return [], 0

def sauvegarderLivres(livres):
    with open(FICHIER_JSON, 'w', encoding='utf-8') as fichier :
        json.dump(livres, fichier, ensure_ascii=False, indent=4)

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

    livres, dernier_id = chargerLivres()

    nouveau_id = dernier_id + 1
    livre = {"id": nouveau_id, "titre": titreLivre, "auteur": auteurLivre, "genre": genreLivre}
    livres.append(livre)
    sauvegarderLivres(livres)
    print(livres)
    print("Livre ajouté avec succès")

        