# =======================================================================================================================================>
#                                                            *UTILITAIRES*
# =======================================================================================================================================>

# Import des librairies.
import streamlit as st
import numpy as np
import mysql.connector
import pandas as pd

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
def create_tables(table_name_1:str, table_name_2:str, features_columns:list, connexion=cnx, cursor=cursor):    
    col_names_str = ','.join([f'{i} REAL' for i in features_columns])    
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_1}
                (id INT AUTO_INCREMENT PRIMARY KEY, {col_names_str})''')
    print(f"Table '{table_name_1}' créée avec succès.")
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_2}
                (id INT AUTO_INCREMENT PRIMARY KEY,
                id_fk INT,
                y_pred TEXT,
                FOREIGN KEY (id_fk) REFERENCES {table_name_1}(id))''')
    print(f"Table '{table_name_2}' créée avec succès.")
    connexion.commit()
    
# =======================================================================================================================================>

# Fonction permettent d'insérer des données dans les tables cible.
def data_insert(table_name_1: str, table_name_2: str, value_features: list, columns_features: list, y_pred: str, connexion=cnx, cursor=cursor):
    table1_sql = f"INSERT INTO {table_name_1} ({', '.join(columns_features)}) VALUES ({', '.join(['%s' for _ in range(len(columns_features))])})"
    cursor.execute(table1_sql, value_features)
    inserted_id = cursor.lastrowid
    table2_columns = ["id_fk", "y_pred"]
    table2_values = [inserted_id, y_pred]
    table2_sql = f"INSERT INTO {table_name_2} ({', '.join(table2_columns)}) VALUES ({', '.join(['%s' for _ in range(len(table2_columns))])})"
    cursor.execute(table2_sql, table2_values)
    print("Données insérées avec succès.")
    connexion.commit()
    
# =======================================================================================================================================>

# Fonction permettent de supprimer 2 tables.
def delete_content_tables(connexion=cnx):
    cursor.execute("DELETE FROM prediction_after_takeoff")
    cursor.execute("DELETE FROM prediction_before_takeoff")
    cursor.execute("DELETE FROM after_takeoff")
    cursor.execute("DELETE FROM before_takeoff")
    connexion.commit()

# =======================================================================================================================================>

# Fonction permettent d'afficher les tables dans la page data.
def show_page(title:str, name_table_features:str, name_table_prediction:str):
    table1 = pd.read_sql_query(f"SELECT * FROM {name_table_features}",   cnx)
    table2 = pd.read_sql_query(f"SELECT * FROM {name_table_prediction}", cnx)
    st.title(title)
    if table1.empty or table2.empty:
        return st.error("Base de données vide !")
    else:
        st.markdown("**Les Features**")
        st.write(table1)
        st.markdown("**Les Prédictions**")
        st.write(table2)
    
# =======================================================================================================================================>
#                                                          *FRONT*
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
        background-image: url("data:image/png;base64,%s");
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


