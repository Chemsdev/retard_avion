import pandas as pd
from functions import cnx
import streamlit as st
from functions import delete_content_tables, background_front, show_page


def data():
    
    # ===================== FRONT ==========================>  
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
     
    # ========================== PAGE ===============================>
    show_page(title="Données Avant décollage", name_table_features="after_takeoff",  name_table_prediction="prediction_after_takeoff")
    show_page(title="Données après décollage", name_table_features="before_takeoff", name_table_prediction="prediction_before_takeoff")
        
    # ===================== DELETE DATA ==========================>
    if st.button("Supprimer toutes les données"):
        delete_content_tables(connexion=cnx)
        
data()





