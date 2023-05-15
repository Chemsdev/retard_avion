# Import des utilitaires.
import streamlit as st 
import streamlit.components.v1 as components
from functions import formulaire_traitement, background_front, encart_prediction, send_data_to_api
from functions import columns_features_after_takeoff, columns_features_before_takeoff

def after_takeoff():
    
    # ======================== FRONT ===============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ======================== FORM ================================>  
    submitted, value_features = formulaire_traitement(titre="Vous souhaitez savoir ?", table="after")
            
    # ===================== INJECTION DATA =========================>  
    if not submitted:
        st.warning("Veuillez remplir tous les champs")
    else:
        send_data_to_api(data=value_features)
        st.write(value_features)
        
        # ===================== AFFICHAGE PREDICTTION =========================>  
        encart_prediction(color="#FF9999", predict="en retard")
        encart_prediction(color="#90EE90", predict="à l'heure")
        
after_takeoff()