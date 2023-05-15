# Import des utilitaires.
import streamlit as st 
from functions import create_tables, background_front, css_page_front

base='dark'
st.set_page_config(layout="wide")

def main():
    
    # ======================== FRONT ==============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    css_page_front()    
    st.title("Bienvenue...")
    
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




