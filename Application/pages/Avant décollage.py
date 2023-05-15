# Import des utilitaires.
import streamlit as st 
from functions import background_front, send_data_to_api, encart_prediction, formulaire_traitement

def before_takeoff():
    
    # ======================== FRONT ================================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ========================= FORM ================================>  
    submitted, value_features = formulaire_traitement(titre="Vous souhaitez savoir ?", table="before")
    
    # ===================== INJECTION DATA ==========================>  
    if submitted:
        send_data_to_api(data=value_features)
        encart_prediction(color="#FF9999", predict="en retard")
        encart_prediction(color="#90EE90", predict="à l'heure")
        st.write(value_features)        
    else:
        st.warning("Veuillez remplir tous les champs")
        
        # ===================== AFFICHAGE PREDICTTION =========================>  

        
before_takeoff()


















