# =======================================================================================================================================>
#                                                            *UTILITAIRES*
# =======================================================================================================================================>

# Import des librairies.
import streamlit as st
import mysql.connector
import requests

# Paramètre de connexion.
cnx = mysql.connector.connect(
    user="chemsdine", 
    password="Ounissi69800", 
    host="chemsdineserver.mysql.database.azure.com", 
    port=3306, 
    database="avion_retard", 
    ssl_disabled=False
)
cursor = cnx.cursor()    

# Colonnes de la table before.
columns_features_before_takeoff=[
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

# =======================================================================================================================================>
#                                                            *SQL DATABASE*
# =======================================================================================================================================>

# Fonction permettant de créer les tables dans une base de données.
def create_tables(table_name_1: str, table_name_2: str, connexion=cnx, cursor=cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_1}
        (id INT AUTO_INCREMENT PRIMARY KEY,
        Month INTEGER,
        Day_of_month TEXT,
        Day_of_week TEXT,
        CRS_DEP_TIME TEXT,
        CRS_ARR_TIME INTEGER,
        CRS_ELAPSED_TIME INT,
        CARRIER TEXT,
        DISTANCE TEXT'''
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
#                                                            *SQL API*
# =======================================================================================================================================>

# Fonction pour envoyer les données à l'API.

# Fonction pour récupérer les données depuis l'API.
def send_data_to_api(data, url="http://localhost:8000/data/post"):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return st.success("Données insérées avec succès.")
    return st.error("Erreur lors de l'insertion des données.")


        
# =======================================================================================================================================>
#                                                            *FORMULAIRE*
# =======================================================================================================================================>

def formulaire_traitement(titre:str, table:str):
    st.title(titre)
    with st.form(f"formulaire_{table}"):
        st.write("**Veuillez remplir le formulaire**")
        value_features = {
            "question_1" : st.selectbox(f'**Veuillez saisir le mois**', [i for i in range(1, 13)]),                # Month
            "question_2" : st.selectbox(f'**Veuillez saisir le jour du mois**', [i for i in range(1, 32)]),        # Day of month
            "question_3" : st.selectbox(f'**Veuillez saisir le jour de la semaine**', [i for i in range(1, 8)]),   # Day of week
            "question_4" : st.text_input(f'**Veuillez saisir l"heure théorique de départ**'),                      # CRS DEP TIME need
            "question_5" : st.text_input(f'**Veuillez saisir l"heure théorique d"arrivée**'),                      # CRS ARR TIME need       
            "question_6" : st.text_input("**Temps théorique entre l'arrivée et le départ.**"),                     # CRS_ELAPSED_TIME
            "question_7" : st.text_input("**Veuillez saisir le code de compagnie aérienne**") ,                    # CARRIER
            "question_8" : st.text_input("**Veuillez saisir la distance en milliers du trajet**")                  # Distance
        }
        if table == "after":
            question_9 = st.text_input("**Veuillez saisir le retard en minutes depuis le décollage de l'avion**")   # DEP DELAY
            value_features["question_9"] = question_9
        submitted = st.form_submit_button("Envoyer")
    return submitted, value_features

# =======================================================================================================================================>
#                                                             *FRONT*
# =======================================================================================================================================>

# Fonction permettent de mettre un background.
def background_front(url:str):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({url});
             background-attachment: fixed;
             background-size: cover
            
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
            font-family: 'Comic Sans MS', cursive, sans-serif;
            text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
            font-color : #F5F5DC;
            font-size:67px;
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
