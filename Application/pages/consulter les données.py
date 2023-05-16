import streamlit as st
from functions import background_front, get_data_from_api, columns_DataFrame, delete_data_via_api

columns_features_before_takeoff=[
    'id',
    'MONTH', 
    'DAY_OF_MONTH', 
    'DAY_OF_WEEK',
    'CRS_DEP_TIME',
    'CRS_ARR_TIME',
    'CRS_ELAPSED_TIME',
    'CARRIER',
    'DISTANCE'
]

# Colonnes de la table after.
columns_features_after_takeoff=[
    'id',
    'MONTH', 
    'DAY_OF_MONTH', 
    'DAY_OF_WEEK',
    'CRS_DEP_TIME',
    'CRS_ARR_TIME',
    'CRS_ELAPSED_TIME',
    'CARRIER',
    'DISTANCE',
    'DEP_DELAY'
]

# table prédiction
columns_prediction=[
    "id",
    "id_fk",
    "y_pred"
]


def data():
    
    # ===================== FRONT ==========================>  
    background_front(url="https://rare-gallery.com/uploads/posts/352939-4k-wallpaper.jpg")
     
    # ========================== PAGE ===============================>
    feature_after,  prediction_after=get_data_from_api(url="http://localhost:8000/data/get/after")
    feature_before, prediction_before=get_data_from_api(url="http://localhost:8000/data/get/before")
    
    after = columns_DataFrame(
        data1=feature_after, 
        data2=prediction_after, 
        columns_features=columns_features_after_takeoff, 
        columns_predict=columns_prediction
    )
    
    before = columns_DataFrame(
        data1=feature_before, 
        data2=prediction_before, 
        columns_features=columns_features_before_takeoff, 
        columns_predict=columns_prediction
    )

    st.title("Visualisation des données")
    st.header("Les données After")
    st.write(after)  
    st.header("Les données Before")
    st.write(before)
    
    if st.button("Supprimer toutes les données"):
        delete_data_via_api(url="http://localhost:8000/data/delete")        
    
    
data()





