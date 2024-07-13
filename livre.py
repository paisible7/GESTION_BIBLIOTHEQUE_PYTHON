import json
from datetime import datetime
import utilisateur

FICHIER_JSON = 'livres.json'
HISTORIQUE = 'historique.json'

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

livres = chargerLivres()


def chargerHistorique():
    try:
        with open(HISTORIQUE, 'r', encoding='utf-8') as fichier:
            historique = json.load(fichier)
        return historique
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def sauvegarderHistorique(historique):
    with open(HISTORIQUE, 'w', encoding='utf-8') as fichier:
        json.dump(historique, fichier, ensure_ascii=False, indent=4)


def afficherLivres():
    choix = int(input("Voulez-vous afficher tous les livres ou seulement les livres disponibles ?\n\t1. Tous\n\t2. Disponibles\nEntre votre choix : ").strip())
    
    if choix == 1:
        livres, _ = chargerLivres()
        if livres:
            for livre in livres:
                print(f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}")
        else:
            print("Aucun livre n'est enregistré")
    elif choix == 2:
        affLivDispo()
    elif choix == 3:
        affLivCategorie()
    else:
        print("Choix invalide, veuillez entrer '1' pour Tous ou '2' pour disponibles")


def affLivDispo():
    livres, _ = chargerLivres()
    livres_disponibles = [livre for livre in livres if livre['disponible']]
    
    if livres_disponibles:
        print("Livres disponibles :")
        for livre in livres_disponibles:
            print(f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}")
    else:
        print("Aucun livre n'est disponible")


def affLivCategorie():
    livres, _ = chargerLivres()
    if not livres:
        print("Aucun livre n'est enregistré")
        return

    categorie = input("Entrez la catégorie à afficher : ").strip()

    livres_par_categorie = [livre for livre in livres if livre['categorie'].lower() == categorie.lower()]

    if livres_par_categorie:
        print(f"Livres dans la catégorie '{categorie}' :")
        for livre in livres_par_categorie:
            print(f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}, Disponible: {'Oui' if livre['disponible'] else 'Non'}")
    else:
        print(f"Aucun livre trouvé dans la catégorie '{categorie}'")



def rechercherLivre():
    livres, _ = chargerLivres()
    livres_trouves = []

    criteres = input("entrer le critère de recherche(Titre, Auteur, Genre ou Disponibilité) : ")
    for livre in livres:
        if (criteres.lower() in livre['titre'].lower() or
            criteres.lower() in livre['auteur'].lower() or
            criteres.lower() in livre['genre'].lower() or
            criteres.lower() == 'disponible' and livre['disponible'] or
            criteres.lower() == 'non disponible' and not livre['disponible']):
            livres_trouves.append(livre)

        if livres_trouves:
            print("Livres trouvés : ")
            for livre in livres_trouves:
                print(f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}, Disponible: {'Oui' if livre['disponible'] else 'Non'}")
        else :
            print("Aucun livre correspondant aux critères de recherche n'a été trouvé")

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
    
def livreExiste(livres, titre, auteur):
    for livre in livres:
        if livre['titre'].lower() == titre.lower() and livre['auteur'].lower() == auteur.lower():
            return True
    return False


def validerCategorie(categorie):
    if categorie.isdigit():
        print("Écrivez correctement la catégorie du livre")
        return False
    else:
        return True


def ajouterLivre():

    statusLivre = True

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

    while True:
        categorieLivre = input("Entrez la catégorie du livre : ")
        if validerCategorie(categorieLivre):
            break

    livres, dernier_id = chargerLivres()

    if livreExiste(livres, titreLivre, auteurLivre):
        print("le livre existe déjà")
        return

    nouveau_id = dernier_id + 1
    livre = {"id": nouveau_id, "titre": titreLivre, "auteur": auteurLivre, "genre": genreLivre, "categorie": categorieLivre, "disponible" : statusLivre}
    livres.append(livre)
    sauvegarderLivres(livres)
    print(livres)
    print("Livre ajouté avec succès")


def supprimerLivre():
    livres, _ = chargerLivres()

    if not livres:
        print("Aucun livre n'est enregistré")
        return

    try:
        idLivre = int(input("Entrez l'ID du livre à supprimer : "))
    except ValueError:
        print("L'ID doit être un nombre entier")
        return

    livreDel = None
    for livre in livres:
        if livre['id'] == idLivre:
            livreDel = livre
            break

    if livreDel:
        livres.remove(livreDel)
        sauvegarderLivres(livres)
        print(f"Le livre avec l'ID {idLivre} a été supprimé avec succès")
    else:
        print(f"Aucun livre trouvé avec l'ID {idLivre}")

