# Import des utilitaires.
import streamlit as st 
from functions import create_tables, background_front, css_page_front

base='dark'
st.set_page_config(layout="wide")

def main():
    
    # ======================== FRONT ==============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    css_page_front()    
    st.title("Bienvenue")
    st.markdown("""
                Nous sommes une entreprise spécialisée dans les services de prédiction des retards de vols. 
                Notre approche novatrice permet aux clients de savoir à l'avance si leur vol sera en retard ou non. 
                Pour cela, nous mettons à leur disposition deux formulaires distincts : l'un pour les vols déjà réalisés et l'autre pour les vols 
                avant le décollage. Grâce à ces formulaires, nos clients peuvent obtenir des prévisions précises et fiables sur les retards 
                potentiels, leur permettant ainsi de mieux planifier leurs voyages et d'éviter les désagréments liés aux retards aériens.
            """)
    
    
    # ========================= SQL ===============================>  
    create_tables(
        table_name_1="after_takeoff",   
        table_name_2="prediction_after_takeoff",
    )
    
    create_tables(
        table_name_1="before_takeoff",   
        table_name_2="prediction_before_takeoff",
    )

main()




