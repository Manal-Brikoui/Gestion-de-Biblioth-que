import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from src.bibliotheque import Bibliotheque
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta

#  Gestion PIL et chargement images
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
    try:
        RESAMPLE_MODE = Image.Resampling.LANCZOS
    except AttributeError:
        RESAMPLE_MODE = Image.ANTIALIAS
except ImportError:
    PIL_AVAILABLE = False

def charger_image(nom_fichier, largeur=None, hauteur=None):
    dossier_script = os.path.dirname(os.path.abspath(sys.argv[0]))
    dossier_assets = os.path.abspath(os.path.join(dossier_script, "..", "assets"))
    chemin = os.path.join(dossier_assets, nom_fichier)
    if not os.path.exists(chemin):
        print(f"Erreur chargement image {nom_fichier}: fichier introuvable.")
        return None
    try:
        if PIL_AVAILABLE:
            img = Image.open(chemin)
            if largeur and hauteur:
                img = img.resize((largeur, hauteur), RESAMPLE_MODE)
            return ImageTk.PhotoImage(img)
        else:
            return tk.PhotoImage(file=chemin)
    except Exception as e:
        print(f"Erreur chargement image {nom_fichier}: {e}")
        return None

#  Création de la fenêtre avant chargement des images
fenetre = tk.Tk()
fenetre.title("\U0001F4DA Gestion de Bibliothèque ENSAO")
fenetre.geometry("1200x750")  # élargi pour plus de colonnes
fenetre.configure(bg="white")

# Chargement images (après création fenetre Tk)
liste_images = [
    "stack-of-books.png", "membres.png", "statistique.png",
    "check.png", "trash.png", "emprunter.png", "retourner.png",
    "pie-chart.png", "bar-chart.png","check.png",
     "line-chart.png", "add-user.png","ajouter-livre.png"
]

icones_brut = {}
for img_nom in liste_images:
    cle = img_nom.split('.')[0]
    icones_brut[cle] = charger_image(img_nom, 24, 24)

icones = {
    "livres": icones_brut.get("stack-of-books"),
    "membres": icones_brut.get("membres"),
    "statistique": icones_brut.get("statistique"),
    "done": icones_brut.get("check"),
    "supprimer": icones_brut.get("trash"),
    "emprunter": icones_brut.get("emprunter"),
    "retourner": icones_brut.get("retourner"),
    "diagramme_genre": icones_brut.get("pie-chart"),
    "diagramme_auteurs": icones_brut.get("bar-chart"),
    "diagramme_emprunts_30j": icones_brut.get("line-chart"),  # remplacé diagramme.png par pie-chart
    "ajouterpersonne": icones_brut.get("add-user"),
    "ajouterlivre":icones_brut.get("ajouter-livre")
}

# Suite de ton code avec l'utilisation des icônes

notebook = ttk.Notebook(fenetre)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

style_label = {"font": ("Arial", 10), "bg": "white", "fg": "#003366"}
style_title = {"font": ("Arial", 12, "bold"), "bg": "white", "fg": "#003366"}

# STYLE ttk pour Treeview
style = ttk.Style(fenetre)
style.theme_use("clam")  # thème personnalisable

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white",
                font=("Arial", 10))

style.map("Treeview",
          background=[("selected", "#cce6ff")],
          foreground=[("selected", "black")])

style.configure("Treeview.Heading",
                background="#003366",
                foreground="white",
                font=("Arial", 11, "bold"))

# Tags pour lignes alternées
style.configure("oddrow", background="#f2f9ff")
style.configure("evenrow", background="white")

# Onglet Livres
cadre_livre = tk.Frame(notebook, bg="white")
notebook.add(cadre_livre, text=" Livres", image=icones["livres"], compound="left")

fields_livre = {}
for champ in ["ISBN", "Titre", "Auteur", "Annee", "Genre"]:
    tk.Label(cadre_livre, text=champ, **style_label).pack(anchor="w", padx=10)
    entry = tk.Entry(cadre_livre, width=50)
    entry.pack(padx=10, pady=2)
    fields_livre[champ.lower()] = entry

def afficher_message(texte):
    affichage.insert(tk.END, texte + "\n")
    affichage.see(tk.END)
def vider_champs_livre():
    for champ in fields_livre.values():
        champ.delete(0, tk.END)

def ajouter_livre():
    try:
        livre = biblio.Livre(
            fields_livre["isbn"].get().strip(),
            fields_livre["titre"].get().strip(),
            fields_livre["auteur"].get().strip(),
            fields_livre["annee"].get().strip(),
            fields_livre["genre"].get().strip(),
            "disponible"
        )
        biblio.ajouter_livre(livre)
        afficher_message("Livre ajouté avec statut 'Disponible'.")
        maj_tout()
        vider_champs_livre()  # Vide les champs après ajout
    except Exception as e:
        afficher_message(f"Erreur : {e}")

    except Exception as e:
        afficher_message(f"Erreur : {e}")