def emprunterLivre():
    livres, _ = chargerLivres()
    if not livres:
        print("Aucun livre n'est enregistré")
        return

    titreLivre = input("Entrez le titre du livre à emprunter : ").lower()
    
    livreEmprunt = None
    for livre in livres:
        if livre['titre'].lower() == titreLivre:
            livreEmprunt = livre
            break

    if livreEmprunt:
        if not livreEmprunt['disponible']:
            print(f"Le livre {titreLivre} est déjà emprunté")
        else:
            utilisateurs = utilisateur.chargerUtilisateurs()
            emprunteur = None
            while True:
                choix = input("1. Vérifier si l'utilisateur existe\n2. Ajouter un nouvel utilisateur\nChoisissez une option : ").strip()
                if choix == '1':
                    email = input("Entrez l'email de l'utilisateur : ").strip()
                    for user in utilisateurs:
                        if user['email'] == email:
                            emprunteur = user
                            break
                    if emprunteur:
                        print(f"Utilisateur trouvé : {emprunteur['nom']}, Email : {emprunteur['email']}, Téléphone : {emprunteur['tel']}")
                        break
                    else:
                        print("Utilisateur non trouvé. Essayez encore ou ajoutez un nouvel utilisateur.")
                elif choix == '2':
                    utilisateur.ajouterUtilisateur()
                    utilisateurs = utilisateur.chargerUtilisateurs()
                else:
                    print("Choix invalide, veuillez entrer '1' ou '2'")

            if emprunteur:
                livreEmprunt['disponible'] = False
                dateEmprunt = datetime.now().strftime("%Y-%m-%d")
                dateRetour = input("Entrez la date de retour (format AAAA-MM-JJ) : ")
                
                livreEmprunt['emprunt'] = {
                    "date_emprunt": dateEmprunt,
                    "date_retour": dateRetour,
                    "nom_emprunteur": emprunteur['nom'],
                    "email_emprunteur": emprunteur['email'],
                    "telephone_emprunteur": emprunteur['tel']
                }

                sauvegarderLivres(livres)
                ajouterHistorique(livreEmprunt, "emprunt")
                print(f"Le livre {titreLivre} a été emprunté avec succès jusqu'au {dateRetour}")
    else:
        print(f"Aucun livre trouvé avec comme titre : « {titreLivre} »")

def retournerLivre():
    livres, _ = chargerLivres()
    if not livres:
        print("Aucun livre n'est enregistré")
        return

    try:
        idLivre = int(input("Entrez l'ID du livre à retourner : "))
    except ValueError:
        print("L'ID doit être un nombre entier")
        return

    livre_a_retourner = None
    for livre in livres:
        if livre['id'] == idLivre:
            livre_a_retourner = livre
            break

    if livre_a_retourner:
        if livre_a_retourner['disponible']:
            print(f"Le livre avec l'ID {idLivre} est déjà disponible")
        else:
            livre_a_retourner['disponible'] = True
            if 'emprunt' in livre_a_retourner:
                ajouterHistorique(livre_a_retourner, "retour")
                del livre_a_retourner['emprunt']
            sauvegarderLivres(livres)
            print(f"Le livre avec l'ID {idLivre} a été retourné avec succès et les informations de l'emprunteur ont été supprimées")
    else:
        print(f"Aucun livre trouvé avec l'ID {idLivre}")



def ajouterHistorique(livre, action):
    historique = chargerHistorique()
    if action == "emprunt":
        entree = {
            "action": "emprunt",
            "titre": livre['titre'],
            "auteur": livre['auteur'],
            "nom_emprunteur": livre['emprunt']['nom_emprunteur'],
            "date_emprunt": livre['emprunt']['date_emprunt'],
            "date_retour": livre['emprunt']['date_retour']
        }
    elif action == "retour":
        entree = {
            "action": "retour",
            "titre": livre['titre'],
            "auteur": livre['auteur'],
            "nom_emprunteur": livre['emprunt']['nom_emprunteur'],
            "date_retour": datetime.now().strftime("%Y-%m-%d")
        }
    historique.append(entree)
    sauvegarderHistorique(historique)

def afficherHistorique():
    historique = chargerHistorique()
    if historique:
        for entree in historique:
            print(f"Action: {entree['action']}, Titre: {entree['titre']}, Auteur: {entree['auteur']}, Emprunteur: {entree['nom_emprunteur']}, Date Emprunt: {entree.get('date_emprunt', 'N/A')}, Date Retour: {entree.get('date_retour', 'N/A')}")
    else:
        print("Aucun historique n'est enregistré")

def verifierRetards():
    livres, _ = chargerLivres()
    if not livres:
        print("Aucun livre n'est enregistré")
        return
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    retardataires = []
    for livre in livres:
        if 'emprunt' in livre:
            date_retour = livre['emprunt']['date_retour']
            if datetime.strptime(date_retour, "%Y-%m-%d") < datetime.strptime(aujourd_hui, "%Y-%m-%d"):
                retardataires.append(livre)
    if retardataires:
        print("Livres en retard : ")
        for livre in retardataires:
            print(f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Emprunteur: {livre['emprunt']['nom_emprunteur']}, Date de retour prévue: {livre['emprunt']['date_retour']}")
    else:
        print("Aucun livre en retard")


def modifierLivre():
    livres, _ = chargerLivres()
    
    if not livres:
        print("Aucun livre n'est enregistré")
        return

    try:
        idLivre = int(input("Entrez l'ID du livre à modifier : "))
    except ValueError:
        print("L'ID doit être un nombre entier")
        return

    livre_a_modifier = None
    for livre in livres:
        if livre['id'] == idLivre:
            livre_a_modifier = livre
            break

    if livre_a_modifier:
        nouveau_titre = input(f"Entrez le nouveau titre (actuel: {livre_a_modifier['titre']}) : ").strip()
        nouveau_auteur = input(f"Entrez le nouvel auteur (actuel: {livre_a_modifier['auteur']}) : ").strip()
        nouveau_genre = input(f"Entrez le nouveau genre (actuel: {livre_a_modifier['genre']}) : ").strip()

        if nouveau_titre:
            livre_a_modifier['titre'] = nouveau_titre
        if nouveau_auteur:
            livre_a_modifier['auteur'] = nouveau_auteur
        if nouveau_genre:
            livre_a_modifier['genre'] = nouveau_genre

        sauvegarderLivres(livres)
        print(f"Le livre avec l'ID {idLivre} a été modifié avec succès")
    else:
        print(f"Aucun livre trouvé avec l'ID {idLivre}")



