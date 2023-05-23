# =======================================================================================================================================>
#                                                            *UTILITAIRES*
# =======================================================================================================================================>

# Import des librairies.
import streamlit as st
import mysql.connector
import requests
import pandas as pd
import pickle
import numpy as np

# Paramètre de connexion.
cnx = mysql.connector.connect(
    user="chemsdine", 
    password="Ounissi69800", 
    host="chemsdineserver.mysql.database.azure.com", 
    port=3306, 
    database="retard_avion", 
    ssl_disabled=False
)
cursor = cnx.cursor()    

# Colonnes de la table before.
columns_features_before_takeoff=[
    'id',
    'MONTH', 
    'DAY_OF_MONTH', 
    'DAY_OF_WEEK',
    'CRS_DEP_TIME',
    'CRS_ARR_TIME',
    'CRS_ELAPSED_TIME',
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
    'DISTANCE',
    'DEP_DELAY'
]

# table prédiction
columns_prediction=[
    "id",
    "id_fk",
    "y_pred"
]

# Import du modèle
model_before = pickle.load(open('before_model.pickle', 'rb'))
model_after  = pickle.load(open('after_model.pickle', 'rb'))


# =======================================================================================================================================>
#                                                      *SQL DATABASE*
# =======================================================================================================================================>

# Fonction permettant de créer les tables dans une base de données.
def create_tables(table_name_1: str, table_name_2: str, connexion=cnx, cursor=cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_1}
        (id INT AUTO_INCREMENT PRIMARY KEY,
        Month INTEGER,
        Day_of_month INTEGER,
        Day_of_week INTEGER,
        CRS_DEP_TIME TEXT,
        CRS_ARR_TIME TEXT,
        CRS_ELAPSED_TIME TEXT,
        DISTANCE INTEGER'''
        + (", DEP_DELAY INTEGER" if table_name_1 == "after_takeoff" else "")
        + ''')''')
    print(f"Table '{table_name_1}' créée avec succès.")    
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_2}
                (id INT AUTO_INCREMENT PRIMARY KEY,
                id_fk INT,
                y_pred TEXT,
                FOREIGN KEY (id_fk) REFERENCES {table_name_1}(id))''')
    print(f"Table '{table_name_2}' créée avec succès.")
    connexion.commit()
    
# =======================================================================================================================================>
#                                                        *SQL API*
# =======================================================================================================================================>

# Fonction pour récupérer les données depuis l'API.
def send_data_to_api(data:dict, url:str):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return st.success("Données insérées avec succès.")
    return st.error("Erreur lors de l'insertion des données.")

# Fonction pour afficher les données depuis l'API.
def get_data_from_api(url:str):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data")
        return data
    return st.error("Erreur lors de la récupération des données.")

# Fonction pour supprimer les données via l'API.
def delete_data_via_api(url):
    response = requests.delete(url)
    if response.status_code == 200:
        print("Les données ont été supprimées avec succès.")
    else:
        print("Erreur lors de la suppression des données.")

# =======================================================================================================================================>
#                                                       *FORMULAIRE*
# =======================================================================================================================================>

def formulaire_traitement(titre:str, table:str):
    st.title(titre)
    with st.form(f"formulaire_{table}"):
        st.write("**Veuillez remplir le formulaire**")
        value_features = {
            "question_1" : st.selectbox(f'Veuillez saisir le mois', [i for i in range(1, 13)]),                # Month
            "question_2" : st.selectbox(f'Veuillez saisir le jour du mois', [i for i in range(1, 32)]),        # Day of month
            "question_3" : st.selectbox(f'Veuillez saisir le jour de la semaine', [i for i in range(1, 8)]),   # Day of week
            "question_4" : str(st.time_input(f'Veuillez saisir l"heure théorique de départ')),                      # CRS DEP TIME need
            "question_5" : str(st.time_input(f'Veuillez saisir l"heure théorique d"arrivée')),                      # CRS ARR TIME need       
            "question_6" : str(st.time_input("Temps théorique entre l'arrivée et le départ.")),                     # CRS_ELAPSED_TIME
            "question_7" : st.number_input("Veuillez saisir la distance en milliers du trajet")                  # Distance
        }
        if table == "after":
            question_8 = st.text_input("**Veuillez saisir le retard en minutes depuis le décollage de l'avion**")   # DEP DELAY
            value_features["question_8"] = question_8
        submitted = st.form_submit_button("Envoyer")
    return submitted, value_features

# =======================================================================================================================================>
#                                                        *FRONT*
# =======================================================================================================================================>

# Fonction permettent de mettre un background.
def background_front(url:str):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({url});
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
    )
    
# =======================================================================================================================================>

# Fonction permettent d'apporter du style au site web.
def css_page_front():
    st.markdown("""
    <style>
        body {
        background-size: cover;
        }
        h1 {
            text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
            font-color : #F5F5DC;
            font-size:67px;
        }
        p {
            text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
            font-size:25px;
            # text-shadow: 1px 1px 2px pink;
        }
    </style>
    """, unsafe_allow_html=True)

# =======================================================================================================================================>

# fonction permettent de créer l'encart pour afficher la prédiction.
def encart_prediction(color:str, predict:str):
    st.markdown("")
    box_style = f"""
        padding: 20px;
        width: 230px;
        height: 80px;
        border: 2px solid {color};
        border-radius: 5px
    """

    text_style = f"""
        color: {color};
        font-size: 18px;
        font-weight: bold;
    """

    st.markdown(
        f'<div style="{box_style}">'
        f'<p style="{text_style}">Votre vol est {predict} !</p>'
        f'</div>',
        unsafe_allow_html=True
    )

# =======================================================================================================================================>

# Fonction permettent de mettre les noms de colonnes aux DataFrames et faire un merge.
def columns_DataFrame(data1, data2, columns_features, columns_predict):
    features   = pd.DataFrame(data1, columns=columns_features)
    prediction = pd.DataFrame(data2, columns=columns_predict)
    data = pd.merge(features, prediction, left_on='id', right_on='id_fk')
    data = data.drop(["id_y", "id_fk", "id_x"], axis=1)
    return data

# =======================================================================================================================================>

# Fonction permettent de préparer les données aux modèles et faire la prédiction.
def prediction_model(data, model):
    data_for_bdd = data.copy()
    for i in (4, 5, 6):
        time = data[f"question_{i}"]
        total_minutes = (60 * int(time[0:2])) + int(time[3:5])
        data[f"question_{i}"] = total_minutes
    data_array = np.array(list(data.values())).reshape(1, -1)
    pred = model.predict(data_array)
    data_for_bdd["Prediction"] = int(round(pred.item()))
    return data_for_bdd

