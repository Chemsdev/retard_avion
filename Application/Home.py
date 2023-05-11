# Import des utilitaires.
import streamlit as st 
from functions import create_tables, background_front, css_page_front, data_insert


def main():
    
    
    # ======================== Front ==============================>
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
    css_page_front()
    
    # ========================= SQL ================================>    
    create_tables(table_name_1="after_takeoff",   table_name_2="prediction_after_takeoff")
    create_tables(table_name_1="before_takeoff",  table_name_2="prediction_before_takeoff")

    # ======================== Formulaires =========================>
    data_insert(table_name_1="after_takeoff",   table_name_2="prediction_after_takeoff")
    data_insert(table_name_1="before_takeoff", table_name_2="prediction_before_takeoff")
    
      

   
main()

