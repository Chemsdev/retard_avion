# Import des utilitaires.
import streamlit as st 
from librairie import formulaire_traitement, create_table, save_formulaire
import pymysql


def main():
    
    # Connexion à la BDD.
    conn=pymysql.connect(host='localhost',port=int(3306),user='root', passwd='', db='avion')
    
    # Accueil (titre & header)
    st.header("Prédire les retards d'avion")
    st.title("Accueil")    
    
    # On créer la table de prédiction s'il n'existe pas.
    create_table(table_name="predictions_clients")
    
    # Initialisation du formulaire    
    formulaire={
        "DEP_TIME"  : st.number_input("Veuillez saisir l'heure de départ"),
        "DEP_DELAY" : st.number_input("Veuillez saisir le temps de retard en minute"),
        "DISTANCE"  : st.number_input("Veuillez saisir la distance en km"),
        "predict"   : 1
    }

    # Vérification de la saisie de l'utilisateur.
    if not formulaire_traitement(formulaire=formulaire):
        st.warning("Veuillez saisir tous les champs")    

    # Envoie dans la BDD.
    else:
        save_formulaire(conn=conn, features=[int(i) for i in formulaire.values()])
       
main()

