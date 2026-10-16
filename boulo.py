import tkinter as tk
from tkinter import ttk, messagebox
import os
import json 
from datetime import datetime

fichier = "taches.json"

def charger_taches() :
    #charger tache depuis le fichier json
    if not os.path.exists(fichier):
        return[]
    with open(fichier, "r", encoding="utf-8") as f :
        try:
            return json.load(f)
        except json.JSONDecodeError :   
            return []

def sauvegarder_taches(taches) :
    #sauvegarder dans le fichier json
    with open(fichier, "w", encoding="utf-8")  as f :
        json.dump(taches, f, indent=4,ensure_ascii=False)

def ajouter_tache() :
    texte = entree.get().strip()
    if texte :
        date_du_jour = datetime.now().strftime("%d/%m/%Y  %H:%M")
        taches.append({"texte" : texte, "fait" : False, "date":date_du_jour})
        sauvegarder_taches(taches)
        afficher_taches()
        entree.delete(0, tk.END)
    else:
        messagebox.showwarning("attention","vous devez entree une tache")

def supprimer_tache(index):
    if 0 <= index < len (taches):
        del taches[index]
        sauvegarder_taches(taches)
        afficher_taches()

def toggle_tache(index):
    #marquer et demarquer une tache comme terminé
    if 0 <= index < len (taches):
        taches[index] ["fait"] = not taches[index] ["fait"]
        sauvegarder_taches(taches)
        afficher_taches()

def afficher_taches():
    #mis a jour l'affichage des taches
    for widget in cadre_taches.winfo_children():
        widget.destroy()

    for i, tache in enumerate(taches):
        var = tk.BooleanVar(value = tache["fait"])
        texte_affiche =f"{tache['texte']} ({tache.get('date','-')})"
        cb = tk.Checkbutton(
            cadre_taches,
            text= texte_affiche,
            variable= var,
            command= lambda idx = i: toggle_tache(idx),
            anchor = "w",
            width= 40
        )
        cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        btn = tk.Button(cadre_taches, text="X", command=lambda idx=i : supprimer_tache(idx))
        btn.grid(row=i, column = 1,padx = 5)

#interface
fenetre = tk.Tk()
fenetre.title(" MES TACHES✅")

#zone de saisie
entree = tk.Entry(fenetre, width=40)
entree.grid(row=0, column=0, padx=10, pady=10)

bouton_ajouter= tk.Button(fenetre, text="ajouter", command=ajouter_tache)
bouton_ajouter.grid(row=0, column=1, padx=5)

#cadre qui contient tous les taches
cadre_taches = tk.Frame(fenetre)
cadre_taches.grid(row=1, column=0, columnspan= 2, padx=10, pady=10)

#charger et afficher les taches au demarrage
taches = charger_taches()
afficher_taches()

fenetre.mainloop()
        
