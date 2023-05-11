# Import des utilitaires.
import streamlit as st 
from functions import create_tables, background_front, css_page_front, data_insert
from functions import columns_features_before_takeoff, columns_features_after_takeoff

def main():
    
    
    # ======================== Front ==============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    css_page_front()
    
    # ========================= SQL ================================>  
    create_tables(
        table_name_1="after_takeoff",   
        table_name_2="prediction_after_takeoff",
        features_columns=columns_features_after_takeoff
    )
    
    create_tables(
        table_name_1="before_takeoff",   
        table_name_2="prediction_before_takeoff",
        features_columns=columns_features_before_takeoff
    )
    # ========================= FORM ================================>  
    with st.form("my_form"):
        st.write("Veuillez remplir le formulaire")
        value_features=[]
        for i in columns_features_before_takeoff:
            a = st.text_input(f'Veuillez saisir {i}')
            value_features.append(a)
            
    # ===================== INJECTION DATA ==========================>  
        submitted = st.form_submit_button("Submit")
        if submitted:
            data_insert(
                table_name_1="before_takeoff",   
                table_name_2="prediction_before_takeoff",
                value_features=value_features, 
                columns_features=columns_features_before_takeoff, 
                y_pred="oui"        
            )



    
    
    
main()