def supprimer_livre():
    try:
        biblio.supprimer_livre(fields_livre["isbn"].get().strip())
        afficher_message("Livre supprimé.")
        maj_tout()

        # Vider les champs après suppression
        for champ in fields_livre.values():
            champ.delete(0, tk.END)

    except Exception as e:
        afficher_message(f"Erreur : {e}")

#  Encadré boutons d'action Livres (ajouter / supprimer) côte à côte
frame_boutons_livre = tk.Frame(cadre_livre, bg="white")
frame_boutons_livre.pack(pady=5)

btn_ajouter_livre = tk.Button(frame_boutons_livre, text=" Ajouter Livre", image=icones["ajouterlivre"], compound="left",
                              bg="#009933", fg="white", font=("Arial", 10, "bold"), command=ajouter_livre)
btn_ajouter_livre.pack(side="left", padx=10)

btn_supprimer_livre = tk.Button(frame_boutons_livre, text=" Supprimer Livre", image=icones["supprimer"], compound="left",
                                bg="#cc0000", fg="white", font=("Arial", 10, "bold"), command=supprimer_livre)
btn_supprimer_livre.pack(side="left", padx=10)

#  Onglet Membres
cadre_membre = tk.Frame(notebook, bg="white")
notebook.add(cadre_membre, text=" Membres", image=icones["membres"], compound="left")

tk.Label(cadre_membre, text="ID Membre", **style_label).pack(anchor="w", padx=10)
id_entry = tk.Entry(cadre_membre, width=30)
id_entry.pack(padx=10)

tk.Label(cadre_membre, text="Nom", **style_label).pack(anchor="w", padx=10)
nom_entry = tk.Entry(cadre_membre, width=30)
nom_entry.pack(padx=10, pady=3)

def enregistrer_membre():
    try:
        membre = biblio.Membre(id_entry.get().strip(), nom_entry.get().strip())
        biblio.enregistrer_membre(membre)
        afficher_message("Membre enregistré.")
        maj_tout()
    except Exception as e:
        afficher_message(f"Erreur : {e}")

def supprimer_membre():
    try:
        biblio.supprimer_membre(id_entry.get().strip())
        afficher_message("🗑 Membre supprimé.")
        maj_tout()
        # Vider les champs après suppression
        id_entry.delete(0, tk.END)
        nom_entry.delete(0, tk.END)
    except Exception as e:
        afficher_message(f"Erreur : {e}")


# Encadré boutons d'action Membres (ajouter / supprimer) côte à côte
frame_boutons_membre = tk.Frame(cadre_membre, bg="white")
frame_boutons_membre.pack(pady=5)

btn_ajouter_membre = tk.Button(frame_boutons_membre, text=" Ajouter Membre", image=icones["ajouterpersonne"], compound="left",
                               bg="#009933", fg="white", font=("Arial", 10, "bold"), command=enregistrer_membre)
btn_ajouter_membre.pack(side="left", padx=10)

btn_supprimer_membre = tk.Button(frame_boutons_membre, text=" Supprimer Membre", image=icones["supprimer"], compound="left",
                                 bg="#cc0000", fg="white", font=("Arial", 10, "bold"), command=supprimer_membre)
btn_supprimer_membre.pack(side="left", padx=10)


# Combobox livres disponibles
livres_disponibles_cb = ttk.Combobox(cadre_membre, width=50, state="readonly")
tk.Label(cadre_membre, text="Livres disponibles", **style_label).pack(anchor="w", padx=10)
livres_disponibles_cb.pack(pady=2)

# Listbox livres empruntés par le membre
tk.Label(cadre_membre, text="Livres empruntés", **style_label).pack(anchor="w", padx=10)
livres_empruntes_listbox = tk.Listbox(cadre_membre, width=50, height=6)
livres_empruntes_listbox.pack(pady=2)

def rafraichir_livres_disponibles():
    livres = [f"{livre.isbn} - {livre.titre}" for livre in biblio.livres.values() if livre.statut == "disponible"]
    livres_disponibles_cb['values'] = livres
    livres_disponibles_cb.set(livres[0] if livres else '')

def rafraichir_livres_empruntes():
    livres_empruntes_listbox.delete(0, tk.END)
    id_membre = id_entry.get().strip()
    if id_membre in biblio.membres:
        empruntes = biblio.membres[id_membre].livres_empruntes
        for isbn in empruntes:
            if isbn in biblio.livres:
                titre = biblio.livres[isbn].titre
                livres_empruntes_listbox.insert(tk.END, f"{isbn} - {titre}")

