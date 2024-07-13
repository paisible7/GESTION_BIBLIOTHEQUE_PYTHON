import json
from datetime import datetime
import utilisateur
import tkinter as tk
from tkinter import messagebox, simpledialog

FICHIER_JSON = 'livres.json'
HISTORIQUE = 'historique.json'

# Functions for handling JSON data
def chargerLivres():
    try:
        with open(FICHIER_JSON, 'r', encoding='utf-8') as fichier:
            livres = json.load(fichier)
        if livres:
            dernier_id = max(livre['id'] for livre in livres)
        else:
            dernier_id = 0
        return livres, dernier_id
    except FileNotFoundError:
        return [], 0
    except json.JSONDecodeError:
        return [], 0

def sauvegarderLivres(livres):
    with open(FICHIER_JSON, 'w', encoding='utf-8') as fichier:
        json.dump(livres, fichier, ensure_ascii=False, indent=4)

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

# Tkinter GUI
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GESTION BIBLIOTHEQUE")
        
        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        root['bg'] = "#000040"
        root.geometry("550x550")
        tk.Button(self.root, text="Ajouter un livre", command=self.ajouterLivre).pack(pady=10)
        tk.Button(self.root, text="Chercher un livre", command=self.rechercherLivre).pack(pady=10)
        tk.Button(self.root, text="Supprimer un livre", command=self.supprimerLivre).pack(pady=10)
        tk.Button(self.root, text="Afficher les livres", command=self.afficherLivres).pack(pady=10)
        tk.Button(self.root, text="Emprunter un livre", command=self.emprunterLivre).pack(pady=10)
        tk.Button(self.root, text="Retourner un livre", command=self.retournerLivre).pack(pady=10)
        tk.Button(self.root, text="Afficher l'historique", command=self.afficherHistorique).pack(pady=10)
        tk.Button(self.root, text="Vérifier les retards", command=self.verifierRetards).pack(pady=10)
        tk.Button(self.root, text="Modifier un livre", command=self.modifierLivre).pack(pady=10)
        tk.Button(self.root, text="Quitter", command=self.root.quit).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def ajouterLivre(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Ajouter un livre").pack(pady=10)
        
        titre = simpledialog.askstring("Titre", "Entrez le titre du livre:")
        if not titre:
            self.main_menu()
            return
        
        auteur = simpledialog.askstring("Auteur", "Entrez l'auteur du livre:")
        if not auteur:
            self.main_menu()
            return
        
        genre = simpledialog.askstring("Genre", "Entrez le genre du livre:")
        if not genre:
            self.main_menu()
            return

        categorie = simpledialog.askstring("Catégorie", "Entrez la catégorie du livre:")
        if not categorie:
            self.main_menu()
            return

        livres, dernier_id = chargerLivres()
        if any(livre['titre'].lower() == titre.lower() and livre['auteur'].lower() == auteur.lower() for livre in livres):
            messagebox.showinfo("Erreur", "Le livre existe déjà")
            self.main_menu()
            return

        nouveau_id = dernier_id + 1
        livre = {"id": nouveau_id, "titre": titre, "auteur": auteur, "genre": genre, "categorie": categorie, "disponible": True}
        livres.append(livre)
        sauvegarderLivres(livres)
        
        messagebox.showinfo("Succès", "Livre ajouté avec succès")
        self.main_menu()

    def rechercherLivre(self):
        self.clear_frame()
        
        criteres = simpledialog.askstring("Recherche", "Entrez le critère de recherche (Titre, Auteur, Genre ou Disponibilité):")
        if not criteres:
            self.main_menu()
            return
        
        livres, _ = chargerLivres()
        livres_trouves = [livre for livre in livres if 
                          criteres.lower() in livre['titre'].lower() or
                          criteres.lower() in livre['auteur'].lower() or
                          criteres.lower() in livre['genre'].lower() or
                          (criteres.lower() == 'disponible' and livre['disponible']) or
                          (criteres.lower() == 'non disponible' and not livre['disponible'])]
        
        if livres_trouves:
            result = "\n".join([f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}, Disponible: {'Oui' if livre['disponible'] else 'Non'}" for livre in livres_trouves])
            messagebox.showinfo("Livres trouvés", result)
        else:
            messagebox.showinfo("Aucun livre trouvé", "Aucun livre correspondant aux critères de recherche n'a été trouvé")
        self.main_menu()

    def supprimerLivre(self):
        self.clear_frame()
        
        livres, _ = chargerLivres()
        if not livres:
            messagebox.showinfo("Erreur", "Aucun livre n'est enregistré")
            self.main_menu()
            return

        idLivre = simpledialog.askinteger("ID Livre", "Entrez l'ID du livre à supprimer:")
        if idLivre is None:
            self.main_menu()
            return

        livreDel = next((livre for livre in livres if livre['id'] == idLivre), None)
        if livreDel:
            livres.remove(livreDel)
            sauvegarderLivres(livres)
            messagebox.showinfo("Succès", f"Le livre avec l'ID {idLivre} a été supprimé avec succès")
        else:
            messagebox.showinfo("Erreur", f"Aucun livre trouvé avec l'ID {idLivre}")
        self.main_menu()

    def afficherLivres(self):
        self.clear_frame()
        
        choix = simpledialog.askinteger("Affichage", "Voulez-vous afficher tous les livres ou seulement les livres disponibles ?\n1. Tous\n2. Disponibles")
        if choix is None:
            self.main_menu()
            return
        
        livres, _ = chargerLivres()
        if choix == 1:
            result = "\n".join([f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}" for livre in livres]) if livres else "Aucun livre n'est enregistré"
        elif choix == 2:
            livres_disponibles = [livre for livre in livres if livre['disponible']]
            result = "\n".join([f"ID: {livre['id']}, Titre: {livre['titre']}, Auteur: {livre['auteur']}, Genre: {livre['genre']}" for livre in livres_disponibles]) if livres_disponibles else "Aucun livre n'est disponible"
        else:
            messagebox.showinfo("Erreur", "Choix invalide")
            self.main_menu()
            return

        messagebox.showinfo("Livres", result)
        self.main_menu()

    def emprunterLivre(self):
        self.clear_frame()
    
        livres, _ = chargerLivres()
        if not livres:
            messagebox.showinfo("Erreur", "Aucun livre n'est enregistré")
            self.main_menu()
            return

        titreLivre = simpledialog.askstring("Titre", "Entrez le titre du livre à emprunter:")
        if not titreLivre:
            self.main_menu()
            return
    
        livreEmprunt = next((livre for livre in livres if livre['titre'].lower() == titreLivre.lower()), None)
        if livreEmprunt:
            if not livreEmprunt['disponible']:
                messagebox.showinfo("Erreur", f"Le livre {titreLivre} est déjà emprunté")
            else:
                utilisateurs = utilisateur.chargerUtilisateurs()
                emprunteur = None
                while True:
                    choix = simpledialog.askinteger("Utilisateur", "1. Vérifier si l'utilisateur existe\n2. Ajouter un nouvel utilisateur")
                    if choix is None:
                        self.main_menu()
                        return
                    if choix == 1:
                        email = simpledialog.askstring("Email", "Entrez l'email de l'utilisateur:")
                        if not email:
                            self.main_menu()
                            return
                        emprunteur = next((user for user in utilisateurs if user['email'] == email), None)
                        if emprunteur:
                            messagebox.showinfo("Succès", f"L'utilisateur {emprunteur['nom']} existe")
                            break
                        else:
                            messagebox.showinfo("Erreur", "Utilisateur non trouvé")
                    elif choix == 2:
                        email = simpledialog.askstring("Email", "Entrez l'email de l'utilisateur:")
                        if not email:
                            self.main_menu()
                            return
                        nom = simpledialog.askstring("Nom", "Entrez le nom de l'utilisateur:")
                        if not nom:
                            self.main_menu()
                            return
                        tel = simpledialog.askstring("Telephone", "Entrez le numero de telephone :")
                        if not tel:
                            self.main_menu()
                            return
                        emprunteur = {"nom": nom, "email": email, "tel": tel}
                        utilisateurs.append(emprunteur)
                        utilisateur.sauvegarderUtilisateurs(utilisateurs)
                        messagebox.showinfo("Succès", "Utilisateur ajouté avec succès")
                        break
                    else:
                        messagebox.showinfo("Erreur", "Choix invalide")

                if emprunteur:
                    livreEmprunt['disponible'] = False
                    date_emprunt = datetime.now().strftime("%d-%m-%Y")
                    date_retour = simpledialog.askstring("date", "Entrez la date de retour (format JJ-MM-AAAA) : ")
                    livreEmprunt['emprunt'] = {
                        "date_emprunt": date_emprunt,
                        "date_retour": date_retour,
                        "nom_emprunteur": emprunteur['nom'],
                        "email_emprunteur": emprunteur['email'],
                        "telephone_emprunteur": emprunteur['tel']
                    }
                    historique = chargerHistorique()
                    historique.append({"titre": titreLivre, "emprunteur": emprunteur, "date_emprunt": date_emprunt, "date_retour": date_retour})
                    sauvegarderHistorique(historique)
                    sauvegarderLivres(livres)
                    messagebox.showinfo("Succès", f"Le livre {titreLivre} a été emprunté avec succès jusqu'au {date_retour}")
        else:
            messagebox.showinfo("Erreur", f"Aucun livre trouvé avec le titre {titreLivre}")
        self.main_menu()

    def retournerLivre(self):
        self.clear_frame()
        
        titreLivre = simpledialog.askstring("Titre", "Entrez le titre du livre à retourner:")
        if not titreLivre:
            self.main_menu()
            return

        livres, _ = chargerLivres()
        livreRetour = next((livre for livre in livres if livre['titre'].lower() == titreLivre.lower()), None)
        if livreRetour:
            if livreRetour['disponible']:
                messagebox.showinfo("Erreur", f"Le livre {titreLivre} n'a pas été emprunté")
            else:
                livreRetour['disponible'] = True
                del livreRetour['emprunt']
                sauvegarderLivres(livres)
                historique = chargerHistorique()
                emprunt = next((item for item in historique if item['titre'].lower() == titreLivre.lower() and item['date_retour'] is None), None)
                if emprunt:
                    emprunt['date_retour'] = datetime.now().strftime("%d-%m-%Y")
                    
                    sauvegarderHistorique(historique)
                    sauvegarderLivres(livres)
                messagebox.showinfo("Succès", f"Le livre {titreLivre} a été retourné avec succès")
        else:
            messagebox.showinfo("Erreur", f"Aucun livre trouvé avec le titre {titreLivre}")
        self.main_menu()

    def afficherHistorique(self):
        self.clear_frame()
        
        historique = chargerHistorique()
        if historique:
            result = "\n".join([f"Titre: {emprunt['titre']}, Emprunteur: {emprunt['emprunteur']['nom']} ({emprunt['emprunteur']['email']}), Date d'emprunt: {emprunt['date_emprunt']}, Date de retour: {emprunt['date_retour'] or 'Non retourné'}" for emprunt in historique])
        else:
            result = "Aucun emprunt enregistré"
        
        messagebox.showinfo("Historique", result)
        self.main_menu()

    def verifierRetards(self):
        self.clear_frame()
        
        historique = chargerHistorique()
        if historique:
            retardataires = [emprunt for emprunt in historique if not emprunt['date_retour'] and (datetime.now() - datetime.strptime(emprunt['date_emprunt'], "%Y-%m-%d")).days > 30]
            if retardataires:
                result = "\n".join([f"Titre: {emprunt['titre']}, Emprunteur: {emprunt['emprunteur']['nom']} ({emprunt['emprunteur']['email']}), Date d'emprunt: {emprunt['date_emprunt']}" for emprunt in retardataires])
                messagebox.showinfo("Retards", result)
            else:
                messagebox.showinfo("Aucun retard", "Aucun livre en retard")
        else:
            messagebox.showinfo("Erreur", "Aucun emprunt enregistré")
        self.main_menu()

    def modifierLivre(self):
        self.clear_frame()
        
        livres, _ = chargerLivres()
        if not livres:
            messagebox.showinfo("Erreur", "Aucun livre n'est enregistré")
            self.main_menu()
            return

        idLivre = simpledialog.askinteger("ID Livre", "Entrez l'ID du livre à modifier:")
        if idLivre is None:
            self.main_menu()
            return

        livreMod = next((livre for livre in livres if livre['id'] == idLivre), None)
        if livreMod:
            nouveauTitre = simpledialog.askstring("Titre", f"Entrez le nouveau titre (actuel: {livreMod['titre']}):")
            if nouveauTitre:
                livreMod['titre'] = nouveauTitre

            nouvelAuteur = simpledialog.askstring("Auteur", f"Entrez le nouvel auteur (actuel: {livreMod['auteur']}):")
            if nouvelAuteur:
                livreMod['auteur'] = nouvelAuteur

            nouveauGenre = simpledialog.askstring("Genre", f"Entrez le nouveau genre (actuel: {livreMod['genre']}):")
            if nouveauGenre:
                livreMod['genre'] = nouveauGenre

            nouvelleCategorie = simpledialog.askstring("Catégorie", f"Entrez la nouvelle catégorie (actuelle: {livreMod['categorie']}):")
            if nouvelleCategorie:
                livreMod['categorie'] = nouvelleCategorie

            sauvegarderLivres(livres)
            messagebox.showinfo("Succès", f"Le livre avec l'ID {idLivre} a été modifié avec succès")
        else:
            messagebox.showinfo("Erreur", f"Aucun livre trouvé avec l'ID {idLivre}")
        self.main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
