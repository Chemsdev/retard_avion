import pandas as pd
from functions import cnx
import streamlit as st
from functions import delete_content_tables, background_front


def data():
    
    # ===================== FRONT ==========================>  
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ===================== SQL ==========================>  
    table_features_before    = pd.read_sql_query("SELECT * FROM before_takeoff", cnx)
    table_predictions_before = pd.read_sql_query("SELECT * FROM prediction_before_takeoff", cnx)
    
    table_features_after     = pd.read_sql_query("SELECT * FROM after_takeoff", cnx)
    table_predictions_after  = pd.read_sql_query("SELECT * FROM prediction_after_takeoff", cnx)
    
    # ========================== PAGE ===============================>
    st.title("Données Avant décollage")
    if table_features_before.empty or table_predictions_before.empty:
        st.error("Base de données vide !")
    else:
        st.markdown("**Les features**")
        st.write(table_features_before)
        st.markdown("**Les prédictions**")
        st.write(table_predictions_before)
    
    st.title("Données après décollage")
    if table_features_after.empty or table_predictions_after.empty:
        st.error("Base de données vide !")
        
    else:
        st.markdown("**Les features**")
        st.write(table_features_after)
        st.markdown("**Les prédictions**")
        st.write(table_predictions_after)
        
        # ===================== DELETE DATA ==========================>
        if st.button("Supprimer toutes les données"):
            delete_content_tables(connexion=cnx)
data()