def vider_champs_membre():
    id_entry.delete(0, tk.END)
    nom_entry.delete(0, tk.END)
    livres_empruntes_listbox.delete(0, tk.END)
    livres_disponibles_cb.set('')


def emprunter_livre():
    id_m = id_entry.get().strip()
    if not id_m:
        afficher_message("Veuillez saisir l'ID du membre.")
        return
    if not livres_disponibles_cb.get():
        afficher_message("Veuillez sélectionner un livre disponible.")
        return
    isbn = livres_disponibles_cb.get().split(" - ")[0]
    try:
        biblio.emprunter_livre(isbn, id_m)
        afficher_message(f"Livre {isbn} emprunté.")
        maj_tout()
        vider_champs_membre()  # vider les champs après emprunt
    except Exception as e:
        afficher_message(f"{e}")

def retourner_livre():
    id_m = id_entry.get().strip()
    selection = livres_empruntes_listbox.curselection()
    if not id_m:
        afficher_message("Veuillez saisir l'ID du membre.")
        return
    if not selection:
        afficher_message("Veuillez sélectionner un livre emprunté.")
        return
    isbn = livres_empruntes_listbox.get(selection[0]).split(" - ")[0]
    try:
        biblio.retourner_livre(isbn, id_m)
        afficher_message(f"Livre {isbn} retourné.")
        maj_tout()
        vider_champs_membre()  # vider les champs après retour
    except Exception as e:
        afficher_message(f"{e}")

# Encadré boutons Emprunter / Retourner horizontalement
frame_emprunt_retour = tk.Frame(cadre_membre, bg="white")
frame_emprunt_retour.pack(pady=5)

btn_emprunter = tk.Button(frame_emprunt_retour, text=" Emprunter livre", image=icones["emprunter"], compound="left",
                          bg="#cc6600", fg="white", font=("Arial", 10, "bold"), command=emprunter_livre)
btn_emprunter.pack(side="left", padx=10)

btn_retourner = tk.Button(frame_emprunt_retour, text=" Retourner livre", image=icones["retourner"], compound="left",
                          bg="#336600", fg="white", font=("Arial", 10, "bold"), command=retourner_livre)
btn_retourner.pack(side="left", padx=10)

# Mise à jour dynamique des listes quand on quitte le champ ID membre
id_entry.bind("<FocusOut>", lambda e: (rafraichir_livres_empruntes(), rafraichir_livres_disponibles()))

#Onglet Statistiques
cadre_stats = tk.Frame(notebook, bg="white")
notebook.add(cadre_stats, text=" Statistiques", image=icones["statistique"], compound="left")

tk.Label(cadre_stats, text="Visualisations Statistiques", font=("Arial", 14, "bold"), bg="white", fg="#003366").pack(pady=10)

def diagramme_genre():
    genres = [livre.genre for livre in biblio.livres.values()]
    compteur = Counter(genres)
    if not compteur:
        messagebox.showinfo("Info", "Aucun livre trouvé.")
        return
    plt.figure(figsize=(6, 6))
    plt.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%', startangle=90)
    plt.title("Répartition des Livres par Genre")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def histogramme_auteurs():
    auteurs = [livre.auteur for livre in biblio.livres.values()]
    compteur = Counter(auteurs)
    top = compteur.most_common(10)
    if not top:
        messagebox.showinfo("Info", "Aucun auteur trouvé.")
        return
    noms, quantites = zip(*top)
    plt.figure(figsize=(10, 5))
    plt.bar(noms, quantites, color='skyblue')
    plt.title("Top 10 Auteurs les plus populaires")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def courbe_emprunts_30j():
    aujourd_hui = datetime.now().date()
    depuis = aujourd_hui - timedelta(days=30)
    dates = []
    for entry in biblio.historique:
        date_str, isbn, id_membre, action = entry
        if action == "emprunt":
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date_obj >= depuis:
                    dates.append(date_obj)
            except:
                continue
    compteur = Counter(dates)
    jours = [depuis + timedelta(days=i) for i in range(31)]
    valeurs = [compteur.get(j, 0) for j in jours]
    plt.figure(figsize=(12, 5))
    plt.plot(jours, valeurs, marker='o', linestyle='-', color='green')
    plt.title("Activité des Emprunts (30 derniers jours)")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
btn_genre = tk.Button(cadre_stats, text=" Diagramme par Genre", image=icones["diagramme_genre"], compound="left",
                      bg="#0059b3", fg="white", font=("Arial", 10, "bold"), width=210, command=diagramme_genre)
btn_genre.pack(pady=5)

btn_auteurs = tk.Button(cadre_stats, text=" Top 10 Auteurs", image=icones["diagramme_auteurs"], compound="left",
                        bg="#0059b3", fg="white", font=("Arial", 10, "bold"), width=210, command=histogramme_auteurs)
btn_auteurs.pack(pady=5)

