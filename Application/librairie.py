# Import des librairies.
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np


# ////////////////////////////////////////////////////////////// DATA SQL //////////////////////////////////////////////////////////////////////////// #

### Fonction permettent d'envoyer les 12 DataFrames sur SQL.
### Les paramètres : on donne en paramètre les numéros de fichiers.
def send_df_to_sql(number_file:list):    
    print("Envoie des DataFrames dans les tables SQL...")
    for i in number_file:         
        table_name=f'2016_{i}'
        df=pd.read_csv(f"data/{table_name}.csv", error_bad_lines=False)
        engine=create_engine('mysql+pymysql://root:@localhost/avion')
        inspector=inspect(engine)
        if table_name in inspector.get_table_names():
            print(f"Table {table_name} déja existante...")
        else:
            df.to_sql(name=table_name, con=engine, if_exists='fail', index=False)
    print("===> Envoie des 12 DataFrames en BDD réussis.")
            
### Fonction permettent de récupérer les 12 tables présentes sur SQL et contaténation.
### Les paramètres : on donne en paramètre les numéros de fichiers et la connexion à la BDD.
def get_tables_SQL(conn, number_file:list):                                                      
    print("Obtention et concaténation des 12 Tables SQL...")
    liste_tables=[]
    for i in number_file:
        table=pd.read_sql_query(f"SELECT * FROM 2016_{i}", conn)
        liste_tables.append(table)
    df_concat=pd.concat([i for i in liste_tables], axis=0)
    print("===> Concaténation des 12 tables réussis.")
    return df_concat

### Fonction permettent de créer une table.
### Les paramètres : On donne en paramètre le nom de la table que nous souhaitons créer
def create_table(table_name:str):
    engine=create_engine('mysql+pymysql://root:@localhost/avion')
    inspector=inspect(engine)
    if not table_name in inspector.get_table_names():
        
        # Initialisation des colonnes.
        df = pd.DataFrame({'DEP_TIME':[], 'DEP_DELAY':[] , 'DISTANCE':[], "predict":[]})
        
        # Typage des colonnes de la Table SQL.
        df['DEP_TIME' ]  = df['DEP_TIME' ].astype('float64')
        df['DEP_DELAY']  = df['DEP_DELAY'].astype('float64')
        df['DISTANCE' ]  = df['DISTANCE' ].astype('float64')
        df['predict'  ]  = df['predict'  ].astype('str')
        
        # envoie du DataFrame sur SQL.
        df.to_sql(name=table_name, con=engine, if_exists='fail', index=False)
    print(f"Création de la table {table_name} avec succès.")

# //////////////////////////////////////////////////////// Traitement Formulaire ///////////////////////////////////////////////////////////////////// #

### Fonction permettent de traiter le formulaire.
### Les paramètres : on donne en paramètre les réponses de l'utilisateur sous forme de dictionnaire.
def formulaire_traitement(formulaire:dict):
    for i in formulaire.values():
        if i == 0.00:
            print("Veuillez saisir tous les champs !")
            return False
    return True        

### Fonction permettent d'enregistrer le formulaire en BDD (la target et les features).
### Les paramètres : la connexion à la BDD, et une liste des features.    
def save_formulaire(conn, features:list):
    cursor = conn.cursor()
    sql = "INSERT INTO predictions_clients (DEP_TIME, DEP_DELAY, DISTANCE, predict) VALUES (%s, %s,%s,%s)"
    cursor.execute(sql, features)
    conn.commit()
    conn.close()    






    
    
            