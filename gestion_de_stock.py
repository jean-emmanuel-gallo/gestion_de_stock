import tkinter as tk
from tkinter import ttk
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Jedeviles88",
    database="boutique"
)
cursor = db.cursor()

fenetre = tk.Tk()
fenetre.title("Gestion de stock")

tableau = tk.ttk.Treeview(fenetre, columns=("nom_produit", "stock", "prix"))
tableau.heading("#0", text="ID")
tableau.heading("nom_produit", text="Nom du produit")
tableau.heading("stock", text="Stock")
tableau.heading("prix", text="Prix")
tableau.pack(padx=10, pady=10)

champ_nom_produit = tk.Entry(fenetre)
champ_nom_produit.pack(padx=10, pady=5)
champ_stock = tk.Entry(fenetre)
champ_stock.pack(padx=10, pady=5)
champ_prix = tk.Entry(fenetre)
champ_prix.pack(padx=10, pady=5)


def ajouter_produit():
    nom_produit = champ_nom_produit.get()
    stock = champ_stock.get()
    prix = champ_prix.get()
    
    cursor.execute("INSERT INTO produit (nom_produit, stock, prix) VALUES (%s, %s, %s)", (nom_produit, stock, prix))
    
    db.commit()
    message.configure(text="Le produit a été ajouté.")
    
    champ_nom_produit.delete(0, tk.END)
    champ_stock.delete(0, tk.END)
    champ_prix.delete(0, tk.END)
    afficher_produit()


def afficher_produit():
    for row in tableau.get_children():
        tableau.delete(row)
        
    cursor.execute("SELECT * FROM produit")
    produit = cursor.fetchall()
    
    for produit in produit:
        tableau.insert("", tk.END, values=produit)




def modifier_produit():
    id_produit = tableau.item(tableau.selection())["text"]
    
    nouveau_nom_produit = champ_nom_produit.get()
    nouveau_stock = champ_stock.get()
    nouveau_prix = champ_prix.get()
    
    cursor.execute("UPDATE produit SET nom_produit = %s, stock = %s, prix = %s WHERE id_produit = %s", (nouveau_nom_produit, nouveau_stock, nouveau_prix, id_produit))
    
    db.commit()
    message.configure(text="Le produit a été modifié.")
    
    champ_nom_produit.delete(0, tk.END)
    champ_stock.delete(0, tk.END)
    champ_prix.delete(0, tk.END)
    afficher_produit()


def supprimer_produit():
    """
    Supprime le produit sélectionné de la liste et réinitialise les champs du formulaire.
    """
    index = liste_produits.curselection()
    if index:
        liste_produits.delete(index)
        entree_nom.delete(0, tk.END)
        entree_prix.delete(0, tk.END)
        entree_quantite.delete(0, tk.END)
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer.")


bouton_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter_produit)
bouton_ajouter.pack(padx=10, pady=5)
bouton_supprimer = tk.Button(fenetre, text="Supprimer", command=supprimer_produit)
bouton_supprimer.pack(padx=10, pady=5)
bouton_modifier = tk.Button(fenetre, text="Modifier", command=modifier_produit)
bouton_modifier.pack(padx=10, pady=5)

message = tk.Label(fenetre, text="")
message.pack(padx=10, pady=5)


afficher_produit()

fenetre.mainloop()
