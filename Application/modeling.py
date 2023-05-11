# Import des utilitaires.
from sklearn.neighbors import KNeighborsClassifier
from data_cleaning import titanic
import numpy as np

# ////////////////////////////////////////////////////////////// Modèle ///////////////////////////////////////////////////////////////////////////////// #

### Fonction pour faire la prédiction.
### Les paramètres : On donne en paramètre les features.
def prediction_survie(pclass, sex, age):
    
    # Modèle
    model = KNeighborsClassifier()
    
    # Séparation X et y
    y = titanic["survived"]
    X = titanic.drop("survived", axis=1)
    
    # Entrainement du modèle
    model.fit(X, y)
    model.score(X, y)
    x = np.array([pclass, sex, age]).reshape(1, 3)
    
    # Prédictions résultat
    predict = model.predict(x)
    if predict == 0:
        survie = "Tu n'aurais pas survécu..."
        return survie 
    survie = "Tu aurais survécu !"
    return survie