btn_emprunts = tk.Button(cadre_stats, text=" Activité des emprunts (30j)", image=icones["diagramme_emprunts_30j"], compound="left",
                         bg="#0059b3", fg="white", font=("Arial", 10, "bold"), width=210, command=courbe_emprunts_30j)
btn_emprunts.pack(pady=5)

#  Zone messages
affichage = tk.Text(fenetre, height=5, bg="white", fg="#333333", font=("Arial", 10))
affichage.pack(fill="x", padx=10, pady=5)

#  Tableau global enrichi
cadre_tableau = tk.Frame(fenetre, bg="white")
cadre_tableau.pack(pady=10, padx=10, fill="both", expand=True)

tk.Label(cadre_tableau, text=" Tous les Livres", font=("Arial", 12, "bold"), bg="white", fg="#003366").pack()

colonnes = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut", "ID Membre", "Nom Membre")
tableau_livres = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings", height=15)

for col in colonnes:
    tableau_livres.heading(col, text=col)

# Ajustement largeur colonnes + alignement
tableau_livres.column("ISBN", width=120, anchor="w")
tableau_livres.column("Titre", width=250, anchor="w")
tableau_livres.column("Auteur", width=150, anchor="w")
tableau_livres.column("Année", width=70, anchor="center")
tableau_livres.column("Genre", width=100, anchor="w")
tableau_livres.column("Statut", width=90, anchor="center")
tableau_livres.column("ID Membre", width=100, anchor="center")
tableau_livres.column("Nom Membre", width=150, anchor="w")
def quitter():
    biblio.sauvegarder()
    fenetre.destroy()


btn_quitter = tk.Button(
    cadre_tableau,
    text="sauvegarder et quitter",
    image=icones["done"],
    compound="left",
    bg="#009933",
    fg="white",
    font=("Arial", 12, "bold"),
    command=quitter
)
btn_quitter.pack(side="bottom", anchor="e", pady=10, padx=10)
# Créer un cadre en haut pour contenir onglets + bouton quitter
frame_onglets_bouton = tk.Frame(fenetre, bg="white")
frame_onglets_bouton.pack(fill="x", padx=10, pady=5)

# Notebook (onglets)
notebook = ttk.Notebook(frame_onglets_bouton)
notebook.pack(side="left", fill="x", expand=True)
# Pack du tableau en dessous, il prendra le reste de l’espace
tableau_livres.pack(fill="both", expand=True, padx=5, pady=(0,10))

def remplir_infos_depuis_tableau(event):
    selected = tableau_livres.selection()
    if not selected:
        return
    ligne = tableau_livres.item(selected[0])["values"]
    isbn = ligne[0]
    id_membre = ligne[6]

    # Remplir champs livre
    fields_livre["isbn"].delete(0, tk.END)
    fields_livre["isbn"].insert(0, isbn)
    fields_livre["titre"].delete(0, tk.END)
    fields_livre["titre"].insert(0, ligne[1])
    fields_livre["auteur"].delete(0, tk.END)
    fields_livre["auteur"].insert(0, ligne[2])
    fields_livre["annee"].delete(0, tk.END)
    fields_livre["annee"].insert(0, ligne[3])
    fields_livre["genre"].delete(0, tk.END)
    fields_livre["genre"].insert(0, ligne[4])

    # Remplir champ ID membre si présent
    if id_membre:
        id_entry.delete(0, tk.END)
        id_entry.insert(0, id_membre)
        rafraichir_livres_empruntes()

        # Sélectionner dans la liste des livres empruntés
        for i in range(livres_empruntes_listbox.size()):
            val = livres_empruntes_listbox.get(i)
            if val.startswith(id_membre):
                livres_empruntes_listbox.selection_set(i)
                break

tableau_livres.bind("<<TreeviewSelect>>", remplir_infos_depuis_tableau)



def maj_tout():
    # Mise à jour tableau livres
    for ligne in tableau_livres.get_children():
        tableau_livres.delete(ligne)

    for livre in biblio.livres.values():
        id_membre = ""
        nom_membre = ""
        if livre.statut == "emprunte":
            # chercher le membre qui emprunte ce livre
            for m in biblio.membres.values():
                if livre.isbn in getattr(m, "livres_empruntes", []):
                    id_membre = m.id_membre
                    nom_membre = m.nom
                    break
        tableau_livres.insert("", "end", values=(
            livre.isbn,
            livre.titre,
            livre.auteur,
            livre.annee,
            livre.genre,
            livre.statut,
            id_membre,
            nom_membre
        ))

    # Mise à jour listes disponibles et empruntées
    rafraichir_livres_disponibles()
    rafraichir_livres_empruntes()

# Chargement initial des données
biblio = Bibliotheque()
biblio.charger()

maj_tout()

fenetre.mainloop()
