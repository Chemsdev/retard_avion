# Import des utilitaires.
import streamlit as st 
from functions import background_front, css_page_front, data_insert
from functions import columns_features_before_takeoff

def before_takeoff():
    
    # ======================== FRONT ================================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    
    # ========================= FORM ================================>  
    st.title("Vous souhaitez savoir ?")
    with st.form("formulaire_before_take_off"):
        st.write("**Veuillez remplir le formulaire**")
        value_features=[]
        for i in columns_features_before_takeoff:
            a = st.text_input(f'**Veuillez saisir {i}**')
            value_features.append(a)
            
    # ===================== INJECTION DATA ==========================>  
        submitted = st.form_submit_button("Envoyer")
        if submitted:
            data_insert(
                table_name_1="before_takeoff",   
                table_name_2="prediction_before_takeoff",
                value_features=value_features, 
                columns_features=columns_features_before_takeoff, 
                y_pred="oui"        
            )

before_takeoff()