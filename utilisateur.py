import json

FICHIER_UTILISATEURS = 'utilisateurs.json'

def chargerUtilisateurs():
    try:
        with open(FICHIER_UTILISATEURS, 'r', encoding='utf-8') as fichier:
            utilisateurs = json.load(fichier)
        return utilisateurs
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def sauvegarderUtilisateurs(utilisateurs):
    with open(FICHIER_UTILISATEURS, 'w', encoding='utf-8') as fichier:
        json.dump(utilisateurs, fichier, ensure_ascii=False, indent=4)

def ajouterUtilisateur():
    utilisateurs = chargerUtilisateurs()

    nom = input("Entrez le nom de l'utilisateur : ").strip()
    email = input("Entrez l'email de l'utilisateur : ").strip()
    tel = input("Entrez le numéro de téléphone de l'utilisateur : ").strip()

    utilisateur = {"nom": nom, "email": email, "tel": tel}
    utilisateurs.append(utilisateur)
    sauvegarderUtilisateurs(utilisateurs)
    print("Utilisateur ajouté avec succès")

