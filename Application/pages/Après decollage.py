# Import des utilitaires.
import streamlit as st 
from functions import formulaire_traitement, background_front, encart_prediction, send_data_to_api, prediction_model, model_after

def after_takeoff():
    
    # ======================== FRONT ===============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ========================= FORM ================================>  
    submitted, value_features = formulaire_traitement(titre="Après décollage de votre Avion", table="after")
            
    if submitted:
        
        # ===================== PREDICITON ====================================>  
        value_features = prediction_model(data=value_features, model=model_after)
        
        # ===================== INJECTION DATA ================================>  
        send_data_to_api(data=value_features, url="http://localhost:8000/data/post/after")
        
        # ===================== AFFICHAGE PREDICTION ==========================>  
        if value_features["Prediction"] == 1:
            encart_prediction(color="#FF9999", predict="en retard")
        else:
            encart_prediction(color="#90EE90", predict="à l'heure")
        
    else:
        st.warning("Veuillez remplir tous les champs")
        
after_takeoff()

