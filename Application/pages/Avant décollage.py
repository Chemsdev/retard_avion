# Import des utilitaires.
import streamlit as st 
from functions import background_front, send_data_to_api, encart_prediction, formulaire_traitement, prediction_model, model_before

def before_takeoff():
    
    # ======================== FRONT ===============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ========================= FORM ================================>  
    submitted, value_features = formulaire_traitement(titre="Vous souhaitez savoir ?", table="before")
    
    if submitted:
        
        # ===================== PREDICITON ====================================>  
        value_features = prediction_model(data=value_features, model=model_before)
        
        # ===================== INJECTION DATA ================================>  
        send_data_to_api(data=value_features, url="http://localhost:8000/data/post/before")
        
        # ===================== AFFICHAGE PREDICTION ==========================>  
        if value_features["Prediction"] == 1:
            encart_prediction(color="#FF9999", predict="en retard")
        else:
            encart_prediction(color="#90EE90", predict="à l'heure")
        
    else:
        st.warning("Veuillez remplir tous les champs")
          
before_takeoff()


















